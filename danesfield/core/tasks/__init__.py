import configparser
from distutils.dir_util import copy_tree
import json
from pathlib import Path
import shutil
import tempfile
from typing import List, Union
import zipfile

import celery
from celery.utils.log import get_task_logger
from rdoasis.algorithms.models import AlgorithmTask, Dataset
from rdoasis.algorithms.tasks.common import ManagedTask
from rdoasis.algorithms.tasks.docker import _run_algorithm_task_docker
import requests
from rgd.models import FileSet
from rgd_3d.models import Mesh3D, Tiles3D
from rgd_imagery.models import Image, ImageSet, Raster

from danesfield.core.utils import danesfield_algorithm

logger = get_task_logger(__name__)

RGD_IMAGERY_EXTENSIONS = ('.tif', '.png')
RGD_3D_EXTENSIONS = ('.ply', '.obj')


def _ingest_checksum_files(dataset: Dataset):
    images: List[Image] = []
    meshes: List[Mesh3D] = []
    for checksum_file in dataset.files.all():
        extension: str = Path(checksum_file.name).suffix

        if not extension:
            continue

        if extension in RGD_IMAGERY_EXTENSIONS:
            images.append(Image(file=checksum_file))
        elif extension in RGD_3D_EXTENSIONS:
            meshes.append(Mesh3D(file=checksum_file))

        # 3D tiles is a special case - save all associated files into the
        # database all at once
        elif checksum_file.name.endswith('tileset.json'):
            # Create a fileset for this 3D tiles dataset
            tiles_3d_fileset = FileSet.objects.create(name=dataset.name)

            # Get the base directory of the 3D tiles dataset
            tiles_3d_base_dir = Path(checksum_file.name).parent

            tiles_3d_fileset.checksumfile_set.set(
                dataset.files.filter(name__startswith=tiles_3d_base_dir)
            )
            Tiles3D.objects.create(name=dataset.name, json_file=checksum_file)

    if images:
        images = Image.objects.bulk_create(images)
        for image in images:
            image_set = ImageSet.objects.create(name=image.file.name)
            image_set.images.set([image])
            Raster.objects.create(name=image.file.name, image_set=image_set)

    if meshes:
        Mesh3D.objects.bulk_create(meshes)


class DanesfieldTask(ManagedTask):
    """Subclass ManagedTask to add extra functionality."""

    def _ensure_model_files(self):
        """
        Download any model files needed.

        Currently, the only needed model is the Columbia Geon Segmentation Model.
        """
        # Check if models dir already exists, and if not, download
        self.models_dir = Path('/tmp/danesfield_models')
        if not self.models_dir.exists():
            # Else, download models
            url = 'https://data.kitware.com/api/v1/resource/download'
            params = {'resources': json.dumps({'folder': ['5fa1b6c850a41e3d192de93b']})}

            logger.info('Downloading model files. This may take a while...')

            # Download file
            _, folder_zip_path = tempfile.mkstemp()
            with requests.get(url, params=params, stream=True) as r:
                with open(folder_zip_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

            # Extract folder from zip
            self.models_dir.mkdir()
            with zipfile.ZipFile(folder_zip_path) as z:
                z.extractall(self.models_dir)

        # Copy to input dir
        copy_tree(src=str(self.models_dir), dst=str(self.input_dir))

    def _write_config_file(self):
        """Create and write the config file."""
        # Assume that input dataset is only one file, and that file is the point cloud file
        point_cloud_path = self.input_dataset_paths[0]

        # Construct config
        config = configparser.ConfigParser()
        config['paths'] = {
            'p3d_fpath': point_cloud_path,
            'work_dir': self.output_dir,
            'rpc_dir': tempfile.mkdtemp(),
        }

        config['aoi'] = {'name': self.algorithm_task.input_dataset.name.replace(' ', '_')}
        config['params'] = {'gsd': 0.25}
        config['roof'] = {
            'model_dir': f'{self.input_dir}/Columbia Geon Segmentation Model',
            'model_prefix': 'dayton_geon',
        }

        # Write config to disk
        self.config_path = self.input_dir / 'config.ini'
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

    def _upload_result_files(self):
        super()._upload_result_files()
        _ingest_checksum_files(self.algorithm_task.output_dataset)

    def _setup(self, **kwargs):
        super()._setup(**kwargs)

        self._ensure_model_files()
        self._write_config_file()


@celery.shared_task(base=DanesfieldTask, bind=True)
def run_danesfield_task(self: DanesfieldTask, *args, **kwargs):
    _run_algorithm_task_docker(self, *args, **kwargs)


def run_danesfield(input_dataset_pk: Union[str, int]) -> AlgorithmTask:
    danesfield = danesfield_algorithm()
    return danesfield.run(input_dataset_pk, celery_task=run_danesfield_task)

import configparser
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import List, Set
import zipfile

from billiard.einfo import ExceptionInfo
import celery
from celery.utils.log import get_task_logger
from django.core.files.uploadedfile import SimpleUploadedFile
import requests
from rgd.models.common import ChecksumFile
from rgd_3d.models import Mesh3D
from rgd_imagery.models.base import Image, ImageSet


from rdoasis.algorithms.tasks.common import ManagedTask
from rdoasis.algorithms.tasks.algorithms import _run_algorithm_task

logger = get_task_logger(__name__)

RGD_IMAGERY_EXTENSIONS = ('.tif', '.png')
RGD_3D_EXTENSIONS = ('.ply', '.obj')


def _ingest_checksum_files(files: List[ChecksumFile]):
    images: List[Image] = []
    meshes: List[Mesh3D] = []
    for checksum_file in files:
        extension: str = Path(checksum_file.name).suffix

        if not extension:
            continue

        if extension in RGD_IMAGERY_EXTENSIONS:
            images.append(Image(file=checksum_file))
        elif extension in RGD_3D_EXTENSIONS:
            meshes.append(Mesh3D(file=checksum_file))

    if images:
        ImageSet.objects.create().images.set(Image.objects.bulk_create(images))

    if meshes:
        Mesh3D.objects.bulk_create(meshes)


# class ManagedTask(celery.Task):
#     def _upload_result_files(self):
#         """Upload any new files to the dataset."""
#         new_checksum_files: List[ChecksumFile] = []
#         existing_filenames: Set[str] = {file.name for file in self.dataset.files.all()}
#         for path, _, files in os.walk(self.output_dir):
#             fixed_filenames = {os.path.join(path, file) for file in files}
#             new_filenames = fixed_filenames - existing_filenames

#             for f in new_filenames:
#                 relative_filename = Path(f).relative_to(self.output_dir)
#                 checksum_file = ChecksumFile(name=relative_filename)

#                 with open(f, 'rb') as file_contents:
#                     checksum_file.file = SimpleUploadedFile(
#                         name=relative_filename, content=file_contents.read()
#                     )

#                 checksum_file.save()
#                 existing_filenames.add(f)
#                 new_checksum_files.append(checksum_file)

#         self.dataset_run.output_files.add(*new_checksum_files)
#         _ingest_checksum_files(new_checksum_files)

#     def _ensure_model_files(self):
#         """
#         Download any model files needed.

#         Currently, the only needed model is the Columbia Geon Segmentation Model.
#         """
#         # Check if models dir already exists, and if so, exit
#         self.models_dir = Path('/tmp/danesfield_models')
#         if self.models_dir.exists():
#             return

#         # Else, download models
#         url = 'https://data.kitware.com/api/v1/resource/download'
#         params = {'resources': json.dumps({'folder': ['5fa1b6c850a41e3d192de93b']})}

#         logger.info('Downloading model files. This may take a while...')

#         # Download file
#         _, folder_zip_path = tempfile.mkstemp()
#         with requests.get(url, params=params, stream=True) as r:
#             with open(folder_zip_path, 'wb') as f:
#                 shutil.copyfileobj(r.raw, f)

#         # Extract folder from zip
#         self.models_dir.mkdir()
#         with zipfile.ZipFile(folder_zip_path) as z:
#             z.extractall(self.models_dir)

#     def _download_dataset(self):
#         """Download the dataset."""
#         if not self.dataset.imageless:
#             self.point_cloud_path = None

#             # TODO: Handle imageful case
#             return

#         # Imageless case
#         self.point_cloud_path = self.dataset.point_cloud_file.download_to_local_path(
#             tempfile.mkdtemp()
#         )

#     def _write_config_file(self):
#         """Create and write the config file."""
#         config = configparser.ConfigParser()
#         config['paths'] = {
#             'p3d_fpath': self.point_cloud_path,
#             'work_dir': self.output_dir,
#             'rpc_dir': tempfile.mkdtemp(),
#         }

#         config['aoi'] = {'name': self.dataset.name.replace(' ', '_')}
#         config['params'] = {'gsd': 0.25}
#         config['roof'] = {
#             'model_dir': f'{self.models_dir}/Columbia Geon Segmentation Model',
#             'model_prefix': 'dayton_geon',
#         }

#         # Write config to disk
#         self.config_path = Path(tempfile.mkstemp(suffix='.ini')[1])
#         with open(self.config_path, 'w') as configfile:
#             config.write(configfile)

#     def _setup(self, **kwargs):
#         # Set run on task instance
#         self.dataset_run: DatasetRun = DatasetRun.objects.select_related(
#             'dataset', 'dataset__point_cloud_file'
#         ).get(pk=kwargs['dataset_run_id'])

#         # Set run status
#         self.dataset_run.status = DatasetRun.Status.RUNNING
#         self.dataset_run.save()

#         # Set step on task instance
#         self.dataset: Dataset = self.dataset_run.dataset

#         # Ensure necessary files and directories exist
#         self.output_dir = Path(tempfile.mkdtemp())
#         self._download_dataset()
#         self._ensure_model_files()

#         # Write config file
#         self._write_config_file()

#     def _cleanup(self):
#         """Perform any necessary cleanup."""
#         # Remove dirs
#         # Don't remove self.model_dir, as other tasks will need it
#         shutil.rmtree(self.output_dir, ignore_errors=True)

#         # Remove files
#         self.config_path.unlink(missing_ok=True)
#         if self.point_cloud_path is not None:
#             self.point_cloud_path.unlink(missing_ok=True)

#     def on_failure(self, exc, task_id, args, kwargs, einfo: ExceptionInfo):
#         if not self.dataset_run.output_log:
#             self.dataset_run.output_log = ''

#         self.dataset_run.output_log += einfo.traceback
#         self.dataset_run.status = DatasetRun.Status.FAILED
#         self.dataset_run.save()

#         self._cleanup()

#     def on_success(self, retval, task_id, args, kwargs):
#         self._upload_result_files()

#         # Mark dataset run as succeeded and save logs
#         self.dataset_run.status = DatasetRun.Status.SUCCEEDED
#         self.dataset_run.save()

#         self._cleanup()

#     def __call__(self, **kwargs):
#         # Setup
#         self._setup(**kwargs)

#         # Run task
#         return self.run(**kwargs)


class DanesfieldTask(ManagedTask):
    def __call__(self, **kwargs):
        print("---------")
        return super().__call__(**kwargs)


@celery.shared_task(base=DanesfieldTask, bind=True)
def run_danesfield(self: DanesfieldTask, *args, **kwargs):
    _run_algorithm_task(self, *args, **kwargs)

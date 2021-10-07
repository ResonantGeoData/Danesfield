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

from danesfield.core.models import Dataset, DatasetRun

logger = get_task_logger(__name__)


class ManagedTask(celery.Task):
    def _upload_result_files(self):
        """Upload any new files to the dataset."""
        new_checksum_files: List[ChecksumFile] = []
        existing_filenames: Set[str] = {file.name for file in self.dataset.files.all()}
        for path, _, files in os.walk(self.output_dir):
            fixed_filenames = {os.path.join(path, file) for file in files}
            new_filenames = fixed_filenames - existing_filenames

            for f in new_filenames:
                relative_filename = Path(f).relative_to(self.output_dir)
                checksum_file = ChecksumFile(name=relative_filename)

                with open(f, 'rb') as file_contents:
                    checksum_file.file = SimpleUploadedFile(
                        name=relative_filename, content=file_contents.read()
                    )

                checksum_file.save()
                existing_filenames.add(f)
                new_checksum_files.append(checksum_file)

        self.dataset_run.output_files.add(*new_checksum_files)

    def _ensure_model_files(self):
        """
        Download any model files needed.

        Currently, the only needed model is the Columbia Geon Segmentation Model.
        """
        # Check if models dir already exists, and if so, exit
        self.models_dir = Path('/tmp/danesfield_models')
        if self.models_dir.exists():
            return

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

    def _download_dataset(self):
        """Download the dataset."""
        if not self.dataset.imageless:
            self.point_cloud_path = None

            # TODO: Handle imageful case
            return

        # Imageless case
        fd, path = tempfile.mkstemp()
        self.point_cloud_path = Path(path)

        file = self.dataset.point_cloud_file.file
        with os.fdopen(fd, 'wb') as point_cloud_in:
            shutil.copyfileobj(file, point_cloud_in)
            point_cloud_in.flush()

    def _write_config_file(self):
        """Create and write the config file."""
        config = configparser.ConfigParser()
        config['paths'] = {
            'p3d_fpath': self.point_cloud_path,
            'work_dir': self.output_dir,
            'rpc_dir': tempfile.mkdtemp(),
        }

        config['aoi'] = {'name': self.dataset.name.replace(' ', '_')}
        config['params'] = {'gsd': 0.25}
        config['roof'] = {
            'model_dir': f'{self.models_dir}/Columbia Geon Segmentation Model',
            'model_prefix': 'dayton_geon',
        }

        # Write config to disk
        self.config_path = Path(tempfile.mkstemp()[1])
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

    def _setup(self, **kwargs):
        # Set run on task instance
        self.dataset_run: DatasetRun = DatasetRun.objects.select_related(
            'dataset', 'dataset__point_cloud_file'
        ).get(pk=kwargs['dataset_run_id'])

        # Set run status
        self.dataset_run.status = DatasetRun.Status.RUNNING
        self.dataset_run.save()

        # Set step on task instance
        self.dataset: Dataset = self.dataset_run.dataset

        # Ensure necessary files and directories exist
        self.output_dir = Path(tempfile.mkdtemp())
        self._download_dataset()
        self._ensure_model_files()

        # Write config file
        self._write_config_file()

    def _cleanup(self):
        """Perform any necessary cleanup."""
        # Remove dirs
        # Don't remove self.model_dir, as other tasks will need it
        shutil.rmtree(self.output_dir, ignore_errors=True)

        # Remove files
        self.config_path.unlink(missing_ok=True)
        if self.point_cloud_path is not None:
            self.point_cloud_path.unlink(missing_ok=True)

    def on_failure(self, exc, task_id, args, kwargs, einfo: ExceptionInfo):
        self.dataset_run.status = DatasetRun.Status.FAILED
        self.dataset_run.output_log = einfo.traceback
        self.dataset_run.save()

        self._cleanup()

    def on_success(self, retval, task_id, args, kwargs):
        self._upload_result_files()

        # Mark dataset run as succeeded and save logs
        self.dataset_run.status = DatasetRun.Status.SUCCEEDED
        self.dataset_run.save()

        self._cleanup()

    def __call__(self, **kwargs):
        # Setup
        self._setup(**kwargs)

        # Run task
        return self.run(**kwargs)


@celery.shared_task(base=ManagedTask, bind=True)
def run_danesfield(self: ManagedTask, **kwargs):
    # Import docker here to django can import task without docker
    import docker
    from docker.errors import DockerException, ImageNotFound
    from docker.models.containers import Container
    from docker.types import DeviceRequest, Mount

    # Construct container arguments
    command = ['python', '/danesfield/tools/run_danesfield.py', str(self.config_path)]
    paths_to_mount = (self.output_dir, self.models_dir, self.config_path, self.point_cloud_path)
    mounts = [Mount(target=str(path), source=str(path), type='bind') for path in paths_to_mount]
    device_requests = [DeviceRequest(count=-1, capabilities=[['gpu']])]

    # Instantiate docker client
    client = docker.from_env()
    danesfield_image_id = 'kitware/danesfield'

    # Get or pull image
    try:
        image = client.images.get(danesfield_image_id)
    except ImageNotFound:
        # TODO: Fix logger to save all logs to output
        logger.info(f'Pulling {danesfield_image_id}. This may take a while...')
        image = client.images.pull(danesfield_image_id)

    # Run container
    try:
        container: Container = client.containers.run(
            image, command=command, mounts=mounts, device_requests=device_requests, detach=True
        )
    except DockerException as e:
        self.dataset_run.output_log = str(e)
        self.dataset_run.save()
        return e.status_code

    # Capture live logs
    self.dataset_run.output_log = ''
    output_generator = container.logs(stream=True)
    for log in output_generator:
        # TODO: Probably inefficient, fix
        self.dataset_run.output_log += log.decode('utf-8')
        self.dataset_run.save()

    # Return status code
    res = container.wait()
    return res['StatusCode']

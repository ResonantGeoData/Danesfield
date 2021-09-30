import os
from pathlib import Path
import shutil
import tempfile
from typing import List, Set

from billiard.einfo import ExceptionInfo
import celery
from django.core.files.uploadedfile import SimpleUploadedFile
from rgd.models.common import ChecksumFile

from danesfield.core.models import Dataset, DatasetRun

from .helpers import DanesfieldRunData, ensure_model_files, write_config_file


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
                new_checksum_files.append(checksum_file)

            existing_filenames.update(new_filenames)

        self.dataset_run.output_files.add(*new_checksum_files)

    def _download_dataset(self):
        """Download the dataset."""

        if not self.dataset.imageless:
            # TODO: Handle imageful case
            return

        # Imageless case
        fd, path = tempfile.mkstemp()
        self.point_cloud_path = Path(path)

        file = self.dataset.point_cloud_file.file
        with os.fdopen(fd, 'wb') as point_cloud_in:
            shutil.copyfileobj(file, point_cloud_in)
            point_cloud_in.flush()

    def _cleanup(self):
        """Perform any necessary cleanup."""
        # Remove dirs
        shutil.rmtree(self.output_dir, ignore_errors=True)
        shutil.rmtree(self.models_dir, ignore_errors=True)

        # Remove files
        self.point_cloud_path.unlink(missing_ok=True)
        self.config_path.unlink(missing_ok=True)

    def on_failure(self, exc, task_id, args, kwargs, einfo: ExceptionInfo):
        self.dataset_run.status = DatasetRun.Status.FAILED
        self.dataset_run.output_log = einfo.traceback
        self.dataset_run.save()

        self._cleanup()

    def on_success(self, retval, task_id, args, kwargs):
        self._upload_result_files()

        # Mark dataset run as succeeded and save logs
        self.dataset_run.status = DatasetRun.Status.SUCCEEDED
        self.dataset_run.output_log = retval
        self.dataset_run.save()

        # Cleanup
        self._cleanup()

    def __call__(self, **kwargs):
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
        self.models_dir = Path(ensure_model_files())
        self.output_dir = Path(tempfile.mkdtemp())
        self.config_path = Path(tempfile.mkstemp()[1])
        self._download_dataset()

        # Construct data
        data = DanesfieldRunData(
            self.dataset,
            self.dataset_run,
            self.output_dir,
            self.models_dir,
            self.point_cloud_path,
            self.config_path,
        )

        # Run task
        return self.run(data=data, **kwargs)


@celery.shared_task(base=ManagedTask)
def run_danesfield(**kwargs):
    # Import docker here to django can import task without docker
    import docker
    from docker.types import DeviceRequest, Mount

    data: DanesfieldRunData = kwargs['data']
    write_config_file(data)

    # Construct container arguments
    command = ['touch', f'{data.output_dir}/test.txt']
    paths_to_mount = (data.output_dir, data.models_dir, data.config_path, data.point_cloud_path)
    mounts = [Mount(target=str(path), source=str(path), type='bind') for path in paths_to_mount]
    device_requests = [DeviceRequest(count=-1, capabilities=[['gpu']])]

    # Instantiate docker client
    client = docker.from_env()
    output = client.containers.run(
        'alpine',
        command=command,
        mounts=mounts,
        device_requests=device_requests,
    )

    return output.decode('utf-8')

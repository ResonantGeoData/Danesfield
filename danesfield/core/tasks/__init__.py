import os
from pathlib import Path
import shutil
import tempfile

import celery

from danesfield.core.models import Dataset, DatasetRun

from .helpers import DanesfieldRunData, ensure_model_files, write_config_file


class ManagedTask(celery.Task):
    def _upload_result_files(self):
        """Upload any new files to the dataset."""
        # TODO: Scan for new files and create new files, add to dataset.

    def _download_dataset(self):
        """Download the dataset."""
        # TODO: Handle imageful case

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

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.dataset_run.status = DatasetRun.Status.FAILED
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

    data: DanesfieldRunData = kwargs['data']
    write_config_file(data)

    with open(data.config_path) as readfile:
        print(readfile.read())

    # TODO: Mount volumes

    # Instantiate docker client
    client = docker.from_env()
    output = client.containers.run('hello-world')

    return output.decode('utf-8')

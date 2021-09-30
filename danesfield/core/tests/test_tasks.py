import pathlib
from typing import List

import celery
import pytest
from rgd.models.common import ChecksumFile

from danesfield.core.models.dataset import DatasetRun
from danesfield.core.tasks import ManagedTask
from danesfield.core.tasks.helpers import DanesfieldRunData


@celery.shared_task(base=ManagedTask)
def succeeding_task(**kwargs):
    data: DanesfieldRunData = kwargs['data']

    output_dir = data.output_dir
    test_file = pathlib.Path(f'{output_dir}/test.txt')
    test_file.touch()

    with open(test_file, 'w') as outfile:
        outfile.write('Test Output')

    return 'OUTPUT!'


@celery.shared_task(base=ManagedTask)
def failing_task(**kwargs):
    raise Exception('Task failed')


@pytest.mark.django_db
def test_successful_task(dataset_run: DatasetRun):
    succeeding_task.delay(dataset_run_id=dataset_run.pk)
    dataset_run.refresh_from_db()

    assert dataset_run.status == DatasetRun.Status.SUCCEEDED
    assert dataset_run.output_log == 'OUTPUT!'

    files: List[ChecksumFile] = list(dataset_run.output_files.all())
    assert len(files) == 1
    assert files[0].name == 'test.txt'

    file = files[0]
    assert file.file.read() == b'Test Output'


@pytest.mark.django_db
def test_failed_task(dataset_run: DatasetRun):
    failing_task.delay(dataset_run_id=dataset_run.pk)
    dataset_run.refresh_from_db()

    # Assert that status is failed, and exception was caught as output
    assert dataset_run.status == DatasetRun.Status.FAILED
    assert dataset_run.output_log != ''

    files: List[ChecksumFile] = list(dataset_run.output_files.all())
    assert len(files) == 0


# TODO: Add task that tests docker run

import subprocess

from django.test import override_settings
import pytest
from rdoasis.algorithms.models import AlgorithmTask, Dataset
from rgd.models import ChecksumFile
from rgd_3d.models import Tiles3D
from rgd_fmv.models import FMV

from danesfield.core.tasks import run_telesculptor


@pytest.mark.django_db
@override_settings(
    BROKER_BACKEND='memory',
    CELERY_ALWAYS_EAGER=True,
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
)
def test_telesculptor_pipeline(dataset_factory, fmv: FMV):
    try:
        subprocess.run('nvidia-smi', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        pytest.skip('NVIDIA GPU not detected.')

    fmv_file: ChecksumFile = fmv.file
    fmv_file.name = 'test.mpg'
    fmv_file.save(update_fields=['name'])

    dataset: Dataset = dataset_factory()
    # Factory boy doesn't trigger the on_save signals correctly,
    # so set this here instead of in the factory constructor
    dataset.files.set([fmv_file])
    dataset.save()

    original_task_count = AlgorithmTask.objects.count()
    original_3d_tile_count = Tiles3D.objects.count()

    run_telesculptor(dataset.pk)

    # There should be two AlgorithmTasks at the conclusion of the run,
    # one for KWIVER/TeleSculptor and one for Danesfield
    assert AlgorithmTask.objects.count() == original_task_count + 2

    # Ensure that the TeleSculptor pipeline outputted a .las point cloud file
    telesculptor_output_dataset: Dataset = AlgorithmTask.objects.order_by('-created')[
        1
    ].output_dataset
    assert telesculptor_output_dataset.files.filter(name='pc.las').exists()

    # Ensure that the Danesfield pipeline outputted a 3D tiles dataset and
    # that it was ingested by RGD
    assert Tiles3D.objects.count() == original_3d_tile_count + 1

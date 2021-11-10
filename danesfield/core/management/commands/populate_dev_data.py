from pathlib import Path

from django.core.files import File
from django.core.files.base import ContentFile
import djclick as click
from rgd.models.common import ChecksumFile

from danesfield.core.models import Dataset, DatasetRun

TEST_DATA_DIRECTORY = (
    Path(__file__).parent.parent.parent.parent.parent.resolve()
    / 'dev'
    / 'test_data'
    / 'TilesetWithDiscreteLOD'
)

test_filenames = ['tileset.json', 'dragon_high.b3dm', 'dragon_low.b3dm', 'dragon_medium.b3dm']


@click.command()
def populate_dev_data():
    point_cloud_file = ChecksumFile.objects.create(
        name='TilesetWithDiscreteLOD.txt',
        file=ContentFile("i'm a point cloud (not really)").read(),
    )
    dataset: Dataset = Dataset.objects.create(
        name='TilesetWithDiscreteLOD',
        imageless=True,
        point_cloud_file=point_cloud_file,
    )
    dataset_run: DatasetRun = DatasetRun.objects.create(
        dataset=dataset, status=DatasetRun.Status.SUCCEEDED, output_log='test'
    )
    for filename in test_filenames:
        with open(TEST_DATA_DIRECTORY / filename, 'rb') as fd:
            dataset_run.output_files.add(
                ChecksumFile.objects.create(name=f'tiler/{filename}', file=File(fd))
            )

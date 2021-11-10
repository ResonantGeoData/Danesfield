from pathlib import Path

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import djclick as click
from rgd.models.common import ChecksumFile

from danesfield.core.models import Dataset, DatasetRun

TEST_DATA_DIRECTORY = (
    Path(__file__).parent.parent.parent.parent.parent.resolve()
    / 'dev'
    / 'sample_data'
    / 'TilesetWithDiscreteLOD'
)

test_filenames = ['tileset.json', 'dragon_high.b3dm', 'dragon_low.b3dm', 'dragon_medium.b3dm']


@click.command()
def populate_dev_data():
    if Dataset.objects.filter(name='TilesetWithDiscreteLOD').exists():
        dataset: Dataset = Dataset.objects.get(name='TilesetWithDiscreteLOD')
        click.echo(f'Dataset "TilesetWithDiscreteLOD" already exists (pk = {dataset.pk}).')
    else:
        point_cloud_file = ChecksumFile.objects.create(
            name='TilesetWithDiscreteLOD.las',
            file=SimpleUploadedFile(name='TilesetWithDiscreteLOD.las', content=b'A' * 10),
        )
        dataset: Dataset = Dataset.objects.create(
            name='TilesetWithDiscreteLOD',
            imageless=True,
            point_cloud_file=point_cloud_file,
        )
        click.echo(f'Created dataset "TilesetWithDiscreteLOD" (pk = {dataset.pk})')
    dataset_run: DatasetRun = DatasetRun.objects.create(
        dataset=dataset, status=DatasetRun.Status.SUCCEEDED, output_log='test'
    )
    click.echo(f'Created DatasetRun for Dataset {dataset.pk}.')
    for filename in test_filenames:
        with open(TEST_DATA_DIRECTORY / filename, 'rb') as fd:
            dataset_run.output_files.add(
                ChecksumFile.objects.create(name=f'tiler/{filename}', file=File(fd))
            )
            click.echo(f'  Added ChecksumFile "tiler/{filename}" to DatasetRun output.')

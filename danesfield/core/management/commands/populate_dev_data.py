from pathlib import Path

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import djclick as click
from rdoasis.algorithms.models import Algorithm, AlgorithmTask, Dataset
from rgd.models.common import ChecksumFile

from danesfield.core.utils import danesfield_algorithm

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
        dataset: Dataset = Dataset.objects.create(name='TilesetWithDiscreteLOD')
        dataset.files.add(
            ChecksumFile.objects.create(
                name='TilesetWithDiscreteLOD.las',
                file=SimpleUploadedFile(name='TilesetWithDiscreteLOD.las', content=b'A' * 10),
            )
        )

        click.echo(f'Created Dataset "TilesetWithDiscreteLOD" (pk = {dataset.pk})')

    if Dataset.objects.filter(name='TilesetWithDiscreteLOD Output').exists():
        output_dataset: Dataset = Dataset.objects.get(name='TilesetWithDiscreteLOD Output')
        click.echo(
            f'Dataset "TilesetWithDiscreteLOD Output" already exists (pk = {output_dataset.pk}).'
        )

        return

    alg: Algorithm = danesfield_algorithm()
    output_dataset = Dataset.objects.create(name='TilesetWithDiscreteLOD Output')
    alg_task: AlgorithmTask = AlgorithmTask.objects.create(
        algorithm=alg,
        status=AlgorithmTask.Status.SUCCEEDED,
        input_dataset=dataset,
        output_dataset=output_dataset,
        output_log='test',
    )
    click.echo(f'Created AlgorithmTask (pk = {alg_task.pk}) for Algorithm {alg.pk}.')

    # Populate output dataset
    for filename in test_filenames:
        with open(TEST_DATA_DIRECTORY / filename, 'rb') as fd:
            output_dataset.files.add(
                ChecksumFile.objects.create(name=f'tiler/{filename}', file=File(fd))
            )
            click.echo(f'  Added ChecksumFile "tiler/{filename}" to AlgorithmTask output dataset.')

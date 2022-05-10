from pathlib import Path

from django.core.files import File
from django.db import transaction
import djclick as click
from rdoasis.algorithms.models import Dataset
from rgd.models import ChecksumFile

from danesfield.core.tasks import _ingest_checksum_files


@click.command()
@click.argument('path', required=True, type=click.Path(exists=True))
@click.option('-n', '--name', required=True, type=str, help='The name of the imported dataset.')
@transaction.atomic
def ingest_danesfield_output(path: str, name: str):
    dataset, created = Dataset.objects.get_or_create(name=name)
    if not created:
        click.echo(f'Dataset "{name}" already exists, please use a different name.')
        return
    else:
        click.echo(f'Creating Dataset "{name}"...')
    files = []
    for p in Path(path).rglob('*'):
        if not p.is_file():
            continue
        file = p.relative_to(path)
        with open(p, 'rb') as fd:
            files.append(ChecksumFile.objects.create(name=file, file=File(fd)))
            click.echo(f'  Created ChecksumFile from file "{file}"')
    dataset.files.set(files)
    dataset.save()
    click.echo('  Ingesting files...')
    _ingest_checksum_files(dataset)
    click.echo('Done.')

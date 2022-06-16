from __future__ import annotations

from pathlib import Path

import djclick as click
from rdoasis.algorithms.models import Dataset
from rgd.models import ChecksumFile


@click.command()
@click.argument('dataset_pk', required=True, type=int)
@click.option('-p', '--path', type=str, help='Directory to save files to.')
def clone_dataset(dataset_pk: int, path: str | None):
    """Clone a Dataset's files to the given path on disk."""
    path = (
        Path(__file__).parent.parent.parent.parent.parent.resolve()
        if path is None
        else Path(path).resolve()
    )
    dataset = Dataset.objects.get(pk=dataset_pk)

    click.echo(f'Saving files from {dataset.name} to {path}...')

    file: ChecksumFile
    for file in dataset.files.all():
        file_path = path / file.name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        click.echo(f'  Saving {file_path}... ', nl=False)
        with open(file_path, 'wb') as fd:
            fd.write(file.file.read())
        click.echo(click.style('Done', fg='green'))

    click.echo(click.style(f'All {dataset.files.count()} files saved.', fg='cyan', bold=True))

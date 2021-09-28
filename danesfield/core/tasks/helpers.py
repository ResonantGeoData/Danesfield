import configparser
from dataclasses import dataclass
import tempfile

from danesfield.core.models.dataset import Dataset, DatasetRun


@dataclass
class DanesfieldRunData:
    dataset: Dataset
    dataset_run: DatasetRun
    output_dir: str
    models_dir: str
    config_path: str
    point_cloud_path: str


def ensure_model_files() -> str:
    """Return model files required for running Danesfield, creating if necessary."""
    # TODO: Implement
    return tempfile.mkdtemp()


def write_config_file(data: DanesfieldRunData) -> str:
    """Return the written config file path."""
    config = configparser.ConfigParser()
    config['paths'] = {
        'p3d_path': data.point_cloud_path,
        'work_dir': data.output_dir,
        'rpc_dir': tempfile.mkdtemp(),
    }

    config['aoi'] = {'name': data.dataset.name.replace(' ', '_')}
    config['params'] = {'gsd': 0.25}
    config['roof'] = {
        'model_dir': f'{data.models_dir}/Columbia Geon Segmentation Model',
        'model_prefix': 'dayton_geon',
    }

    # Write config to disk
    with open(data.config_path, 'w') as configfile:
        config.write(configfile)

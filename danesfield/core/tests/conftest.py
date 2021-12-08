from typing import List

from factory.django import FileField
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rgd.models.common import ChecksumFile

from .factories import DATA_DIR, ChecksumFileFactory, DatasetFactory, DatasetRunFactory, UserFactory


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticated_api_client(user) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def intermediate_output_images() -> List[ChecksumFile]:
    """Sample intermediate images the Danesfield algorithm outputs during 3D tiles generation."""
    return [
        ChecksumFileFactory(name=file_path, file=FileField(from_path=(file_path)))
        for file_path in (DATA_DIR / 'intermediate' / 'images').iterdir()
        if not file_path.is_dir()
    ]


@pytest.fixture
def intermediate_output_meshes() -> List[ChecksumFile]:
    """Sample intermediate meshes the Danesfield algorithm outputs during 3D tiles generation."""
    return [
        ChecksumFileFactory(name=file_path, file=FileField(from_path=(file_path)))
        for file_path in (DATA_DIR / 'intermediate' / 'meshes').iterdir()
        if not file_path.is_dir()
    ]


# @pytest.fixture
# def successful_dataset_run(intermediate_output_images, intermediate_output_meshes):
#     dataset_output_files: List[ChecksumFileFactory] = (
#         intermediate_output_images
#         + intermediate_output_meshes
#         + [
#             ChecksumFileFactory(
#                 name='tiler/tileset.json',
#                 file=FileField(from_path=(DATA_DIR / 'tileset.json')),
#             ),
#         ]
#     )
#     run: DatasetRun = DatasetRunFactory(
#         status=DatasetRun.Status.SUCCEEDED, output_files=dataset_output_files
#     )
#     return run


# @pytest.fixture
# def failed_dataset_run():
#     run: DatasetRun = DatasetRunFactory(status=DatasetRun.Status.FAILED)
#     return run


register(ChecksumFileFactory)
register(DatasetFactory)
register(DatasetRunFactory)
register(UserFactory)

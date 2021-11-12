from factory.django import FileField
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from danesfield.core.models import DatasetRun

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
def successful_dataset_run():
    run: DatasetRun = DatasetRunFactory(
        status=DatasetRun.Status.SUCCEEDED,
        output_files=(
            ChecksumFileFactory(
                name='tiler/tileset.json',
                file=FileField(from_path=(DATA_DIR / 'tileset.json')),
            ),
        ),
    )
    return run


@pytest.fixture
def failed_dataset_run():
    run: DatasetRun = DatasetRunFactory(status=DatasetRun.Status.FAILED)
    return run


register(ChecksumFileFactory)
register(DatasetFactory)
register(DatasetRunFactory)
register(UserFactory)

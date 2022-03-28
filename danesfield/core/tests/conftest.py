from typing import List

from factory.django import FileField
import pytest
from pytest_factoryboy import register
from rdoasis.algorithms.tests.factories import DatasetFactory
from rest_framework.test import APIClient
from rgd.models import ChecksumFile
from rgd_3d.management.commands.rgd_3d_demo import load_tiles_3d_files
from rgd_3d.models import Mesh3D, Tiles3D
from rgd_3d.tasks.jobs import task_read_3d_tiles_file
from rgd_imagery.models import Image, ImageSet, Raster

from .factories import DATA_DIR, ChecksumFileFactory, UserFactory


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticated_api_client(user) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_api_client(user_factory) -> APIClient:
    client = APIClient()
    user = user_factory(is_superuser=True)
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def sample_output_image():
    """Sample output image from the Danesfield algorithm."""
    file_path = DATA_DIR / 'images' / 'threshold_CLS.tif'
    return ChecksumFileFactory(name=file_path, file=FileField(from_path=(file_path)))


@pytest.fixture(params=['44_building_49.obj', 'building_49.ply'])
def sample_output_mesh(request):
    """Sample output mesh from the Danesfield algorithm."""
    file = str(DATA_DIR / 'meshes' / request.param)
    return ChecksumFileFactory(name=file, file=FileField(from_path=(file)))


@pytest.fixture
def sample_output_3d_tiles() -> List[ChecksumFile]:
    """Sample 3D tiles output from the Danesfield algorithm."""
    return [
        ChecksumFileFactory(name=file_path, file=FileField(from_path=(file_path)))
        for file_path in (DATA_DIR / '3d_tiles').iterdir()
        if not file_path.is_dir()
    ]


@pytest.fixture
def raster(sample_output_image):
    image = Image.objects.create(file=sample_output_image)
    image_set = ImageSet.objects.create(name=image.file.name)
    image_set.images.set([image])
    raster: Raster = Raster.objects.create(name=image.file.name, image_set=image_set)
    raster._run_tasks()
    return raster


@pytest.fixture
def mesh(sample_output_mesh):
    return Mesh3D.objects.create(file=sample_output_mesh)


@pytest.fixture
def tiles3d(sample_output_3d_tiles):
    pk = load_tiles_3d_files(['jacksonville-textured.zip'])[0]
    task_read_3d_tiles_file(pk)
    return Tiles3D.objects.get(pk=pk)


register(ChecksumFileFactory)
register(DatasetFactory)
register(UserFactory)

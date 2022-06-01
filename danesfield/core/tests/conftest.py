from __future__ import annotations

import pytest
from pytest_factoryboy import register
from rdoasis.algorithms.tests.factories import DatasetFactory
from rest_framework.test import APIClient
from rgd_3d.management.commands.rgd_3d_demo import load_mesh_3d_files, load_tiles_3d_files
from rgd_3d.models import Mesh3D, Tiles3D
from rgd_3d.tasks.jobs import task_read_3d_tiles_file
from rgd_imagery.management.commands._data_helper import load_raster_files, make_raster_dict
from rgd_imagery.models import Raster
from rgd_imagery.tasks.jobs import task_populate_raster

from .factories import ChecksumFileFactory, UserFactory


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
def raster() -> Raster:
    pk = load_raster_files([make_raster_dict(['paris_france_10.tiff'])])[0]
    task_populate_raster(pk)
    return Raster.objects.get(pk=pk)


@pytest.fixture
def mesh() -> Mesh3D:
    pk = load_mesh_3d_files(['topo.vtk'])[0]
    return Mesh3D.objects.get(pk=pk)


@pytest.fixture
def tiles3d() -> Tiles3D:
    pk = load_tiles_3d_files(['jacksonville-textured.zip'])[0]
    task_read_3d_tiles_file(pk)
    return Tiles3D.objects.get(pk=pk)


register(ChecksumFileFactory)
register(DatasetFactory)
register(UserFactory)

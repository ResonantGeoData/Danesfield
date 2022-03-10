from django.urls import reverse
import pytest
from rdoasis.algorithms.models import Dataset
from rest_framework.test import APIClient
from rgd_3d.models import Mesh3D, Tiles3D
from rgd_imagery.models import Raster, RasterMeta


@pytest.mark.django_db
def test_raster_viewer(
    dataset: Dataset,
    raster: Raster,
    admin_api_client: APIClient,
):
    dataset.files.set([image.file for image in raster.image_set.images.all()])

    resp = admin_api_client.get(f'/api/datasets/{dataset.id}/viewer/{raster.name}/')

    assert resp.status_code == 302
    assert resp.url == reverse(RasterMeta.detail_view_name, kwargs={'pk': raster.rastermeta.pk})


@pytest.mark.django_db
def test_mesh_viewer(
    dataset: Dataset,
    mesh: Mesh3D,
    admin_api_client: APIClient,
):
    dataset.files.set([mesh.file])

    resp = admin_api_client.get(f'/api/datasets/{dataset.id}/viewer/{mesh.file.name}/')

    assert resp.status_code == 302
    assert resp.url == reverse(Mesh3D.detail_view_name, kwargs={'pk': mesh.pk})


@pytest.mark.django_db
def test_3d_tiles_viewer(
    dataset: Dataset,
    tiles3d: Tiles3D,
    admin_api_client: APIClient,
):
    dataset.files.set([file for file in tiles3d.json_file.file_set.files])

    resp = admin_api_client.get(f'/api/datasets/{dataset.id}/viewer/{tiles3d.json_file.name}/')

    assert resp.status_code == 302
    assert resp.url == reverse(Tiles3D.detail_view_name, kwargs={'pk': tiles3d.pk})

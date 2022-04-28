import json

from django.contrib.gis.geos import MultiPoint, Point
from django.http import JsonResponse
import pytest
from rdoasis.algorithms.models import Dataset
from rest_framework.test import APIClient
from rgd_3d.models import Tiles3D
from rgd_imagery.models import Raster


@pytest.mark.django_db
def test_footprints(
    dataset: Dataset, raster: Raster, tiles3d: Tiles3D, admin_api_client: APIClient
):
    dataset.files.add(raster.image_set.images.first().file)
    dataset.files.add(tiles3d.json_file)

    expected_footprints = [
        json.loads(raster.rastermeta.footprint.json),
        json.loads(tiles3d.tiles3dmeta.footprint.json),
    ]

    points = [
        Point(coord[0], coord[1])
        for footprint in expected_footprints
        for coords in footprint['coordinates']
        for coord in coords
    ]

    resp: JsonResponse = admin_api_client.get('/api/datasets/footprints/')

    assert resp.status_code == 200

    footprints: dict = resp.json()

    assert footprints[str(dataset.pk)] == json.loads(MultiPoint(points).convex_hull.json)

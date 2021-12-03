from typing import List

from django.http.response import HttpResponseRedirect
import pytest
import requests
from requests.models import Response
from rest_framework.test import APIClient
from rgd.models.common import ChecksumFile
from rgd_3d.models import PointCloud
from rgd_imagery.models import Image

from danesfield.core.models.dataset import DatasetRun
from danesfield.core.tasks import _ingest_checksum_files


@pytest.mark.django_db
def test_successful_dataset_run_output_rest(
    authenticated_api_client: APIClient, successful_dataset_run: DatasetRun
):
    # Test that /output endpoint reports correct number of output files
    assert (
        successful_dataset_run.output_files.count()
        == authenticated_api_client.get(
            f'/api/datasets/{successful_dataset_run.dataset.id}/runs/'
            f'{successful_dataset_run.id}/output/'
        ).data['count']
    )

    # This endpoint should redirect to a minio presigned URL
    redirect_resp: HttpResponseRedirect = authenticated_api_client.get(
        f'/api/datasets/{successful_dataset_run.dataset.id}/runs/'
        f'{successful_dataset_run.id}/output/tiler/tileset.json/'
    )
    assert redirect_resp.status_code == 302

    # Download the file from the presigned URL
    resp: Response = requests.get(redirect_resp.url)

    # Get the same file directly from the database
    file = successful_dataset_run.output_files.first().file.open('r')

    assert resp.text == file.read().decode('utf-8')


@pytest.mark.django_db
def test_failed_dataset_run_output_rest(
    authenticated_api_client: APIClient, failed_dataset_run: DatasetRun
):
    # Test that /output endpoint reports correct number of output files
    assert (
        failed_dataset_run.output_files.count()
        == authenticated_api_client.get(
            f'/api/datasets/{failed_dataset_run.dataset.id}/runs/'
            f'{failed_dataset_run.id}/output/'
        ).data['count']
    )

    # This request should fail since no files exist
    resp: Response = authenticated_api_client.get(
        f'/api/datasets/{failed_dataset_run.dataset.id}/runs/'
        f'{failed_dataset_run.id}/output/tiler/tileset.json/'
    )

    assert resp.status_code == 404


# Set transaction=True to ensure the DB is flushed prior to this test.
# This ensures that the Images and PointClouds being tested are
# created during this test and not leftover from another.
@pytest.mark.django_db(transaction=True)
def test_intermediate_files_etl(
    successful_dataset_run: DatasetRun,
    intermediate_output_images: List[ChecksumFile],
    intermediate_output_meshes: List[ChecksumFile],
):
    """Test that relevant files from a DatasetRun are properly saved into RGD models."""
    # Call this function directly here. Normally, this is executed upon the
    # successful completion of a DatasetRun.
    _ingest_checksum_files(successful_dataset_run.output_files.all())

    for checksum_file in intermediate_output_images:
        assert Image.objects.filter(file=checksum_file).exists()

    for checksum_file in intermediate_output_meshes:
        assert PointCloud.objects.filter(file=checksum_file).exists()

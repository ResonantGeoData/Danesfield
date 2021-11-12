from django.http.response import HttpResponseRedirect
import pytest
import requests
from requests.models import Response
from rest_framework.test import APIClient

from danesfield.core.models.dataset import DatasetRun


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

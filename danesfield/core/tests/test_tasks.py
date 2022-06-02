from __future__ import annotations

import pytest
from rdoasis.algorithms.models import Dataset
from rgd_3d.models import Mesh3D, Tiles3D
from rgd_imagery.models import Raster

from danesfield.core.tasks import _ingest_checksum_files


@pytest.mark.django_db
def test_dataset_ingestion(output_dataset: Dataset):
    """Test that relevant files from an AlgorithmTask are properly saved into RGD models."""
    # Call this function directly here. Normally, this is executed upon the
    # successful completion of an AlgorithmTask.
    _ingest_checksum_files(output_dataset)

    assert Raster.objects.count() == 1
    assert Mesh3D.objects.count() == 1
    assert Tiles3D.objects.count() == 1

from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from rdoasis.algorithms.models import Dataset
from rdoasis.algorithms.views.algorithms import DatasetViewSet as BaseDatasetViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rgd.models import ChecksumFile
from rgd_3d.models import Mesh3D, Tiles3D
from rgd_imagery.models import Image, RasterMeta


class DatasetViewSet(BaseDatasetViewSet):
    @action(detail=True, methods=['GET'], url_path='viewer/(?P<path>.+)')
    def viewer(self, request: Request, pk: str, path: str):
        """Redirects to the appropriate viewer for the given file."""
        dataset: Dataset = get_object_or_404(Dataset, pk=pk)
        checksum_file: ChecksumFile = get_object_or_404(dataset.files, name=path)

        # Try Image model
        ingested_file = Image.objects.filter(file=checksum_file).first()
        if ingested_file is not None:
            raster_meta = ingested_file.imageset_set.first().raster.rastermeta
            return HttpResponseRedirect(
                reverse(RasterMeta.detail_view_name, kwargs={'pk': raster_meta.pk})
            )

        # Try Mesh3D model
        ingested_file = Mesh3D.objects.filter(file=checksum_file).first()
        if ingested_file is not None:
            return HttpResponseRedirect(
                reverse(Mesh3D.detail_view_name, kwargs={'pk': ingested_file.pk})
            )

        # Try Tiles3D model
        if checksum_file.file_set is not None:
            tileset = checksum_file.file_set.files.filter(name__endswith='tileset.json').first()
            if tileset is not None:
                ingested_file = Tiles3D.objects.filter(json_file=tileset).first()
                if ingested_file is not None:
                    return HttpResponseRedirect(
                        reverse(Tiles3D.detail_view_name, kwargs={'pk': ingested_file.pk})
                    )

        # No match found
        return HttpResponseNotFound()

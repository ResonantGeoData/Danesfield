import json

from django.contrib.gis.geos import MultiPoint, Point
from django.http import JsonResponse
from django.shortcuts import redirect
from rdoasis.algorithms.models import Dataset
from rdoasis.algorithms.views.algorithms import DatasetViewSet as BaseDatasetViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rgd_3d.models import Mesh3D, Mesh3DSpatial, Tiles3DMeta
from rgd_fmv.models import FMVMeta
from rgd_imagery.models import RasterMeta


class DatasetViewSet(BaseDatasetViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        rasters = [
            raster['pk']
            for raster in RasterMeta.objects.filter(
                parent_raster__image_set__images__file__in=instance.files.all()
            ).values('pk')
        ]
        meshes = [
            mesh['pk'] for mesh in Mesh3D.objects.filter(file__in=instance.files.all()).values('pk')
        ]
        tiles3d = [
            tiles['pk']
            for tiles in Tiles3DMeta.objects.filter(
                source__json_file__in=instance.files.all()
            ).values('pk')
        ]
        fmvs = [
            fmv['pk']
            for fmv in FMVMeta.objects.filter(fmv_file__file__in=instance.files.all()).values('pk')
        ]

        resp = serializer.data
        resp['rasters'] = rasters
        resp['meshes'] = meshes
        resp['tiles3d'] = tiles3d
        resp['fmvs'] = fmvs

        return Response(resp)

    @action(detail=True, methods=['GET'], url_path='file/(?P<name>.+)')
    def file(self, request: Request, pk: str, name: str):
        """Download a file from a 3D tiles FileSet."""
        dataset = get_object_or_404(Dataset.objects.all(), pk=pk)
        file = get_object_or_404(dataset.files.all(), name=name)
        return redirect(file.file.url, permanent=False)

    @action(detail=False, methods=['GET'])
    def footprints(self, request: Request):
        resp = {}
        for dataset in Dataset.objects.all():
            # Collect footprints of every Raster/Mesh/3D Tiles in this Dataset
            footprints = (
                [
                    json.loads(item['footprint'].json)
                    for item in RasterMeta.objects.filter(
                        parent_raster__image_set__images__file__in=dataset.files.all()
                    ).values('footprint')
                ]
                + [
                    json.loads(item['footprint'].json)
                    for item in Tiles3DMeta.objects.filter(
                        source__json_file__in=dataset.files.all()
                    ).values('footprint')
                ]
                + [
                    json.loads(item['footprint'].json)
                    for item in Mesh3DSpatial.objects.filter(
                        source__file__in=dataset.files.all()
                    ).values('footprint')
                ]
                + [
                    json.loads(item['footprint'].json)
                    for item in FMVMeta.objects.filter(
                        fmv_file__file__in=dataset.files.all()
                    ).values('footprint')
                ]
            )

            # Flatten list of polygons into list of points
            points = [
                Point(coord[0], coord[1])
                for footprint in footprints
                for coords in footprint['coordinates']
                for coord in coords
            ]

            # Compute convex hull of this dataset
            resp[dataset.pk] = json.loads(MultiPoint(points).convex_hull.json)

        return JsonResponse(resp)

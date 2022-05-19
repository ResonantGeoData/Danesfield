from drf_yasg.utils import swagger_auto_schema
from rdoasis.algorithms.models import Dataset
from rdoasis.algorithms.views.serializers import (
    AlgorithmRunSerializer,
    AlgorithmSerializer,
    AlgorithmTaskSerializer,
)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from danesfield.core.tasks import run_danesfield, run_telesculptor
from danesfield.core.utils import danesfield_algorithm

from .dataset import DatasetViewSet


class DanesfieldAlgorithmViewSet(ViewSet):
    @swagger_auto_schema(method='GET')
    @action(detail=False, methods=['GET'])
    def algorithm(self, request):
        """Return the singleton Danesfield algorithm."""
        alg = danesfield_algorithm()
        return Response(AlgorithmSerializer(alg).data)

    @swagger_auto_schema(method='POST', request_body=AlgorithmRunSerializer())
    @action(detail=False, methods=['POST'])
    def run(self, request):
        """Run the algorithm, returning the task."""
        serializer = AlgorithmRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_dataset: Dataset = get_object_or_404(
            Dataset, pk=serializer.validated_data['input_dataset']
        )

        # If the dataset contains a point cloud, run Danesfield on it
        if input_dataset.files.filter(name__endswith='.las').exists():
            task = run_danesfield(input_dataset.pk)
        # Otherwise, assume it contains an FMV that needs to be converted first,
        # and run the KWIVER/TeleSculptor pipeline
        else:
            task = run_telesculptor(input_dataset.pk)
        return Response(AlgorithmTaskSerializer(task).data)


__all__ = ['DanesfieldAlgorithmViewSet', 'DatasetViewSet']

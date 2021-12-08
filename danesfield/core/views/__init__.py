from drf_yasg.utils import swagger_auto_schema
from rdoasis.algorithms.views.serializers import AlgorithmRunSerializer, AlgorithmTaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from danesfield.core.tasks import run_danesfield


class DanesfieldAlgorithmViewSet(ViewSet):
    @swagger_auto_schema(method='POST', request_body=AlgorithmRunSerializer())
    @action(detail=False, methods=['POST'])
    def run(self, request):
        """Run the algorithm, returning the task."""
        serializer = AlgorithmRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = run_danesfield(serializer.validated_data['input_dataset'])
        return Response(AlgorithmTaskSerializer(task).data)

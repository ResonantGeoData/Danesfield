from django.utils.encoding import smart_str
from drf_yasg.utils import swagger_auto_schema
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from danesfield.core.models.dataset import Dataset, DatasetRun
from danesfield.core.views.serializers import (
    DatasetRunLogsSerializer,
    DatasetRunSerializer,
    DatasetSerializer,
)


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return smart_str(data, encoding=self.charset)


class DatasetViewSet(ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    pagination_class = LimitOffsetPagination


class DatasetRunViewSet(NestedViewSetMixin, ReadOnlyModelViewSet):
    serializer_class = DatasetRunSerializer
    pagination_class = LimitOffsetPagination
    queryset = DatasetRun.objects.all()

    @swagger_auto_schema(
        query_serializer=DatasetRunLogsSerializer(), responses={200: 'The log text.'}
    )
    @action(detail=True, methods=['GET'], renderer_classes=[PlainTextRenderer])
    def logs(self, request: Request, parent_lookup_dataset__pk: str, pk: str):
        """Return the logs from a dataset run."""
        # Fetch run
        run: DatasetRun = get_object_or_404(
            DatasetRun, dataset__pk=parent_lookup_dataset__pk, pk=pk
        )

        # Grab params
        serializer = DatasetRunLogsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        head: int = serializer.validated_data.get('head')
        tail: int = serializer.validated_data.get('tail')

        # Slice text if required
        response_text: str = run.output_log
        if head or tail:
            lines = response_text.splitlines()
            lines = lines[-tail:] if tail else lines[:head]
            response_text = '\n'.join(lines)

        return Response(response_text, content_type='text/plain')

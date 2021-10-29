from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from danesfield.core.models.dataset import Dataset, DatasetRun
from danesfield.core.views.serializers import DatasetRunSerializer, DatasetSerializer


class DatasetViewSet(ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    pagination_class = LimitOffsetPagination


class DatasetRunViewSet(NestedViewSetMixin, ReadOnlyModelViewSet):
    serializer_class = DatasetRunSerializer
    pagination_class = LimitOffsetPagination
    queryset = DatasetRun.objects.all()

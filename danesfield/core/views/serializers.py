from rest_framework import serializers


class DatasetListQueryParamsSerializer(serializers.Serializer):
    include_input_datasets = serializers.BooleanField(
        default=True, help_text='Whether or not to include input datasets.'
    )

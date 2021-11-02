from rest_framework import serializers

from danesfield.core.models import Dataset, DatasetRun


class LimitOffsetSerializer(serializers.Serializer):
    limit = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'
        read_only_fields = ['created', 'modified']

    def validate(self, data):
        imageless = data.get('imageless', True)
        if imageless and data.get('point_cloud_file') is None:
            raise serializers.ValidationError('Must specify point_cloud_file if imageless=True')

        if not imageless and not data.get('files'):
            raise serializers.ValidationError('Must specify files if imageless=False')

        return data


class DatasetRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetRun
        exclude = ['output_log', 'output_files']
        read_only_fields = ['created', 'modified']


class DatasetRunLogsSerializer(serializers.Serializer):
    """A serializer for the log action query params."""

    head = serializers.IntegerField(required=False)
    tail = serializers.IntegerField(required=False)

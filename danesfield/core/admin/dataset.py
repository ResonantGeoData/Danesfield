from django.contrib import admin
from girder_utils.admin import ReadonlyTabularInline

from danesfield.core.models import Dataset, DatasetRun


class DatasetRunInline(ReadonlyTabularInline):
    model = DatasetRun


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    inlines = [DatasetRunInline]
    list_display = ['id', 'name', 'imageless', 'point_cloud_file', 'created', 'modified']

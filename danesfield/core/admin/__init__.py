from django.contrib import admin

from .dataset import Dataset

# general admin settings
admin.site.site_header = 'Danesfield Admin'
admin.site.site_title = 'Danesfield Admin'

__all__ = ['Dataset']

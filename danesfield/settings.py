from __future__ import annotations

import os
from pathlib import Path
from typing import Type

from composed_configuration import (
    ComposedConfiguration,
    ConfigMixin,
    DevelopmentBaseConfiguration,
    HerokuProductionBaseConfiguration,
    ProductionBaseConfiguration,
    TestingBaseConfiguration,
)
from configurations import values


class GeoDjangoMixin(ConfigMixin):
    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]):
        configuration.INSTALLED_APPS += ['django.contrib.gis']
        try:
            import re

            import osgeo

            libsdir = os.path.join(
                os.path.dirname(os.path.dirname(osgeo._gdal.__file__)), 'GDAL.libs'
            )
            libs = {
                re.split(r'-|\.', name)[0]: os.path.join(libsdir, name)
                for name in os.listdir(libsdir)
            }
            configuration.GDAL_LIBRARY_PATH = libs['libgdal']
            configuration.GEOS_LIBRARY_PATH = libs['libgeos_c']
        except Exception:
            # TODO: Log that we aren't using the expected GDAL wheel?
            pass


class DanesfieldMixin(GeoDjangoMixin, ConfigMixin):
    WSGI_APPLICATION = 'danesfield.wsgi.application'
    ROOT_URLCONF = 'danesfield.urls'

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    @staticmethod
    def before_binding(configuration: ComposedConfiguration) -> None:
        # Install local apps first, to ensure any overridden resources are found first
        configuration.INSTALLED_APPS = [
            'danesfield.core.apps.CoreConfig',
        ] + configuration.INSTALLED_APPS

        # Install additional apps
        configuration.INSTALLED_APPS += ['s3_file_field', 'rgd']
        configuration.MIDDLEWARE += ['crum.CurrentRequestUserMiddleware']
        configuration.DATABASES = values.DatabaseURLValue(
            environ_name='DATABASE_URL',
            environ_prefix='DJANGO',
            environ_required=True,
            engine='django.contrib.gis.db.backends.postgis',
            conn_max_age=600,
        )


class DevelopmentConfiguration(DanesfieldMixin, DevelopmentBaseConfiguration):
    pass


class TestingConfiguration(DanesfieldMixin, TestingBaseConfiguration):
    pass


class ProductionConfiguration(DanesfieldMixin, ProductionBaseConfiguration):
    pass


class HerokuProductionConfiguration(DanesfieldMixin, HerokuProductionBaseConfiguration):
    pass

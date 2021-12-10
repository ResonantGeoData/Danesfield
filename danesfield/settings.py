from __future__ import annotations

from pathlib import Path

from composed_configuration import (
    ComposedConfiguration,
    ConfigMixin,
    DevelopmentBaseConfiguration,
    HerokuProductionBaseConfiguration,
    ProductionBaseConfiguration,
    TestingBaseConfiguration,
)
from configurations import values
from rgd.configuration import GeoDjangoMixin


class DanesfieldMixin(GeoDjangoMixin, ConfigMixin):
    WSGI_APPLICATION = 'danesfield.wsgi.application'
    ROOT_URLCONF = 'danesfield.urls'

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    @staticmethod
    def mutate_configuration(configuration: ComposedConfiguration) -> None:
        # Install local apps first, to ensure any overridden resources are found first
        configuration.INSTALLED_APPS = [
            'danesfield.core.apps.CoreConfig',
        ] + configuration.INSTALLED_APPS

        # Install additional apps
        configuration.INSTALLED_APPS += ['s3_file_field', 'rgd', 'rgd_3d', 'rgd_imagery']
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
    CELERY_TASK_ALWAYS_EAGER = True


class ProductionConfiguration(DanesfieldMixin, ProductionBaseConfiguration):
    pass


class HerokuProductionConfiguration(DanesfieldMixin, HerokuProductionBaseConfiguration):
    pass

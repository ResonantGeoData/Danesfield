from __future__ import annotations

from pathlib import Path

from composed_configuration import (
    ComposedConfiguration,
    DevelopmentBaseConfiguration,
    ProductionBaseConfiguration,
    TestingBaseConfiguration,
)
from configurations import values
from rgd.configuration import ResonantGeoDataBaseMixin


class DanesfieldMixin(ResonantGeoDataBaseMixin):
    WSGI_APPLICATION = 'danesfield.wsgi.application'
    ROOT_URLCONF = 'danesfield.urls'

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    @staticmethod
    def mutate_configuration(configuration: ComposedConfiguration) -> None:
        # Install local apps first, to ensure any overridden resources are found first
        configuration.INSTALLED_APPS = [
            'danesfield.core.apps.CoreConfig',
            'rdoasis.algorithms.apps.AlgorithmsConfig',
        ] + configuration.INSTALLED_APPS

        # Install additional apps
        configuration.INSTALLED_APPS += ['s3_file_field', 'rgd', 'rgd_3d', 'rgd_fmv', 'rgd_imagery']
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


class AWSProductionConfiguration(DanesfieldMixin, ProductionBaseConfiguration):
    # when using instance profile Secret/Access should be set to None
    AWS_S3_ACCESS_KEY_ID = None
    AWS_S3_SECRET_ACCESS_KEY = None
    # Proxy sends this header to indicate that it is a secure connection
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


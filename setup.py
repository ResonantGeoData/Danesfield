from pathlib import Path

from setuptools import find_packages, setup

readme_file = Path(__file__).parent / 'README.md'
if readme_file.exists():
    with readme_file.open() as f:
        long_description = f.read()
else:
    # When this is first installed in development Docker, README.md is not available
    long_description = ''

setup(
    name='danesfield',
    version='0.1.0',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    keywords='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
    ],
    python_requires='>=3.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'celery',
        'django>=4',
        'django-allauth',
        'django-click',
        'django-configurations[database,email]',
        'django-extensions',
        'django-filter',
        'django-oauth-toolkit',
        'django-rgd @ git+https://github.com/ResonantGeoData/ResonantGeoData@main#subdirectory=django-rgd',  # noqa
        'django-rgd-3d @ git+https://github.com/ResonantGeoData/ResonantGeoData@main#subdirectory=django-rgd-3d',  # noqa
        'django-rgd-fmv @ git+https://github.com/ResonantGeoData/ResonantGeoData@main#subdirectory=django-rgd-fmv',  # noqa
        'django-rgd-imagery @ git+https://github.com/ResonantGeoData/ResonantGeoData@main#subdirectory=django-rgd-imagery',  # noqa
        'djangorestframework',
        'drf-extensions',
        'drf-yasg',
        # Production-only
        'django-composed-configuration[prod]>=0.21.0',
        'django-s3-file-field[boto3]',
        'gunicorn',
        # Install with git
        'RD-OASIS @ git+https://github.com/ResonantGeoData/RD-OASIS@5b536ab3a9aa67a89c494a18beb3ce105c21779c',  # noqa
    ],
    dependency_links=['https://girder.github.io/large_image_wheels'],
    extras_require={
        'dev': [
            'django-composed-configuration[dev]>=0.21.0',
            'django-debug-toolbar',
            'django-s3-file-field[minio]',
            'ipython',
            'rasterio',
            'tox',
        ],
        'worker': [
            'docker',
        ],
    },
)

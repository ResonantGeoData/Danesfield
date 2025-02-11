# Danesfield

## Develop with Docker (recommended quickstart)
This is the simplest configuration for developers to start with.

### Initial Setup
1. Run `docker-compose run --rm django ./manage.py migrate`
2. Run `docker-compose run --rm django ./manage.py createsuperuser`
   and follow the prompts to create your own user
3. Create a virtual environment and run `pip install --find-links https://girder.github.io/large_image_wheels -e .[worker]` inside of it.

### Run Application
**Note**: Even though most of the application will be run with `docker-compose`, the `celery` worker must still be run natively, as it itself makes use of `docker`.

To run the application, do the following:
1. Run `docker-compose up`
2. In a seperate window, activate the virtual environment created previously in "Initial Setup" and run the following commands:
   1. `source ./dev/export-env.sh`
   2. `celery --app danesfield.celery worker --loglevel INFO --heartbeat-interval 60`
3. Access the site, starting at http://localhost:8000/admin/
4. When finished, use `Ctrl+C`

### Application Maintenance
Occasionally, new package dependencies or schema changes will necessitate
maintenance. To non-destructively update your development stack at any time:
1. Run `docker-compose pull`
2. Run `docker-compose build --pull --no-cache`
3. Run `docker-compose run --rm django ./manage.py migrate`

## Develop Natively (advanced)
This configuration still uses Docker to run attached services in the background,
but allows developers to run Python code on their native system.

### Initial Setup
1. Run `docker-compose -f ./docker-compose.yml up -d`
2. Install Python 3.8
3. Install
   [`psycopg2` build prerequisites](https://www.psycopg.org/docs/install.html#build-prerequisites)
4. Create and activate a new Python virtualenv
5. Run `pip install -e .[dev]`
6. Run `source ./dev/export-env.sh`
7. Run `./manage.py migrate`
8. Run `./manage.py createsuperuser` and follow the prompts to create your own user

### Run Application
1.  Ensure `docker-compose -f ./docker-compose.yml up -d` is still active
2. Run:
   1. `source ./dev/export-env.sh`
   2. `./manage.py runserver`
3. Run in a separate terminal:
   1. `source ./dev/export-env.sh`
   2. `celery --app danesfield.celery worker --loglevel INFO --heartbeat-interval 60`
4. Run in a seperate terminal:
   1. `cd client/`
   2. `yarn`
   3. `yarn run serve`
5. When finished, run `docker-compose stop`

## Remap Service Ports (optional)
Attached services may be exposed to the host system via alternative ports. Developers who work
on multiple software projects concurrently may find this helpful to avoid port conflicts.

To do so, before running any `docker-compose` commands, set any of the environment variables:
* `DOCKER_POSTGRES_PORT`
* `DOCKER_RABBITMQ_PORT`
* `DOCKER_MINIO_PORT`

The Django server must be informed about the changes:
* When running the "Develop with Docker" configuration, override the environment variables:
  * `DJANGO_MINIO_STORAGE_MEDIA_URL`, using the port from `DOCKER_MINIO_PORT`.
* When running the "Develop Natively" configuration, override the environment variables:
  * `DJANGO_DATABASE_URL`, using the port from `DOCKER_POSTGRES_PORT`
  * `DJANGO_CELERY_BROKER_URL`, using the port from `DOCKER_RABBITMQ_PORT`
  * `DJANGO_MINIO_STORAGE_ENDPOINT`, using the port from `DOCKER_MINIO_PORT`

Since most of Django's environment variables contain additional content, use the values from
the appropriate `dev/.env.docker-compose*` file as a baseline for overrides.

## Testing
### Initial Setup
tox is used to execute all tests.
tox is installed automatically with the `dev` package extra.

When running the "Develop with Docker" configuration, all tox commands must be run as
`docker-compose run --rm django tox`; extra arguments may also be appended to this form.

### Running Tests
Run `tox` to launch the full test suite.

Individual test environments may be selectively run.
This also allows additional options to be be added.
Useful sub-commands include:
* `tox -e lint`: Run only the style checks
* `tox -e type`: Run only the type checks
* `tox -e test`: Run only the pytest-driven tests

To automatically reformat all code to comply with
some (but not all) of the style checks, run `tox -e format`.


### Developer Scripts

The following Django management scripts can be executed using `./manage.py <name_of_script>`.

To view help text for any of them, run with the `--help` flag.


### populate_dev_data

Populates the database with a sample dataset as well as 3D tile output from a successful run on that dataset.


### create_oauth_application

Creates a `django-oauth-toolkit` `Application` so the Vue SPA can login.


### ingest_danesfield_output

Takes as input a path to a directory. The directory is ingested as a `Dataset`, with every file in the directory
added recursively as a `ChecksumFile`. Any "special" file types such as rasters, meshes, 3d tiles, or FMVs are
automatically ingested as their corresponding RGD models.

## Management Scripts

The following scripts can be executed using `./manage.py <name_of_script>`.

To view help text for any of them, run with the `--help` flag.


### populate_dev_data

Populates the database with a sample dataset as well as 3D tile output from a successful run on that dataset.


### create_oauth_application

Creates a `django-oauth-toolkit` `Application` so the Vue SPA can login.


### ingest_danesfield_output

Takes as input a path to a directory. The directory is ingested as a `Dataset`, with every file in the directory
added recursively as a `ChecksumFile`. Any "special" file types such as rasters, meshes, 3d tiles, or FMVs are
automatically ingested as their corresponding RGD models.

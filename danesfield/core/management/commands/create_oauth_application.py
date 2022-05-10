from django.contrib.auth.models import User
import djclick as click
from oauth2_provider.models import Application

CLIENT_ID = 'HaPTjtIdra5x0OJfaS6pSFyqmFjQDyqoWBaScumi'


# create django oauth toolkit appliction (client)
@click.option(
    '--username',
    type=str,
    required=False,
    help='Superuser username for application creator. Defaults to oldest user if not specified.',
)
@click.option(
    '--uri',
    type=str,
    required=True,
    help='Comma-separated list of redirect uris for the application',
)
@click.command()
def command(username: str, uri: str):
    if Application.objects.filter(client_id=CLIENT_ID).exists():
        click.echo('The client already exists. You can administer it from the admin console.')
        return

    if username:
        user: User = User.objects.get(username=username)
    else:
        # If a username wasn't provided, use the first user created in the system
        user: User = User.objects.latest('-date_joined')

    Application.objects.create(
        name='danesfield-oauth-client',
        client_id=CLIENT_ID,
        client_secret='',
        client_type='public',
        redirect_uris=uri,
        authorization_grant_type='authorization-code',
        user_id=user.id,
        skip_authorization=True,
    )

    click.echo('OAuth application successfully created.')

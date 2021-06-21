import os

import click


os.environ["THINGS_USERS_DATABASE_URL"] = ""
os.environ["THINGS_USERS_SECRET_KEY"] = "robocop"


from thingsusers import application  # noqa
from thingsusers import settings  # noqa
from thingsusers.users import models  # noqa
from thingsusers import database  # noqa


@click.command("access-token")
def access_token():
    """Create a dummy access token."""
    app = application.create_app(settings.TestConfig)
    app_context = app.test_request_context()
    app_context.push()
    with app.app_context():
        database.db.create_all()
        secret = "robocop"
        app.config["JWT_SECRET_KEY"] = secret
        user = models.User("robocop@robocop.com", "alexmurphy", "robocop")
        token = user.access_token(expires_delta=False)
        click.echo(f"Token: {token}")
        click.echo(f"Secret: {secret}")

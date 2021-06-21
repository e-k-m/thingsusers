# FIXME: clean up code side affecting

import os
import unittest

os.environ["THINGS_USERS_DATABASE"] = ""
os.environ["THINGS_USERS_SECRET"] = "robocop"


from thingsusers import application  # noqa
from thingsusers import database  # noqa
from thingsusers import settings  # noqa
from thingsusers.users import models as users_models  # noqa


PASSWORD = "password"


class TestFixure(unittest.TestCase):
    def load_users(self):
        res = []
        for i in range(10):
            e = users_models.User(
                email=f"{i}@{i}.com",
                username=f"{i} username",
                password=PASSWORD,
            )
            e.save()
            res.append(e)
        self.should_user = res[0]

    def setUp(self):
        self.app = application.create_app(settings.TestConfig)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        with self.app.app_context():
            database.db.create_all()

        self.load_users()

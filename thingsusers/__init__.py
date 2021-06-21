# FIXME: Review if openapi test really fully do what they should.
# FIXME: Maybe remove the commands again.

from flask import helpers

from thingsusers import application
from thingsusers import settings
from thingsusers import version

__author__ = "Eric Matti"
__version__ = version.__version__

config = (
    settings.DevConfig if helpers.get_debug_flag() else settings.ProdConfig
)
app = application.create_app(config)

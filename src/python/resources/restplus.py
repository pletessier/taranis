# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.

import logging

from flask_restplus import Api

from utils.configuration import CONFIGURATION as config

LOGGER = logging.getLogger(__name__)

API = Api(version=config.get("swagger.version"),
          title=config.get("swagger.title"),
          description=config.get("swagger.description"))

NSDB = API.namespace('db', description='Everything about databases')


@API.errorhandler
def default_error_handler(ex):
    message = 'An unhandled exception occurred.'
    LOGGER.exception(message)
    return {'message': message}, 500

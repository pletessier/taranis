# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.

import logging

from flask_restplus import Api

from utils.configuration import configuration as config

log = logging.getLogger(__name__)

api = Api(version=config.get("swagger.version"),
          title=config.get("swagger.title"),
          description=config.get("swagger.description"))

ns_db = api.namespace('db', description='Everything about databases')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    if not True:
        return {'message': message}, 500

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from dynaconf import settings
from flask_restplus import Api

log = logging.getLogger(__name__)

api = Api(version=settings.SWAGGER.version,
          title=settings.SWAGGER.title,
          description=settings.SWAGGER.description)

ns_db = api.namespace('db', description='Everything about databases')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    if not True:
        return {'message': message}, 500

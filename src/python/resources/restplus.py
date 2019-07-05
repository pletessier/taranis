#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

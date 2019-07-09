# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.
"""
Health API resource
"""
import logging

from flask_restplus import Resource

from resources.restplus import API

LOGGER = logging.getLogger(__name__)
NS = API.namespace('health', description='health resource')


@NS.route('/')
@NS.response(404, 'health')
class HealthResource(Resource):
    '''
    In charge to handle health resource
    '''

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    def get(self):
        return {
            "status": "UP",
            "message": "This feature is not implemented: always return UP..."
        }

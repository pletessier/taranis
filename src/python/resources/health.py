# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.

import logging

from flask_restplus import Resource

from src.python.resources.restplus import api

logger = logging.getLogger(__name__)
ns = api.namespace('health', description='health resource')


@ns.route('/')
@ns.response(404, 'health')
class HealthResource(Resource):
    '''
    In charge to handle health resource
    '''

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    def get(self):
        return {
            "status": "UP"
        }

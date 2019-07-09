# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.

import logging

import prometheus_client
from flask import Response
from flask_restplus import Resource

from resources.restplus import API

LOGGER = logging.getLogger(__name__)
NS = API.namespace('metrics', description='metrics resource')


@NS.route('/')
@NS.response(404, 'metrics')
class MetricsResource(Resource):
    '''
    In charge to handle metrics resource
    '''

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    def get(self):
        return Response(prometheus_client.generate_latest(), mimetype=prometheus_client.CONTENT_TYPE_LATEST)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask import Response
from flask_restplus import Resource
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from src.python.api.restplus import api

logger = logging.getLogger(__name__)
ns = api.namespace('metrics', description='metrics resource')


@ns.route('/')
@ns.response(404, 'metrics')
class MetricsResource(Resource):
    '''
    In charge to handle metrics resource
    '''

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    def get(self):
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

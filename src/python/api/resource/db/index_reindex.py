#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask_restplus import Resource, abort
from flask_restplus._http import HTTPStatus

from api.model.IndexModelApiModel import IndexModelApiModel
from service.taranis_service import TaranisService
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/index/<string:index_name>/reindex')
class IndexModelResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.db_service = TaranisService()

    @ns_db.doc('post_reindex')
    @ns_db.response(HTTPStatus.OK, 'Index is reindexed')
    @ns_db.response(HTTPStatus.NOT_FOUND, 'Index not found')
    @ns_db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def post(self, db_name, index_name):
        """Reindex the vectors in database"""
        self.db_service.reindex(db_name, index_name)


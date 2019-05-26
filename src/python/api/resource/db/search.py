#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask import request
from flask_restplus import Resource
from flask_restplus._http import HTTPStatus

from api.model.VectorApiModel import VectorModel, VectorDataModel, VectorDataListModel
from service.taranis_service import TaranisService
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/search')
class SearchResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.db_service = TaranisService()

    @ns_db.doc('search')
    @ns_db.expect(VectorDataListModel)
    # @api.doc(model='VectorDataListModel', body=VectorDataListModel, as_list=True)
    @ns_db.param(name="index", description="Name of the index")
    @ns_db.param(name="k", description="Number of KNN", type=int)
    @ns_db.param(name="n_probe", description="Number of probes", type=int)
    @api.marshal_with(VectorDataListModel, as_list=True, code=HTTPStatus.OK)
    @ns_db.response(HTTPStatus.NOT_FOUND, 'Database not found')
    @ns_db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def post(self, db_name):
        """Search a vector in the database"""
        index = request.args.get('index')
        k = request.args.get('k', default=100, type=int)
        n_probe = request.args.get('n_probe', default=4, type=int)

        queries = api.payload["vectors"]
        self.db_service.search(db_name, queries, index=index, k=k, n_probe=n_probe)

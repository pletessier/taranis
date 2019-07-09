# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.


import logging
import time
from concurrent import futures
from threading import Thread

import grpc

from errors.TaranisError import *
from models.taranis_pb2 import DatabaseNameModel, NewDatabaseModel, SearchRequestModel, VectorsQueryModel, \
    NewVectorsModel, IndexQueryModel, NewIndexModel
from models.taranis_pb2_grpc import TaranisServicer, add_TaranisServicer_to_server
from services.taranis_service import TaranisService

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

logger = logging.getLogger("Taranis")


class Taranis(TaranisServicer):

    def __init__(self, taranis_service: TaranisService):
        self.taranis_service = taranis_service

    def getDatabase(self, request: DatabaseNameModel, context):
        try:
            return self.taranis_service.get_database(request.name)
        except TaranisNotFoundError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, e.message)

    def createDatabase(self, request: NewDatabaseModel, context):
        try:
            return self.taranis_service.create_database(request)
        except TaranisAlreadyExistsError as e:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, e.message)

    def deleteDatabase(self, request: DatabaseNameModel, context):
        try:
            return self.taranis_service.delete_database(request.name)
        except TaranisNotFoundError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, e.message)
        except TaranisError as e:
            context.abort(grpc.StatusCode.INTERNAL, e.message)

    def getIndex(self, request: IndexQueryModel, context):
        try:
            return self.taranis_service.get_index(request.db_name, request.index_name)
        except TaranisNotFoundError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, e.message)
        except TaranisError as e:
            context.abort(grpc.StatusCode.INTERNAL, e.message)

    def deleteIndex(self, request: IndexQueryModel, context):
        try:
            return self.taranis_service.delete_index(request.db_name, request.index_name)
        except TaranisNotFoundError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, e.message)
        except TaranisError as e:
            context.abort(grpc.StatusCode.INTERNAL, e.message)

    def createIndex(self, request: NewIndexModel, context):
        try:
            return self.taranis_service.create_index(request)
        except TaranisAlreadyExistsError as e:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, e.message)

    def trainIndex(self, request: IndexQueryModel, context):
        try:
            return self.taranis_service.train_index(request.db_name, request.index_name)
        except TaranisError as e:
            context.abort(grpc.StatusCode.INTERNAL, e.message)

    def reindex(self, request: IndexQueryModel, context):
        try:
            return self.taranis_service.reindex(request.db_name, request.index_name)
        except TaranisError as e:
            context.abort(grpc.StatusCode.INTERNAL, e.message)

    def addVectors(self, request: NewVectorsModel, context):
        try:
            return self.taranis_service.put_vectors(request.db_name, request.vectors, index=request.index_name)
        except TaranisNotFoundError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, e.message)
        except TaranisError as e:
            context.abort(grpc.StatusCode.INTERNAL, e.message)

    def getVectors(self, request: VectorsQueryModel, context):
        return self.taranis_service.get_vectors(request.db_name, request.ids)

    def searchVectors(self, request: SearchRequestModel, context):

        return self.taranis_service.search(request.db_name, list(request.vectors), index_name=request.index_name, k=request.k, n_probe=request.n_probe)


class GRPCServer(Thread):

    def __init__(self, taranis_service, listen_address='[::]', listen_port=50051, max_workers=10):
        Thread.__init__(self)
        self.listen_address = listen_address
        self.listen_port = listen_port
        self.max_workers = max_workers
        self.taranis_service = taranis_service

    def run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.max_workers))
        add_TaranisServicer_to_server(Taranis(self.taranis_service), server)
        server_listen = '{}:{}'.format(self.listen_address, self.listen_port)
        server.add_insecure_port(server_listen)
        logger.info("Starting gRPC server on {}".format(server_listen))
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt")
            server.stop(0)


# if __name__ == '__main__':
#     logging.basicConfig()
#     serve()

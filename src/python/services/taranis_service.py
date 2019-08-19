# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.

"""
Taranis Service
"""
import json
import logging
from datetime import datetime

import cpp_taranis
import numpy as np
from google.protobuf.json_format import ParseDict, MessageToDict
from pymongo.errors import DuplicateKeyError

from errors.taranis_error import TaranisError, TaranisNotFoundError, TaranisNotImplementedError, \
    TaranisAlreadyExistsError
from repositories.mongo_db_repository import MongoDBDatabaseRepository
from taranis_pb2 import NewDatabaseModel, DatabaseModel, Empty, IndexModel, NewIndexModel, VectorsReplyModel, \
    SearchResultListModel, SearchResultModel
from utils.singleton import Singleton


class TaranisService(metaclass=Singleton):
    # instance = None
    #
    # def __new__(cls, *args, **kargs):
    #     if cls.instance is None:
    #         cls.instance = object.__new__(cls, *args, **kargs)
    #     return cls.instance

    def __init__(self, mongo_host=None, mongo_port=None, mongo_username=None, mongo_password=None,
                 redis_host="localhost", redis_port=6379, redis_timeout_msecs=3000,
                 redis_max_reconnects=10, redis_reconnect_interval_msecs=1000):

        logging.info("__init__ TaranisService")

        self.repo = MongoDBDatabaseRepository(host=mongo_host, port=mongo_port, username=mongo_username,
                                              password=mongo_password)

        self.faiss_wrapper = cpp_taranis.FaissWrapper(redis_host, redis_port, redis_timeout_msecs, redis_max_reconnects,
                                                      redis_reconnect_interval_msecs)

    # def list_database(self):
    #     return self.repo.get_all_databases()

    def create_database(self, database: NewDatabaseModel):

        t = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
        new_db = dict(name=database.name, created_at=t, updated_at=t, size=0)
        res = self.repo.create_one_database(new_db)
        # TODO Check result
        return ParseDict(new_db, DatabaseModel(), ignore_unknown_fields=True)

    def get_database(self, db_name):
        database = self.repo.find_one_database_by_name(db_name)
        if database is None:
            raise TaranisNotFoundError("Database {} not found".format(db_name))
        return ParseDict(database, DatabaseModel(), ignore_unknown_fields=True)

    def delete_database(self, db_name: str):
        res = self.repo.delete_one_database_by_name(db_name)
        if not res:
            raise TaranisNotFoundError("Database {} not found".format(db_name))
        res = self.repo.delete_vectors_by_database_name(db_name)
        if not res:
            raise TaranisError("Error while deleting vectors associated with database {}".format(db_name))
        return Empty()

    def get_vectors(self, db_name, ids):

        reply = VectorsReplyModel()

        vectors_from_db = self.repo.get_vectors(db_name, list(ids))
        for vdb in vectors_from_db:
            v = reply.vectors.add()
            v.id = vdb["id"]
            v.data = vdb["data"]
            v.metadata = json.dumps(vdb["metadata"])
        return reply

    def put_vectors(self, db_name, vectors, index=None):

        vectors_to_add = []

        for v in vectors:
            v_to_add = dict(id=v.id,
                            db_name=db_name,
                            data=np.frombuffer(v.data, dtype=np.float32).tobytes(),
                            metadata=json.loads(v.metadata))
            # v_to_add["db_name"] = db_name
            # v_to_add["data"] = np.frombuffer(v.data, dtype=np.float32).tobytes()
            # v_to_add["metadata"] = json.loads(v.metadata)
            # # Convert string data to bytes
            # buf = struct.pack('f' * len(v["data"]), *v["data"])
            # v["data"] = buf
            vectors_to_add.append(v_to_add)

        res = self.repo.create_vectors(vectors_to_add)
        if not res:
            raise TaranisError("Can't add these vectors in database")

        return Empty()

    def create_index(self, index: NewIndexModel):
        try:
            t = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)

            new_index = IndexModel()
            new_index.created_at = t
            new_index.updated_at = t
            new_index.state = IndexModel.State.CREATED

            new_dict_index = MessageToDict(ParseDict(MessageToDict(index, preserving_proto_field_name=True), new_index),
                                           preserving_proto_field_name=True)

            res = self.repo.create_one_index(new_dict_index)

            config = json.loads(index.config)

            if config["index_type"] == "IVFPQ":
                dimension = config["dimension"]
                n_list = config["n_list"]
                n_probes = config["n_probes"]
                index_type = "IVF{},PQ{}np".format(n_list, n_probes)

                metric_type = cpp_taranis.Faiss.MetricType.METRIC_L2
                if config["metric"] == "METRIC_L1":
                    metric_type = cpp_taranis.Faiss.MetricType.METRIC_L1
                elif config["metric"] == "METRIC_L2":
                    metric_type = cpp_taranis.Faiss.MetricType.METRIC_L2

                self.faiss_wrapper.create_index(index.db_name, index.index_name, dimension, index_type, metric_type,
                                                n_probes)
            else:
                raise TaranisNotImplementedError(
                    "Can't create index because of unknown index type {}".format(index.config["index_type"]))
        except DuplicateKeyError as e:
            raise TaranisAlreadyExistsError("Index name {} already exists".format(index.index_name))
        return index

    def delete_index(self, db_name, index_name):
        index = IndexModel(db_name=db_name, index_name=index_name)
        res = self.repo.delete_one_index(index)
        self.faiss_wrapper.delete_index(db_name, index_name)
        return Empty()

    def get_index(self, db_name, index_name):
        index = self.faiss_wrapper.get_index(db_name, index_name)
        if index is None:
            raise TaranisNotFoundError("Can't find index {} for database {}".format(index_name, db_name))
        res = self.repo.find_one_index_by_index_name_and_db_name(index_name, db_name)
        if res is None:
            raise TaranisNotFoundError("Can't find index {} for database {}".format(index_name, db_name))
        return ParseDict(res, IndexModel(), ignore_unknown_fields=True)

    def train_index(self, db_name, index_name):
        logging.info("start train_index")
        logging.info("start find_vectors_by_database_name")
        vectors, count, ids = self.repo.find_vectors_by_database_name(db_name, limit=1000000, skip=0)
        logging.info("end find_vectors_by_database_name")
        logging.info("start faiss_wrapper.train_model with " + str(count) + " vectors")
        self.faiss_wrapper.train_model(db_name, index_name, count, vectors)
        logging.info("end faiss_wrapper.train_model")
        return Empty()

    # @profile
    def reindex(self, db_name, index_name):

        self.faiss_wrapper.clear_index(db_name, index_name)

        n_processed = 0
        while True:
            vectors, count, ids = self.repo.find_vectors_by_database_name(db_name, limit=10000, skip=n_processed)
            if not count > 0:
                break
            n_processed += count
            print("Found {} vectors to index".format(count))
            self.faiss_wrapper.encode_vectors(db_name, index_name, count, vectors, ids)
        return Empty()

    def search(self, db_name, queries, index_name=None, k: int = 100, n_probe: int = 4):
        if index_name is None:
            raise TaranisNotImplementedError(
                "Searching in all indices is not supported yet, please provide an index name")

        query_count = len(queries)
        dimension = np.frombuffer(queries[0], dtype=np.float32).shape[0]
        raw_queries = np.empty((query_count, dimension), dtype=np.dtype('Float32'))

        i = 0
        for q in queries:
            v = np.frombuffer(q, dtype=np.float32)
            raw_queries[i, :] = v
            i += 1

        faiss_result = self.faiss_wrapper.search_vectors(db_name, index_name, raw_queries, k, n_probe)

        result_list = SearchResultListModel()

        # for i in range(0, 10):
        #     dists = [float(0.0)] * k
        #     knn = [0] * k
        #     res: SearchResultModel = result_list.results.add()
        #     res.dists.extend(dists)
        #     res.knn.extend(knn)

        for dists, knn in zip(faiss_result.dists, faiss_result.knns):
            res: SearchResultModel = result_list.results.add()
            res.dists.extend(dists)
            res.knn.extend(knn)

        return result_list

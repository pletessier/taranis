import ctypes
import struct
from datetime import datetime

from bson import Binary
from pymongo.errors import DuplicateKeyError
from werkzeug.exceptions import Conflict, NotFound, InternalServerError

from api.model.DatabaseModel import DatabaseModel
from api.model.IndexModel import IndexModel
from repository.mongo_db_repository import MongoDBDatabaseRepository
import cpp_taranis


class TaranisService(object):
    instance = None

    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kargs)
        return cls.instance

    def __init__(self):
        # TODO Set Database type and params from config
        self.repo = MongoDBDatabaseRepository()

        redis_host = "localhost"
        redis_port = 6379
        timeout_msecs = 3000
        max_reconnects = 10
        reconnect_interval_msecs = 1000

        self.faiss_wrapper = cpp_taranis.FaissWrapper(redis_host, redis_port, timeout_msecs, max_reconnects,
                                                      reconnect_interval_msecs)

    def list_database(self):
        return self.repo.get_all_databases()

    def create_database(self, database: DatabaseModel):
        try:
            database.created_at = datetime.now()
            database.updated_at = database.created_at
            database.size = 0
            res = self.repo.create_one_database(database)
            # TODO Check result
        except DuplicateKeyError as e:
            raise Conflict("Database name {} already exists".format(database.name))
        return database

    def get_database(self, db_name):
        database = self.repo.find_one_database_by_name(db_name)
        if database is None:
            raise NotFound("Database {} not found".format(db_name))
        return database

    def delete_database(self, db_name: str):
        res = self.repo.delete_one_database_by_name(db_name)
        if not res:
            raise NotFound("Database {} not found".format(db_name))
        res = self.repo.delete_vectors_by_database_name(db_name)
        if not res:
            raise InternalServerError("Error while deleting vectors associated with database {}".format(db_name))

    def put_vectors(self, db_name, vectors, index=None):
        for v in vectors:
            v["db"] = db_name
            # Convert string data to bytes
            buf = struct.pack('f' * len(v["data"]), *v["data"])
            v["data"] = buf

        res = self.repo.create_vectors(vectors)
        if not res:
            raise InternalServerError("Can't add these vectors in database")

    def create_index(self, db_name, index: IndexModel):
        try:
            index.db_name = db_name
            index.created_at = datetime.now()
            index.updated_at = index.created_at
            index.size = 0
            index.state = IndexModel.States.CREATED.value
            res = self.repo.create_one_index(index)

            if index.config["index_type"] == "IVFPQ":
                dimension = index.config["dimension"]
                n_list = index.config["n_list"]
                n_probes = index.config["n_probes"]
                index_type = "IVF{},PQ{}np".format(n_list, n_probes)

                metric_type = cpp_taranis.Faiss.MetricType.METRIC_L2
                if index.config["metric"] == "METRIC_L1":
                    metric_type = cpp_taranis.Faiss.MetricType.METRIC_L1
                elif index.config["metric"] == "METRIC_L2":
                    metric_type = cpp_taranis.Faiss.MetricType.METRIC_L2

                self.faiss_wrapper.create_index(db_name, index.name, dimension, index_type, metric_type, n_probes)
            else:
                raise InternalServerError(
                    "Can't create index because of unknown index type {}".format(index.config["index_type"]))
        except DuplicateKeyError as e:
            raise Conflict("Index name {} already exists".format(index.name))
        return index

    def delete_index(self, db_name, index_name):
        index = IndexModel(db_name=db_name, name=index_name)
        res = self.repo.delete_one_index(index)

    def get_index(self, db_name, index_name):
        self.faiss_wrapper.get_index(db_name, index_name)
        res = self.repo.find_one_index_by_index_name_and_db_name(index_name, db_name)
        return res

    def train_index(self, db_name, index_name):
        vectors, count = self.repo.find_vectors_by_database_name(db_name)
        self.faiss_wrapper.train_model(db_name, index_name, count, vectors)

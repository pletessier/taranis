from datetime import datetime

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

            dimension = 64
            n_list = 32
            n_probes = 4
            index_type = "IVF{},PQ{}np".format(n_list, n_probes)
            metric_type = cpp_taranis.Faiss.MetricType.METRIC_L2

            cpp_taranis.create_index(dimension, index_type, metric_type, n_probes)

        except DuplicateKeyError as e:
            raise Conflict("Index name {} already exists".format(index.name))
        return index

    def delete_index(self, db_name, index_name):

        index = IndexModel(db_name=db_name, name=index_name)
        res = self.repo.delete_one_index(index)

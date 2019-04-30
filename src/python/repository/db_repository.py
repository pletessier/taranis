from abc import ABC, abstractmethod

from api.model.DatabaseModel import DatabaseModel
from api.model.IndexModel import IndexModel


class AbstractDatabaseRepository(ABC):
    instance = None

    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kargs)
        return cls.instance

    @abstractmethod
    def get_all_databases(self) -> list:
        pass

    @abstractmethod
    def create_one_database(self, database: DatabaseModel) -> str:
        pass

    @abstractmethod
    def find_one_database_by_name(self, name: str) -> dict:
        pass

    @abstractmethod
    def delete_one_database_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def delete_vectors_by_database_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def create_vectors(self, vectors: []) -> bool:
        pass

    @abstractmethod
    def create_one_index(self, index: IndexModel) -> str:
        pass

    @abstractmethod
    def delete_one_index(self, index: IndexModel) -> bool:
        pass
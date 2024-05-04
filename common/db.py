import asyncpg
from pydantic import BaseModel
import yaml


class DBException(Exception):
    pass


class UnknownDatabaseError(DBException):
    pass


class Database(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str


class DatabaseConnection:
    _databases: dict[str, Database] = {}
    _connections: dict[str, asyncpg.Connection] = {}

    @classmethod
    async def get_connection(cls, db_name: str) -> asyncpg.Connection:
        if db_name not in cls._databases:
            # TODO: Load from environment variables
            cls._load_from_yaml("social_network/config/service.yaml")
        if db_name not in cls._databases:
            raise UnknownDatabaseError(db_name)
        connection = await cls._get_connection(cls._databases[db_name])
        return connection

    @classmethod
    def _load_from_yaml(cls, file_path: str):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        for db_name, db_info in data["databases"].items():
            cls._databases[db_name] = Database(**db_info)

    @classmethod
    async def _get_connection(cls, db: Database) -> asyncpg.Connection:
        return await asyncpg.connect(
                user=db.username,
                password=db.password,
                database=db.database,
                host=db.host,
                port=db.port,
            )

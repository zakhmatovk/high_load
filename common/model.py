import datetime
import json
from typing import Any, ClassVar, Self
from pydantic import BaseModel
from common.db import DatabaseConnection


class DBException(Exception):
    pass


class InsertWasFailedException(DBException):
    pass


class RowNotFoundException(DBException):
    def __init__(self, pk, *args):
        super().__init__(*args)
        self.pk = pk

    def __str__(self):
        return f"No record found with id {self.pk}"


class BasePgModel(BaseModel):
    __database__: ClassVar[str] = "social_network"  # TODO: replace with test db
    __table__: ClassVar[str]

    async def insert(self) -> Self:
        _fields: list[str] = []
        _values: list[str] = []
        _data: list[Any] = []
        model_dump = self.model_dump()

        for i, field in enumerate(self.model_fields):
            _fields.append(field)
            _values.append(f"${i+1}")

            value = model_dump.get(field)
            if isinstance(value, dict):
                value = json.dumps(value)
            _data.append(value)

        fields: str = ", ".join(_fields)
        values: str = ", ".join(_values)
        query = f"INSERT INTO {self.__table__} ({fields}) VALUES ({values}) RETURNING *"

        connection = await DatabaseConnection.get_connection(db_name=self.__database__)
        try:
            row = await connection.fetchrow(query, *_data)
            if not row:
                raise InsertWasFailedException()
            return type(self)(**row)
        finally:
            await connection.close()

    @classmethod
    async def load(cls, pk) -> Self:
        query = f"SELECT * FROM {cls.__table__} WHERE id = $1"
        connection = await DatabaseConnection.get_connection(db_name=cls.__database__)

        try:
            row = await connection.fetchrow(query, pk)
            if not row:
                raise RowNotFoundException(pk=pk)
            return cls(**row)
        finally:
            await connection.close()

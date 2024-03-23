import datetime
from typing import Any
from pydantic import BaseModel
from common.db import DatabaseConnection

class BaseDBModel(BaseModel):
    __database__ = 'auth'

    async def insert(self):
        _fields: list[str] = []
        _values: list[str] = []
        _data: list[Any] = []
        model_dump = self.model_dump()
        
        for i, field in enumerate(self.model_fields):
            value_template = f'${i+1}'
            
            _fields.append(field)
            _values.append(value_template)
            _data.append(model_dump.get(field))
        
        fields: str = ', '.join(_fields)
        values: str = ', '.join(_values)
        query = f'INSERT INTO users ({fields}) VALUES ({values})'
        
        connection = await DatabaseConnection.get_connection(db_name=self.__database__)
        await connection.execute(query, *_data)
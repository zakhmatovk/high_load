import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from auth.models.base import BaseDBModel

class User(BaseDBModel):
    __database__ = 'auth'
    
    id: UUID = Field(default_factory=uuid4)
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    birth_date: datetime.date
    gender: str
    city: str
    interests: list[str]
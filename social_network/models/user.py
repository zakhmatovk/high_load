import datetime
from uuid import UUID, uuid4
from pydantic import Field

from common.model import BasePgModel

class User(BasePgModel):
    __database__ = 'social_network'
    __table__ = 'users'
    
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
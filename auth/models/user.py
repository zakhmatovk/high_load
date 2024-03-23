from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    birth_date: str
    gender: str
    city: str
    interests: list[str]
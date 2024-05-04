import base64
import datetime
import json
from uuid import UUID, uuid4
from pydantic import Field, SecretStr, field_validator

from common.model import BasePgModel

def is_hash(password: str|SecretStr) -> bool:
    if isinstance(password, SecretStr):
        password = password.get_secret_value()
    return password.startswith('__hash__')

def hash_password(password: str|SecretStr) -> str:
    if isinstance(password, SecretStr):
        password = password.get_secret_value()
    return f'__hash__{password}'

class User(BasePgModel):
    __database__ = "social_network"
    __table__ = "users"

    id: UUID = Field(default_factory=uuid4)
    username: str
    email: str
    password: SecretStr
    first_name: str
    last_name: str
    birth_date: datetime.date
    gender: str
    city: str
    interests: list[str]

    @field_validator('password')
    @classmethod
    def hash_password(cls, pw: str|SecretStr) -> str|SecretStr:
        if is_hash(pw):
            return pw
        return hash_password(pw)

    def check_password(self, password: str) -> bool:
        return self.password.get_secret_value() == hash_password(password)
    
    def token(self) -> str:
        data = {'id': str(self.id)}    
        datastr = json.dumps(data)
        
        encoded = base64.b64encode(datastr.encode('utf-8')).decode('utf-8')
        return encoded

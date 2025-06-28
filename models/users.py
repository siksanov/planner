from typing import Optional, List
from beanie import Document, Link

from pydantic import BaseModel, EmailStr
from models.events import Event

class User(Document):
    username: EmailStr
    password: str

    class Settings:
        name = "users"

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "email": "fastapi@pact.com",
                "password": "strong!!!",
                "event": []
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
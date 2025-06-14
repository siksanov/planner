from beanie import Document, PydanticObjectId
from typing import Optional, List
from pydantic import BaseModel


class Event(Document):
    id: Optional[PydanticObjectId] = None
    creator: Optional[str] = None
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "id": "68063d65581b5e6363a86805",
                "title": "FastAPI Book Lacunch",
                "image": "https: \
                //linktomyimage.com/image.png",
                "description": "We will be discussing \
                the contents of the FastAPI book in \
                this event. Ensure to come with your \
                own copy to win gifts!",
                "tags": ["python", "fastapi", "book",
                "launch"],
                "location": "Google Meet"
            }
        }
    
    class Settings:
        name = "events"

class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing \
                the contents of the FastAPI book in \
                this event. Ensure to come with your \
                own copy to win gifts!",
                "tags": ["python", "fastapi", "book",
                         "launch"],
                "location": "Google Meet"
            }
        }
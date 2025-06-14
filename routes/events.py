from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.templating import Jinja2Templates
from database.connection import Database

from models.events import Event, EventUpdate
from typing import List
from auth.authenticate import authenticate

event_database = Database(Event)

event_router = APIRouter(
    tags=["Events"]
)

templates = Jinja2Templates(directory="templates/")


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(request: Request) -> List[Event]:
    events = await event_database.get_all()
    return templates.TemplateResponse("events.html",
    {
        "request": request,
        "events": events
    })

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(request: Request, id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return templates.TemplateResponse("events.html",
    {
        "request": request,
        "event": event
    })

@event_router.post("/new")
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    body.creator = user
    await event_database.save(body)
    return {
        "message": "Event created successfully."
    }

@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate,
                       user: str = Depends(authenticate)) -> Event:
    event = await event_database.get(id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )
    update_event = await event_database.update(id, body)
    if not update_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return update_event

@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId,
                       user: str = Depends(authenticate)) -> dict:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
    if event.creator != user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Operation not allowed"
            )
    event = await event_database.delete(id)
    
    return {
        "message": "Event deleted successfully."
    }
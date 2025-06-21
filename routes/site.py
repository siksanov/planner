from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from routes.events import retrieve_all_events, retrieve_event

from beanie import PydanticObjectId

site_router = APIRouter(
    tags=["Site"],
)


templates = Jinja2Templates(directory="templates/")


@site_router.get("/")
async def index(request: Request):
    events = await retrieve_all_events()
    return templates.TemplateResponse("index.html",
    {
        "request": request,
        "events": events
    })

@site_router.get("/{id}")
async def get_event(request: Request, id: PydanticObjectId):
    event = await retrieve_event(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return templates.TemplateResponse("index.html",
    {
        "request": request,
        "event": event
    })

@site_router.get("/auth/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html",
    {
        "request": request
    })


@site_router.get("/auth/signin")
async def signin(request: Request):
    return templates.TemplateResponse("signin.html",
    {
        "request": request
    })
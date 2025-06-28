from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.templating import Jinja2Templates
from routes.events import retrieve_all_events, retrieve_event
from routes.users import sign_user_up
from pydantic import EmailStr
from models.users import User

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

@site_router.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html",
    {
        "request": request
    })


@site_router.get("/signin")
async def signin(request: Request):
    return templates.TemplateResponse("signin.html",
    {
        "request": request
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
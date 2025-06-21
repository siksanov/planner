import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from database.connection import Settings
from routes.events import event_router
from routes.users import user_router
from routes.site import site_router

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

# register origins

origins = ["*"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await settings.initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
settings = Settings()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routes

app.include_router(user_router, prefix="/api/v1/user")
app.include_router(event_router, prefix="/api/v1/event")
app.include_router(site_router, prefix="/site")


@app.get("/")
async def home():
    return RedirectResponse(url="/site/")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                reload=True)

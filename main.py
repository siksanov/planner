import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse

from database.connection import Settings
from routes.events import event_router
from routes.users import user_router

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

# Register routes

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

@app.get("/")
async def home():
    return RedirectResponse(url="/event/")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                reload=True)

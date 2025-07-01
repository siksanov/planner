from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from database.connection import Database
from models.users import User, TokenResponse
from typing import Annotated

from auth.hash_password import HashPassword

user_router = APIRouter(
    tags=["User"]
)

user_database = Database(User)
hash_password = HashPassword()


@user_router.post("/signup")
async def sign_user_up(user: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    user_exist = await User.find_one(User.username == user.username)
    
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already."
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(User(username=user.username, password=user.password))
    return {
        "message": "User created successfully."
    }

@user_router.post("/signin")
async def sign_user_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> TokenResponse:
    user = await User.find_one(User.username == form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if hash_password.verify_hash(form_data.password, user.password):
        access_token = create_access_token({"sub": user.username}, expires_delta=None)
        response.set_cookie(key="token", value=f'{access_token}', httponly=True)
        return TokenResponse(access_token=access_token, token_type="Bearer")
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

@user_router.get("/set")
def set_cookie(response: Response):
    now = datetime.now()    # получаем текущую дату и время
    response = JSONResponse(content={"message": "куки установлены"})
    response.set_cookie(key="last_visit", value=f'{now}')
    return  response

@user_router.get("/get")
def get_cookie(last_visit = Cookie()):
    return  {"last visit": last_visit}
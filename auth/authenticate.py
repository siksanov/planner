from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from auth.jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/signin")
fff: Annotated[str, Depends(oauth2_scheme)]
async def authenticate(token: Annotated[str, Cookie()]) -> str:
    print(token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access"
        )

    decoded_token = verify_access_token(token)
    return decoded_token["user"]
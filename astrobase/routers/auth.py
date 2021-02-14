from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from astrobase.apis import auth as auth_api
from astrobase.schemas.auth import AstroToken

TOKEN_EXPIRE_MINUTES = 60 * 72

router = APIRouter()
tags = ["auth"]


@router.post("/login/token", tags=tags, response_model=AstroToken)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    astro_client = auth_api.authenticate_client(form_data.username, form_data.password)
    if not astro_client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = auth_api.create_access_token(
        data={"sub": astro_client.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

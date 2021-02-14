from datetime import datetime, timedelta
from typing import Union

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from starlette import status

from astrobase.schemas.auth import AstroToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "changethis"
ACCESS_TOKEN_ALGORITHM = "HS256"
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


class AuthAPI:
    def valid_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_client(
        self, client_email: str, password: str
    ) -> Union[bool, AstroToken]:
        if not self.valid_password(password, user.password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta) -> bytes:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)

    def astro_client(self, token: str = Depends(oauth2_scheme)) -> AstroToken:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
            email = payload.get("sub")
            if email is None or email == "":
                raise CREDENTIALS_EXCEPTION
        except PyJWTError:
            raise CREDENTIALS_EXCEPTION
        return AstroToken(token=token, token_type="bearer")

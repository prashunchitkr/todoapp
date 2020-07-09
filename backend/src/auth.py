from typing import Optional

from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.hash import pbkdf2_sha256

from . import models, schemas
from .app import APP_SECRET, TOKEN_EXPIRY_MINUTES
from .models import SessionLocal

oauth2_scheme = OAuth2PasswordBearer('/token')


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, APP_SECRET)
        username: str = payload.get('username')
        print(payload, username)
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = get_user(username)

    if not user:
        raise credentials_exception

    return user


def verify_password(hashed_pw: str, plain_pw: str):
    return pbkdf2_sha256.verify(plain_pw, hashed_pw)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    db = SessionLocal()
    q = db.query(models.User).filter(models.User.username == username)
    if user and not verify_password(user.password, password):
        return False
    return schemas.User(username=user.username, password=user.password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    to_encode.update({'expires': expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, APP_SECRET)
    return encoded_jwt


def get_user(username: str):
    db = SessionLocal()
    q = db.query(models.User).filter(models.User.username == username)

    if q.first():
        user = q.first()
        db.close()
        return user

    return None

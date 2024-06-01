import os
from datetime import datetime, timedelta
from jose import jwt
from typing import Union, Any
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# ACCESS_TOKEN_EXPIRE_MINUTES = 38000  # 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 380000000  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 10080  # 7 days ()60 * 24 * 7)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
  if expires_delta is not None:
    expires_delta = datetime.utcnow() + expires_delta
  else:
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  to_encode = {"exp": expires_delta, "sub": str(subject)}
  encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), os.getenv("ALGORITHM"))
  return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
  if expires_delta is not None:
    expires_delta = datetime.utcnow() + expires_delta
  else:
    expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

  to_encode = {"exp": expires_delta, "sub": str(subject)}
  encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_REFRESH_SECRET_KEY"), os.getenv("ALGORITHM"))
  return encoded_jwt

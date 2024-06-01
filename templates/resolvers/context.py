import os
from fastapi import HTTPException, status
from core.schemas import User
from functools import cached_property
from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType
from core.models import TokenPayload
from core.types import UserType
from db import engine
from jose import jwt
from sqlalchemy.orm import Session
from dotenv import load_dotenv, find_dotenv

_db = Session(engine)
load_dotenv(find_dotenv())


class Context(BaseContext):
  @cached_property
  def user(self) -> UserType:
    token = self.request.cookies.get("access_token")
    try:
      if token:
        token_data = jwt.decode(
          token, os.environ["JWT_SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]]
        )

        token_data = TokenPayload(**token_data)

        user = _db.query(User).filter(User.id == token_data.sub).first()
        UserType(
          id=user.id,
          first_name=user.first_name,
          last_name=user.last_name,
          email=user.email,
          avatar=user.avatar,
          avatar_color=user.avatar_color,
        )
        return user
      else:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Token expired or not provided"
        )
    except Exception as e:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials"
      )


@cached_property
def request(self):
  cookie = self.request.cookies.get("access_token", None)

  if cookie:
    return cookie


async def get_context() -> Context:
  return Context()


Info = _Info[Context, RootValueType]

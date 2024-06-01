import os
from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from jose import jwt
from pydantic import BaseModel
from strawberry import BasePermission
from strawberry.types import Info


class TokenPayload(BaseModel):
  sub: str
  exp: int
  # Add other token data fields as required


class IsAuthenticated(BasePermission):
  message = "User is not authenticated"

  async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
    request = info.context.request
    print(request.cookies, "REQUEST HERE")

    # Accessing cookies instead of headers
    if "access_token" in request.cookies:
      auth_cookie = request.cookies.get("access_token")
      print(auth_cookie, "COOKIE")
      try:
        payload = jwt.decode(
          auth_cookie, os.environ["JWT_SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]]
        )
        token_data = TokenPayload(**payload)
        print(token_data, "TOKEN DATA")

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
          print("CHECKING HEREE")
          raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": ""},
          )
        return True
      except Exception as e:
        # Handle decoding errors or any other exceptions
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid token",
          headers={"WWW-Authenticate": "Bearer"},
        )
    return False

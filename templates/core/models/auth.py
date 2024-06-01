from pydantic import BaseModel


class OAuthPayload(BaseModel):
  username: str
  password: str

class GooglePayload(BaseModel):
  code: str

class TokenPayload(BaseModel):
  sub: str = None
  exp: int = None

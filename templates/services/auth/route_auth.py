import os, requests
from utils.jwtUtils import create_access_token, create_refresh_token
from db.db import get_db
from core.schemas import User
from core.models import GooglePayload, OAuthPayload
from fastapi import HTTPException, APIRouter, Depends, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", os.getenv("GOOGLE_CLIENT_ID"))
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", os.getenv("GOOGLE_CLIENT_SECRET"))
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", os.getenv("GOOGLE_REDIRECT_URI"))


@router.post("/login")
def login(login_payload: OAuthPayload, _db: Session = Depends(get_db)):
  try:
    user = _db.query(User).filter(User.username == login_payload.username,
                                  User.password == login_payload.password).first()

    if user:
      access_token = create_access_token(user.id)
      refresh_token = create_refresh_token(user.id)

      # Set cookies in the response
      response = Response()
      response.set_cookie(key="access_token", value=access_token, samesite=None, secure=True)
      response.set_cookie(key="refresh_token", value=refresh_token, samesite=None, secure=True)

      # return response to set cookies
      return response
    else:
      return None
  except Exception as e:
    print(f"An error occurred: {e}")
    raise HTTPException(status_code=400, detail=f"User with provided ID does not exist.")


@router.post("/google_authenticate")
async def auth_google(google_payload: GooglePayload):
  code = google_payload.code
  if not code:
    raise HTTPException(status_code=400, detail="Code parameter is required")

  try:
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
      "code": code,
      "client_id": GOOGLE_CLIENT_ID,
      "client_secret": GOOGLE_CLIENT_SECRET,
      "redirect_uri": GOOGLE_REDIRECT_URI,
      "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    print(response, "RESPONSE")
    access_token = response.json()
    print(access_token, "TOKEN")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {access_token}"})
    print(user_info, "USER")
    return user_info.json()
  except requests.exceptions.RequestException as e:
    raise HTTPException(status_code=500, detail=f"Error communicating with Google: {str(e)}")


@router.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
  return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])

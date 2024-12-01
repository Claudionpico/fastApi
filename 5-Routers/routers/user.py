from fastapi import HTTPException, Request

from pydantic import BaseModel, Field
from authentication import createToken, verifyToken
from fastapi.security import HTTPBearer
from models.movie import Movie as MovieModel
from db.database import Session
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerUser = APIRouter()

class BarearToken(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = verifyToken(auth.credentials)

        if data["emails"] != "claudionpico@gmail.com":
            raise HTTPException(status_code=401, detail="Invalid token")
        if data["password"] != "123456":
            raise HTTPException(status_code=401, detail="Invalid token")

class User(BaseModel):
    emails: str
    password: str

@routerUser.post("/login", tags=["authentication"], status_code=200)
def login(user: User):
    if user.emails != "claudionpico@gmail.com" or user.password != "123456":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = createToken(user.dict())
    return token
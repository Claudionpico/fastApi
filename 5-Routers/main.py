from fastapi import FastAPI, Path, Query, HTTPException, Request, Depends

from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from authentication import createToken, verifyToken
from fastapi.security import HTTPBearer
from models.movie import Movie as MovieModel
from db.database import Base, Session, engine
from fastapi.encoders import jsonable_encoder
from routers.movie import routerMovie
from routers.user import routerUser

app = FastAPI(
    title="Aprendiendo FastAPI",
    description="Este es un proyecto de prueba para aprender FastAPI",
    version="0.1"
)

app.include_router(routerMovie)
app.include_router(routerUser)


Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Inicio"])
def read_root():
    return HTMLResponse('<h1>¡Hola mundo!</h1>')



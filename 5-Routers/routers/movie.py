from fastapi import Path, Query, HTTPException, Request, Depends

from fastapi.responses import  JSONResponse
from pydantic import BaseModel, Field
from authentication import verifyToken
from fastapi.security import HTTPBearer
from models.movie import Movie as MovieModel
from db.database import Session
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerMovie = APIRouter()

class BarearToken(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = verifyToken(auth.credentials)

        if data["emails"] != "claudionpico@gmail.com":
            raise HTTPException(status_code=401, detail="Invalid token")
        if data["password"] != "123456":
            raise HTTPException(status_code=401, detail="Invalid token")


class Movie(BaseModel):
    title: str = Field(default="title of movie", min_length=3, max_length=100)
    #description: str = Field(default="description of movie", min_length=3)
    overview: str
    year: int = Field(default=2021, ge=1900, le=2022)
    rating: float = Field(default=0.0, ge=0.0, le=10.0)
    category: str = Field(default="category of movie", min_length=3)

@routerMovie.get("/movies", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
def get_movies():
    db = Session()
    data = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(data))

@routerMovie.get("/movies/", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
def get_movies_by_category(category: str = Query(None)):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(data))

@routerMovie.get("/movies/{movie_id}", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
def read_movie(movie_id: int = Path(ge=1, le=100)):
    data = Session().query(MovieModel).filter(MovieModel.id == movie_id).first()
    return JSONResponse(content= jsonable_encoder(data))

@routerMovie.post("/movies/")
def create_movie(movie: Movie):
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)  # Refresca para obtener los valores generados automáticamente como el ID
    return {"msg": "Movie added", "movie": new_movie}


@routerMovie.put("/movies/{movie_id}", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
def update_movie(movie: Movie, movie_id: int):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not data:
        return JSONResponse(content={"msg": "Movie not found"})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(content=[movie.dict()])

@routerMovie.delete("/movies/{movie_id}", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
def delete_movie(movie_id: int):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not data:
        return JSONResponse(content={"msg": "Movie not found"})
    db.delete(data)
    db.commit()
    return JSONResponse(content={"msg": "Movie deleted"})
from fastapi import FastAPI, Path, Query, HTTPException, Request, Depends

from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from authentication import createToken, verifyToken
from fastapi.security import HTTPBearer
from models.movie import Movie as MovieModel
from db.database import Base, Session, engine
from fastapi.encoders import jsonable_encoder

app = FastAPI(
    title="Aprendiendo FastAPI",
    description="Este es un proyecto de prueba para aprender FastAPI",
    version="0.1"
)

class Movie(BaseModel):
    title: str = Field(default="title of movie", min_length=3, max_length=100)
    #description: str = Field(default="description of movie", min_length=3)
    overview: str
    year: int = Field(default=2021, ge=1900, le=2022)
    rating: float = Field(default=0.0, ge=0.0, le=10.0)
    category: str = Field(default="category of movie", min_length=3)

class User(BaseModel):
    emails: str
    password: str

Base.metadata.create_all(bind=engine)


class BarearToken(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = verifyToken(auth.credentials)

        if data["emails"] != "claudionpico@gmail.com":
            raise HTTPException(status_code=401, detail="Invalid token")
        if data["password"] != "123456":
            raise HTTPException(status_code=401, detail="Invalid token")


movies = [
    {
        "id": 1,
        "title": "Inception",
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given a chance to have his criminal history erased. His task is to do the opposite: implant an idea into the mind of a CEO.",
        "year": 2010,
        "rating": 8.8,
        "category": "Science Fiction, Action"
    },
    {
        "id": 2,
        "title": "The Shawshank Redemption",
        "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "year": 1994,
        "rating": 9.3,
        "category": "Drama"
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "overview": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham. The Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "year": 2008,
        "rating": 9.0,
        "category": "Action, Crime, Drama"
    },
    {
        "id": 4,
        "title": "The Godfather",
        "overview": "An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
        "year": 1972,
        "rating": 9.2,
        "category": "Crime, Drama"
    }
]

@app.post("/login", tags=["authentication"], status_code=200)
def login(user: User):
    if user.emails != "claudionpico@gmail.com" or user.password != "123456":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = createToken(user.dict())
    return token

@app.get("/", tags=["Inicio"])
def read_root():
    return HTMLResponse('<h1>¡Hola mundo!</h1>')

@app.get("/movies", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
def get_movies():
    db = Session()
    data = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(data))

@app.get("/movies/", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
def get_movies_by_category(category: str = Query(None)):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(data))

@app.get("/movies/{movie_id}", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
def read_movie(movie_id: int = Path(ge=1, le=100)):
    data = Session().query(MovieModel).filter(MovieModel.id == movie_id).first()
    return JSONResponse(content= jsonable_encoder(data))

@app.post("/movies/")
def create_movie(movie: Movie):
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)  # Refresca para obtener los valores generados automáticamente como el ID
    return {"msg": "Movie added", "movie": new_movie}


@app.put("/movies/{movie_id}", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
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

@app.delete("/movies/{movie_id}", tags=["Movies"], status_code=200, dependencies=[Depends(BarearToken())])
def delete_movie(movie_id: int):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not data:
        return JSONResponse(content={"msg": "Movie not found"})
    db.delete(data)
    db.commit()
    return JSONResponse(content={"msg": "Movie deleted"})

from fastapi import FastAPI, Path, Query

from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Aprendiendo FastAPI",
    description="Este es un proyecto de prueba para aprender FastAPI",
    version="0.1"
)

class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(default="title of movie", min_length=3, max_length=100)
    description: str = Field(default="description of movie", min_length=3)
    overview: str
    year: int = Field(default=2021, ge=1900, le=2022)
    rating: float = Field(default=0.0, ge=0.0, le=10.0)
    category: str = Field(default="category of movie", min_length=3)

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

@app.get("/", tags=["Inicio"])
def read_root():
    return HTMLResponse('<h1>¡Hola mundo!</h1>')

@app.get("/movies", tags=["Movies"], status_code=200)
def read_root():
    return JSONResponse(content={"msg": f"Movies", "movie": movies})

@app.get("/movies/{movie_id}", tags=["Movies"], status_code=200)
def read_movie(movie_id: int = Path(ge=1, le=100)):
    for movie in movies:
        if movie['id'] == movie_id:
            selectMovie = movie
    return JSONResponse(content={"msg": f"Movie", "movie": [selectMovie]})


@app.get("/movies/", tags=["Movies"], status_code=200)
def get_movies_by_category(category: str = Query( min_length=3)):
    movies_by_category = []
    for movie in movies:
        if category.lower() in movie["category"].lower():
            movies_by_category.append(movie)
    return JSONResponse(content={"msg": f"Movie by '{category}'", "movie": [movies_by_category]})

@app.post("/movies/", tags=["Movies"], status_code=201)
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={"msg": "Movie add", "movie": [movie.dict()]})

@app.put("/movies/{movie_id}", tags=["Movies"], status_code=200)
def update_movie(movie: Movie, movie_id: int):
    for m in movies:
        if m["id"] == movie_id:
            m["title"] = movie.title
            m["overview"] = movie.overview
            m["year"] = movie.year
            m["rating"] = movie.rating
            m["category"] = movie.category
    return JSONResponse(content={"msg": "Movie update", "movie": [movie.dict()]})

@app.delete("/movies/{movie_id}", tags=["Movies"], status_code=200)
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            return {"message": "Movie deleted"}
    return JSONResponse(content={"msg": "Movie delete"})
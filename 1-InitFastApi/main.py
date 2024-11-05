from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Aprendiendo FastAPI",
    description="Este es un proyecto de prueba para aprender FastAPI",
    version="0.1"
)

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

@app.get("/movies", tags=["Movies"])
def read_root():
    return movies

@app.get("/movies/{movie_id}", tags=["Movies"])
def read_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return {"message": "Movie not found"}

@app.get("/movies/", tags=["Movies"])
def get_movies_by_category(category: str):
    movies_by_category = []
    for movie in movies:
        if category.lower() in movie["category"].lower():
            movies_by_category.append(movie)
    return movies

@app.post("/movies/", tags=["Movies"])
def create_movie(
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
):
    movie = {
        "id": len(movies) + 1,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    }
    movies.append(movie)
    return movies

@app.put("/movies/{movie_id}", tags=["Movies"])
def update_movie(
    movie_id: int,
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
):
    for movie in movies:
        if movie["id"] == movie_id:
            movie["title"] = title
            movie["overview"] = overview
            movie["year"] = year
            movie["rating"] = rating
            movie["category"] = category
            return movie
    return {"message": "Movie not found"}

@app.delete("/movies/{movie_id}", tags=["Movies"])
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            return {"message": "Movie deleted"}
    return {"message": "Movie not found"}
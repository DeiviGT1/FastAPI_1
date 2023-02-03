from fastapi import FastAPI, Depends, HTTPException, Request, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie


app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

@app.get("/")
class  JWTUser(BaseModel):
    async def __call__(self, request: Request):
      auth = await super().__call__(request)
      data = validate_token(auth.credentials)
      if data["email"] != "admin@gmail.com":
        raise HTTPException(status_code=403, detail="Unauthorized")

class User(BaseModel):
  email: str
  password: str

class Movie(BaseModel):
  id: Optional[int] == None
  title: str = Field(min_length=5, max_length=15)
  overview: str = Field(min_length=15, max_length=50)
  year: int = Field(min_length=4, max_length=4)
  rating: float = Field(min_value=0.0, max_value=10.0)
  category: str = Field(min_length=5, max_length=15)

  class Config:
    schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get("/", tags=["Home"])
def message():
  return HTMLResponse(content="<h1>¡Hola mundo!</h1>")

@app.post("/login", tags=["auth"])
def login(user: User):
  if user.email == "admin@gmail.com" and user.password == "admin":
    token: str = create_token(user.dict())
    return JSONResponse(content= token, status_code=200)

# La solicitud requiere un token de autenticación JWT valido
@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTUser())])
def get_movies() -> List[Movie]:
  return JSONResponse(content=movies, status_code=200)

@app.get("/movies/{movie_id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movies(id: int = Path(ge=1, le=200)) -> Movie:
  for item in movies:
    if item["id"] == id:
      return JSONResponse(content=item, status_code=200)
  return JSONResponse(content={"message": "Movie not found"}, status_code=404)

@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
  data =  [item for item in movies if item["category"] == category]
  return JSONResponse(content=data, status_code=200)

@app.post("/movies", tags=["movies"], response_model=Movie, status_code=201)
def create_movie(movie: Movie) -> dict:
  movies.append(movie)
  return JSONResponse(content={"Message":"Se ha registrado con exito la pelicula","":movie.dict()}, status_code=201)

@app.put("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(movie_id: int, movie: Movie) -> dict:
  for item in movies:
    if item["id"] == movie_id:
      item["title"] = movie.title
      item["overview"] = movie.overview
      item["year"] = movie.year
      item["rating"] = movie.rating
      item["category"] = movie.category
      return JSONResponse(content={"Message":"Se ha actualizado con exito la pelicula","":movie.dict()}, status_code=200)

@app.delete("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
  for item in movies:
    if item["id"] == movie_id:
      movies.remove(item)
      return JSONResponse(content={"Message":"Se ha eliminado con exito la pelicula"}, status_code=200)
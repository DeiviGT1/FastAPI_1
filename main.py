from typing import List, Optional

from fastapi import Depends, FastAPI, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from config.database import Base, Session, engine
from jwt_manager import create_token
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTUser
from models.movie import Movie as MovieModel

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)

class User(BaseModel):
  email: str
  password: str

class Movie(BaseModel):
  id: Optional[int] = None
  title: str = Field(min_length=5, max_length=15)
  overview: str = Field(min_length=15, max_length=50)
  year: int = Field(le=2022)
  rating:float = Field(ge=1, le=10)
  category:str = Field(min_length=5, max_length=15)

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
  db = Session()
  result = db.query(MovieModel).all()
  return JSONResponse(content= jsonable_encoder(result), status_code=200)

@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
  db = Session()
  result = db.query(MovieModel).filter(MovieModel.id == id).first()
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
  db = Session()
  result = db.query(MovieModel).filter(MovieModel.category == category).all()
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  return JSONResponse(content=jsonable_encoder(result), status_code=200)

@app.post("/movies", tags=["movies"], response_model=Movie, status_code=201)
def create_movie(movie: Movie) -> dict:
  db = Session()
  # ** Lo que hace es traer los atributos y pasarlos como parametros
  new_movie = MovieModel(**movie.dict())
  db.add(new_movie)
  db.commit()
  return JSONResponse(content={"Message":"Se ha registrado con exito la pelicula","":movie.dict()}, status_code=201)

@app.put("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(movie_id: int, movie: Movie) -> dict:
  db = Session()
  result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  result.title = movie.title
  result.overview = movie.overview
  result.year = movie.year
  result.rating = movie.rating
  result.category = movie.category
  db.commit()
  return JSONResponse(content={"Message":"Se ha actualizado con exito la pelicula","":movie.dict()}, status_code=200)

@app.delete("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
  db = Session()
  result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  db.delete(result)
  db.commit() 
  return JSONResponse(content={"Message":"Se ha eliminado con exito la pelicula"}, status_code=200)
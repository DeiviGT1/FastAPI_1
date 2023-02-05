from fastapi import APIRouter

from typing import List, Optional

from fastapi import Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from config.database import Session
from middlewares.jwt_bearer import JWTUser
from models.movie import Movie as MovieModel
from services.movie import MovieService

movie_router = APIRouter()

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

# La solicitud requiere un token de autenticación JWT valido
@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTUser())])
def get_movies() -> List[Movie]:
  db = Session()
  result = MovieService(db).get_movies()
  return JSONResponse(content= jsonable_encoder(result), status_code=200)

@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
  db = Session()
  result = db.query(MovieModel).filter(MovieModel.id == id).first()
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
  db = Session()
  result = db.query(MovieModel).filter(MovieModel.category == category).all()
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.post("/movies", tags=["movies"], response_model=Movie, status_code=201)
def create_movie(movie: Movie) -> dict:
  db = Session()
  # ** Lo que hace es traer los atributos y pasarlos como parametros
  new_movie = MovieModel(**movie.dict())
  db.add(new_movie)
  db.commit()
  return JSONResponse(content={"Message":"Se ha registrado con exito la pelicula","":movie.dict()}, status_code=201)

@movie_router.put("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
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

@movie_router.delete("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
  db = Session()
  result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  db.delete(result)
  db.commit() 
  return JSONResponse(content={"Message":"Se ha eliminado con exito la pelicula"}, status_code=200)
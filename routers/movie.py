from fastapi import APIRouter

from typing import List

from fastapi import Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session
from middlewares.jwt_bearer import JWTUser
from models.movie import Movie as MovieModel
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

# La solicitud requiere un token de autenticación JWT valido
@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200) # , dependencies=[Depends(JWTUser())]
def get_movies() -> List[Movie]:
  db = Session()
  result = MovieService(db).get_movies()
  return JSONResponse(content= jsonable_encoder(result), status_code=200)

@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
  db = Session()
  result = MovieService(db).get_movie(id)
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
  db = Session()
  result = MovieService(db).get_movies_by_category(category)
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.post("/movies", tags=["movies"], response_model=Movie, status_code=201)
def create_movie(movie: Movie) -> dict:
  db = Session()
  MovieService(db).create_movie(movie)
  return JSONResponse(content={"Message":"Se ha registrado con exito la pelicula","":movie.dict()}, status_code=201)

@movie_router.put("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(movie_id: int, movie: Movie) -> dict:
  db = Session()
  result = MovieService(db).get_movie(movie_id)
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
    
  MovieService(db).update_movie(movie_id, movie)
  return JSONResponse(content={"Message":"Se ha actualizado con exito la pelicula","":movie.dict()}, status_code=200)

@movie_router.delete("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
  db = Session()
  result = MovieService(db).get_movie(movie_id)
  if not result:
    return JSONResponse(status_code=404, content={'message': "No encontrado"})
  
  MovieService(db).delete_movie(movie_id)
  return JSONResponse(content={"Message":"Se ha eliminado con exito la pelicula"}, status_code=200)
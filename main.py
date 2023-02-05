from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

#Es una funcion de fastAPI que sirve para añadir middlewares
app.add_middleware(ErrorHandler)


Base.metadata.create_all(bind=engine)

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

app.include_router(movie_router)
app.include_router(user_router)
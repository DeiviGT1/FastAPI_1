from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body, Query
import uvicorn

app = FastAPI()

# Modelos
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}

#Request and response body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return Person

#Validaciones Query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: int = Query(...)   
):
    return {name: age}

# if __name__ == "__main__":  
#     uvicorn.run(app, host="127.0.0.1", port=5000)
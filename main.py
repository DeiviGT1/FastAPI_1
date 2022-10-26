from doctest import Example
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from fastapi import FastAPI, Body, Query, Path
import uvicorn

app = FastAPI()

class HairColor(Enum):
    white = "white"
    blode = "blonde"
    brown = "brown"
    black = "black"
    red = "red"

# Modelos
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = "Jose"
        )
    last_name: str = Field(
        min_length=1,
        max_length=50,
        example = "Tabarez"
        )
    age: int = Field(
        ...,
        gt = 0,
        le = 115,
        example = 25
    )
    hair_color: Optional[HairColor] = Field(default=None, example = "brown")
    is_married: Optional[bool] = Field(default = None, example = False)
    
    # class Config:
    #     schema_extra = {
    #         "example": { 
    #             "first_name" : "David",
    #             "last_name" : "Gonzalez",
    #             "age" : 21,
    #             "hair_color" : "black",
    #             "is_married" : False
    #         }
    #     }

class Location(BaseModel):
    ciry: str
    state: str
    country: str

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
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title = "Person name",
        description = "This is the person name. It's between 1 and 50 characters"
        ),
    age: int = Query(
        ...,
        title = "Person age",
        description = "This is the person age, It's required"
        )
):
    return {name: age}

#Validaciones path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0
        )
):
    return {person_id: "It exists!"}

#Validaciones body parameter
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = "Person id",
        description = "This is the person id",
        gt = 0
        ),
    person: Person = Body(...),
    #location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())
    return person

# if __name__ == "__main__":  
#     uvicorn.run(app, host="127.0.0.1", port=5000)
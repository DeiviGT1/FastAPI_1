from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body
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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
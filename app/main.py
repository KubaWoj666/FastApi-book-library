from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import authors, books, users, samples_data
from .database import engine, get_db
from . import models 


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authors.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(samples_data.router)

@app.get("/")
def hello():
    return {'message': 'Hello'}
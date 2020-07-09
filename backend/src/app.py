from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .models import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ("http://localhost:8080")

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=['*'],
                   allow_headers=['*'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from .views import *

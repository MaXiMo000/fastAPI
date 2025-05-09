from fastapi import FastAPI
from .routers import post, user, auth, vote
from .config import settings
from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
# origins = ["https://www.google.co.in"]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Hello": "World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
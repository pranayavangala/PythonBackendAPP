from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine
from app.models import Base
from app.routes import router

app = FastAPI(
    title="Python Backend App",
    description="FastAPI + SQLAlchemy project",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "FastAPI application is running successfully"
    }
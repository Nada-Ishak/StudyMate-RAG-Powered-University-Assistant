from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.api.routes.query import router as query_router
from backend.app.services.retrieval import (
    load_embedding_model,
    load_collection
)
from backend.app.utils.logging_config import setup_logging
from backend.app.api.routes.upload import router as upload_router
from backend.app.api.routes.summary import router as summary_router


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading StudyMate resources...")

    app.state.embedding_model = load_embedding_model()
    app.state.collection = load_collection()

    print("StudyMate resources loaded successfully!")

    yield

    print("StudyMate shutting down...")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "StudyMate API"
    }


app.include_router(query_router)
app.include_router(upload_router)
app.include_router(summary_router)
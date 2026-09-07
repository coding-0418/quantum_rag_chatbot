from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat, documents, health
from app.core.config import get_settings
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting Quantum RAG Chatbot API")
    yield
    logger.info("Shutting down Quantum RAG Chatbot API")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Quantum RAG Chatbot",
        description="Multi-agent quantum-enhanced retrieval-augmented generation system",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(documents.router)

    return app


app = create_app()

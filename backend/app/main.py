from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models  # noqa: ensures models are registered before create_all
from .routers import (
    auth_router, schemes_router, scholarships_router,
    eligibility_router, chat_router, documents_router, misc_router,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SulabhAI API",
    description="Marathi AI Gateway to Government Schemes, Scholarships & Public Benefits",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(schemes_router.router)
app.include_router(scholarships_router.router)
app.include_router(eligibility_router.router)
app.include_router(chat_router.router)
app.include_router(documents_router.router)
app.include_router(misc_router.router)


@app.get("/")
def root():
    return {"name": "SulabhAI API", "status": "ok", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}

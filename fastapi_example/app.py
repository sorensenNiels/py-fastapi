import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .config import getAPIVersion, setLogBasicConfig, settings
from .db import create_db_and_tables, engine
from .routes import main_router

setLogBasicConfig()

logger = logging.getLogger(__name__)

description = """
fastapi_example API helps you do awesome stuff. 🚀
"""


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("---> Inside lifespan function")
    create_db_and_tables(engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="fastapi_example",
    description=description,
    version=getAPIVersion(),
    terms_of_service="http://fastapi_example.com/terms/",
    contact={
        "name": "sorensenNiels",
        "url": "http://fastapi_example.com/contact/",
        "email": "sorensenNiels@fastapi_example.com",
    },
    license_info={
        "name": "The Unlicense",
        "url": "https://unlicense.org",
    },
)


if settings.server and settings.server.get("cors_origins", None):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.cors_origins,
        allow_credentials=settings.get("server.cors_allow_credentials", True),
        allow_methods=settings.get("server.cors_allow_methods", ["*"]),
        allow_headers=settings.get("server.cors_allow_headers", ["*"]),
    )

app.include_router(main_router)

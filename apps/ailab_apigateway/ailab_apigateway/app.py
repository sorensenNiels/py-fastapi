from contextlib import asynccontextmanager
from ailab_apigateway.routers import ask
from fastapi import FastAPI

from .config import getAPIVersion, setLogBasicConfig, description
from .routers import health


setLogBasicConfig()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # TODO: Add db connection
    yield


app = FastAPI(
    lifespan=lifespan,
    title="ailab_apigateway",
    description=description,
    version=getAPIVersion(),
    terms_of_service="https://lionbrain.com/terms/",
    contact={
        "name": "The AI Lab Team",
        "url": "https://lionbrain.com",
        "email": "aiteam@lionbrain.com",
    },
    license_info={
        "name": "The Unlicense",
        "url": "https://unlicense.org",
    },
)

# TODO: Add middleware

# Add routers
app.include_router(health.router)
app.include_router(ask.router)

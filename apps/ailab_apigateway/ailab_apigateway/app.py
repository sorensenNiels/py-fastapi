from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .config import description, getAPIVersion, setLogBasicConfig, settings
from .routers import main_router

setLogBasicConfig()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # TODO: Add db connection
    yield


app = FastAPI(
    lifespan=lifespan,
    title="AI Lab API Gateway",
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

# Setup CORS middleware
if settings.server and settings.server.get("cors_origins", None):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.cors_origins,
        allow_credentials=settings.get("server.cors_allow_credentials", True),
        allow_methods=settings.get("server.cors_allow_methods", ["*"]),
        allow_headers=settings.get("server.cors_allow_headers", ["*"]),
    )

# Todo! Setup Requst ID middleware
# Todo! Setup access log middleware

# Add routers
app.include_router(main_router)

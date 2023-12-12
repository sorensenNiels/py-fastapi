from fastapi import APIRouter

from ..config import settings

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    """
    Check if the service is healthy.

    Returns
    -------
    dict
        A dictionary containing the status of the service.
    """

    environment = settings.get("ENV_FOR_DYNACONF")
    logLevel = settings.get("LOG_LEVEL")

    return {"status": True, "environment": environment, "logLevel": logLevel}

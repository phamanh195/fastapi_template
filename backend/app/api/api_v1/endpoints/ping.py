from fastapi import APIRouter, Depends

from app import models, schemas
from app.core import depends

router = APIRouter()


@router.get("/public", response_model=schemas.PingSchema)
def ping_public():
    """
    Public API. Any users (include anonymous) can call this API.
    """
    return {"message": "Hello world"}


@router.get("/private", response_model=schemas.PingSchema)
def ping_private(user: models.User = Depends(depends.get_current_user)):
    """
    Private API. Allow login users can call this API.
    """
    return {"message": "Hello world"}

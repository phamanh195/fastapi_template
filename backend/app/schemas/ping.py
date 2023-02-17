from pydantic import BaseModel


class PingSchema(BaseModel):
    """
    Schema for ping API response.
    """

    message: str

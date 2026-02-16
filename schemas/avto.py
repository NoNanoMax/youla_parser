from datetime import datetime
from pydantic import BaseModel, AnyUrl


class AvtoOut(BaseModel):
    url: AnyUrl
    title: str | None
    published_at: datetime | None = None
    photo_urls: list[AnyUrl] = []
    color: str | None = None
    year: int | None = None
    company: str | None = None
    brand: str | None = None

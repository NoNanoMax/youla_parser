from pydantic import BaseModel, AnyUrl


class LinkOut(BaseModel):
    url: AnyUrl
    source: str
    
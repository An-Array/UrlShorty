from pydantic import BaseModel, ConfigDict, HttpUrl


class SlugData(BaseModel):
  url: str
  slug: str | None = None
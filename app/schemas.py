from pydantic import BaseModel, ConfigDict


class SlugData(BaseModel):
  url: str
  slug: str | None = None
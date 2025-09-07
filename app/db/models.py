from sqlalchemy import String, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from typing import List
from .database import Base

class SlugStore(Base):
  __tablename__ = "slugs"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

  def __repr__(self):
    return f"<SlugStore(id={self.id}, url={self.url}, slug={self.slug}, created_at={self.created_at})>"

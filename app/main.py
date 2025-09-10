from fastapi import FastAPI, Depends, status, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.database import get_db, engine
from app.db import models
from app import schemas
import secrets
import string

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def generate_random_slug(db: Session, length: int = 6):
  alphabet = string.ascii_letters + string.digits
  while True:
    slug = "".join(secrets.choice(alphabet) for _ in range(length))
    if not db.query(models.SlugStore).filter(models.SlugStore.slug == slug).first():
      return slug

@app.get("/")
def root():
  return {"message":"FastAPI works!!"}

@app.post("/shorten")
def shorten_url(slug_data: schemas.SlugData, request: Request, db: Session = Depends(get_db)):
  url_db = db.query(models.SlugStore).filter(models.SlugStore.url == slug_data.url).first()
  if url_db:
    return {"Details":"ShortUrl Already exists", "short_url": f"{request.base_url}{url_db.slug}"}
  slug = slug_data.slug or generate_random_slug(db)
  new_data = models.SlugStore(url = slug_data.url, slug=slug)
  db.add(new_data)
  try:
    db.commit()
    db.refresh(new_data)
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This Custom slug is already present. Please try another Slug!!")
  return {"short_url" : f"{request.base_url}{new_data.slug}"}

@app.get("/{slug}")
async def slug_redirect(slug: str, db: Session = Depends(get_db)):
  db_q = db.query(models.SlugStore).filter(models.SlugStore.slug == slug).first()
  if not db_q:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found!")
  long_url = db_q.url
  return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)
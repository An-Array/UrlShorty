from fastapi import FastAPI, Depends, status, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db, engine
from app.db import models
from app import schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
  return {"message":"FastAPI works!!"}

@app.post("/shorten")
def shorten_url(slug_data: schemas.SlugData, request: Request, db: Session = Depends(get_db)):
  url_db = db.query(models.SlugStore).filter(models.SlugStore.url == slug_data.url).first()
  if url_db is not None:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="shortyurl already exists for this!")
  new_data = models.SlugStore(url = slug_data.url, slug=slug_data.slug)
  db.add(new_data)
  db.commit()
  db.refresh(new_data)
  return {"short_url" : f"{request.base_url}{new_data.slug}"}

@app.get("/{slug}")
async def slug_redirect(slug: str, db: Session = Depends(get_db)):
  db_q = db.query(models.SlugStore).filter(models.SlugStore.slug == slug).first()
  if not db_q:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found!")
  long_url = db_q.url
  return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)
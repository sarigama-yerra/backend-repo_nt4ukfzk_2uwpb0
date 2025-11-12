from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Project, CaseStudy, Testimonial, BlogPost, ContactSubmission
import os

app = FastAPI(title="AI Studio Portfolio API", version="1.0.0")

# CORS for frontend
frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "service": "portfolio-api"}

@app.get("/test")
async def test_db():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")
    # Just list collections names to confirm connectivity
    cols = await _list_collections()
    return {"db_connected": True, "collections": cols}

async def _list_collections():
    try:
        return db.list_collection_names()
    except Exception:
        return []

# Read endpoints (for demo content)
@app.get("/projects", response_model=List[Project])
async def list_projects():
    docs = get_documents("project", limit=12)
    # Convert Mongo docs to Pydantic-ready dicts
    return [
        {
            "title": d.get("title", ""),
            "client": d.get("client"),
            "summary": d.get("summary", ""),
            "cover_image": d.get("cover_image"),
            "tags": d.get("tags", []),
            "stat": d.get("stat"),
        }
        for d in docs
    ]

@app.get("/testimonials", response_model=List[Testimonial])
async def list_testimonials():
    docs = get_documents("testimonial", limit=5)
    return [
        {
            "name": d.get("name", ""),
            "role": d.get("role", ""),
            "quote": d.get("quote", ""),
            "avatar": d.get("avatar"),
        }
        for d in docs
    ]

@app.get("/posts", response_model=List[BlogPost])
async def list_posts():
    docs = get_documents("blogpost", limit=2)
    return [
        {
            "title": d.get("title", ""),
            "slug": d.get("slug", ""),
            "excerpt": d.get("excerpt", ""),
            "hero_image": d.get("hero_image"),
        }
        for d in docs
    ]

# Contact form submission
class ContactIn(BaseModel):
    name: str
    email: EmailStr
    brief: str

@app.post("/contact")
async def submit_contact(payload: ContactIn):
    submission = ContactSubmission(**payload.model_dump())
    try:
        _id = create_document("contactsubmission", submission)
        return {"ok": True, "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

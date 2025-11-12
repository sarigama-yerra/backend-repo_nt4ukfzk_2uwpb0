"""
Database Schemas for AI Studio Portfolio

Each Pydantic model maps to a MongoDB collection whose name is the lowercase of the class.
Example: class Project -> collection "project"
"""
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class Project(BaseModel):
    title: str = Field(..., description="Project title")
    client: Optional[str] = Field(None, description="Client name")
    summary: str = Field(..., description="Short one-liner about the project")
    cover_image: Optional[HttpUrl] = Field(None, description="Hero image URL (WebP/AVIF preferred)")
    tags: List[str] = Field(default_factory=list, description="Tech and domain tags")
    stat: Optional[str] = Field(None, description="Measurable result, e.g., '+32% sign-ups'")

class CaseStudy(BaseModel):
    project_id: str = Field(..., description="Related project document id (string)")
    problem: str = Field(..., description="Business or UX problem")
    solution: str = Field(..., description="Approach and what was shipped")
    stack: List[str] = Field(default_factory=list, description="Tech stack")
    before_image: Optional[HttpUrl] = Field(None, description="Before screenshot")
    after_image: Optional[HttpUrl] = Field(None, description="After screenshot")

class Testimonial(BaseModel):
    name: str = Field(..., description="Client name")
    role: str = Field(..., description="Client role/title")
    quote: str = Field(..., description="Short testimonial quote")
    avatar: Optional[HttpUrl] = Field(None, description="Avatar image URL")

class BlogPost(BaseModel):
    title: str = Field(..., description="Post title")
    slug: str = Field(..., description="URL slug")
    excerpt: str = Field(..., description="Short excerpt")
    hero_image: Optional[HttpUrl] = Field(None, description="Hero image URL")

class ContactSubmission(BaseModel):
    name: str = Field(..., description="Sender name")
    email: str = Field(..., description="Sender email")
    brief: str = Field(..., description="Project brief / message")
    source: Optional[str] = Field(None, description="Where they found us or campaign tag")

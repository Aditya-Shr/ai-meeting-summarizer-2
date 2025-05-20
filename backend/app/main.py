from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import meetings, action_items, decisions
from app.core.config import settings
import os

app = FastAPI(
    title="AI Meeting Summarizer API",
    description="API for meeting transcription, summarization, and tracking",
    version="1.0.0"
)

# Get allowed origins from environment variable or use default
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(meetings.router, prefix="/api/meetings", tags=["meetings"])
app.include_router(action_items.router, prefix="/api/action-items", tags=["action-items"])
app.include_router(decisions.router, prefix="/api/decisions", tags=["decisions"])

@app.get("/")
async def root():
    return {"message": "AI Meeting Summarizer API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
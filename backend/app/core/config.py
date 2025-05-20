from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./app.db"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"
    
    # Hugging Face settings
    HUGGINGFACE_CACHE_DIR: str = str(Path.home() / ".cache" / "huggingface")
    
    # Google Calendar settings
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    
    # OpenAI settings
    OPENAI_API_KEY: Optional[str] = None
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    
    # Transcription settings
    TRANSCRIPTION_PROVIDER: str = "huggingface"  # Default to huggingface
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 
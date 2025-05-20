import os
from fastapi import UploadFile, HTTPException
import tempfile
from app.core.config import settings
import whisper
import torch

class TranscriptionService:
    _model = None

    @staticmethod
    def _load_model():
        """Load or initialize the Whisper model"""
        if TranscriptionService._model is None:
            try:
                # Create cache directory if it doesn't exist
                os.makedirs(settings.HUGGINGFACE_CACHE_DIR, exist_ok=True)
                
                # Load model
                TranscriptionService._model = whisper.load_model("base")
                
                # Move model to GPU if available
                if torch.cuda.is_available():
                    TranscriptionService._model = TranscriptionService._model.to("cuda")
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error loading Whisper model: {str(e)}"
                )

    @staticmethod
    async def transcribe_audio(file: UploadFile, provider: str = "huggingface"):
        """
        Transcribe audio file using OpenAI's Whisper model
        """
        try:
            # Load model if not already loaded
            TranscriptionService._load_model()
            
            # Save the uploaded file temporarily
            temp_path = f"uploads/temp_{file.filename}"
            with open(temp_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            try:
                # Transcribe audio
                result = TranscriptionService._model.transcribe(temp_path)
                transcript = result["text"]
                
                return transcript
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Transcription error: {str(e)}"
            ) 
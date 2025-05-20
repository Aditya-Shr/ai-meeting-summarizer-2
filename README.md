# AI Meeting Summarizer

An intelligent system that transcribes, summarizes, and tracks meetings using AI.

## Features

- Audio file transcription
- Meeting summarization
- Action item extraction
- Decision tracking
- Calendar integration
- RESTful API

## Backend Setup

### Prerequisites

- Python 3.8+
- SQLite
- FFmpeg (for audio processing)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-meeting-summarizer.git
cd ai-meeting-summarizer
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file in the backend directory
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your_secret_key
HUGGINGFACE_CACHE_DIR=./.cache/huggingface
```

4. Initialize the database:
```bash
python create_db.py
```

### Running the Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Meetings
- `POST /api/meetings/` - Create a new meeting
- `GET /api/meetings/` - List all meetings
- `GET /api/meetings/{meeting_id}` - Get meeting details
- `PUT /api/meetings/{meeting_id}` - Update meeting
- `DELETE /api/meetings/{meeting_id}` - Delete meeting
- `POST /api/meetings/{meeting_id}/upload-audio` - Upload meeting audio
- `POST /api/meetings/{meeting_id}/transcribe` - Transcribe meeting
- `POST /api/meetings/{meeting_id}/summarize` - Summarize meeting
- `POST /api/meetings/{meeting_id}/schedule` - Schedule meeting

### Action Items
- `POST /api/action-items/` - Create action item
- `GET /api/action-items/` - List action items
- `GET /api/action-items/{id}` - Get action item details
- `PUT /api/action-items/{id}` - Update action item
- `DELETE /api/action-items/{id}` - Delete action item

### Decisions
- `POST /api/decisions/` - Create decision
- `GET /api/decisions/` - List decisions
- `GET /api/decisions/{id}` - Get decision details
- `PUT /api/decisions/{id}` - Update decision
- `DELETE /api/decisions/{id}` - Delete decision

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | Database connection string | sqlite:///./app.db |
| SECRET_KEY | Application secret key | - |
| HUGGINGFACE_CACHE_DIR | Cache directory for HuggingFace models | ./.cache/huggingface |
| ALLOWED_ORIGINS | CORS allowed origins | * |

## Development

### Running Tests
```bash
cd backend
pytest
```

### Code Style
The project uses:
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

## Deployment

The application is configured for deployment on Render. The deployment process is automated through the `render.yaml` configuration file.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Downloading Models

This project uses Hugging Face and Whisper models.  
They will be automatically downloaded the first time you run the backend, or you can manually download them using:

    python -c "import whisper; whisper.load_model('base')"
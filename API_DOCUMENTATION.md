# API Documentation

## Authentication

Currently, the API does not require authentication. This will be implemented in future versions.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://ai-meeting-summarizer.onrender.com`

## API Endpoints

### Meetings

#### Create Meeting
```http
POST /api/meetings/
```

Request Body:
```json
{
  "title": "Project Kickoff",
  "description": "Initial project planning meeting",
  "date": "2024-03-20T10:00:00Z",
  "duration": 60,
  "participants": ["john@example.com", "jane@example.com"],
  "status": "scheduled"
}
```

Response:
```json
{
  "id": 1,
  "title": "Project Kickoff",
  "description": "Initial project planning meeting",
  "date": "2024-03-20T10:00:00Z",
  "duration": 60,
  "participants": ["john@example.com", "jane@example.com"],
  "status": "scheduled",
  "audio_file_path": null,
  "transcript": null,
  "summary": null,
  "created_at": "2024-03-20T10:00:00Z",
  "updated_at": null
}
```

#### List Meetings
```http
GET /api/meetings/
```

Query Parameters:
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)
- `status` (optional): Filter by meeting status (e.g., "scheduled", "in_progress", "completed")
- `date_from` (optional): Filter meetings after this date (ISO format)
- `date_to` (optional): Filter meetings before this date (ISO format)

Response:
```json
[
  {
    "id": 1,
    "title": "Project Kickoff",
    "description": "Initial project planning meeting",
    "date": "2024-03-20T10:00:00Z",
    "duration": 60,
    "participants": ["john@example.com", "jane@example.com"],
    "status": "scheduled",
    "audio_file_path": null,
    "transcript": null,
    "summary": null,
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": null
  }
]
```

#### Get Meeting Details
```http
GET /api/meetings/{meeting_id}
```

Response:
```json
{
  "id": 1,
  "title": "Project Kickoff",
  "description": "Initial project planning meeting",
  "date": "2024-03-20T10:00:00Z",
  "duration": 60,
  "participants": ["john@example.com", "jane@example.com"],
  "status": "scheduled",
  "audio_file_path": "uploads/meeting_1/audio.mp3",
  "transcript": "Meeting transcript text...",
  "summary": "Meeting summary text...",
  "created_at": "2024-03-20T10:00:00Z",
  "updated_at": "2024-03-21T09:00:00Z"
}
```

#### Upload Audio
```http
POST /api/meetings/{meeting_id}/upload-audio
```

Request:
- Content-Type: multipart/form-data
- Body: audio file

Response:
```json
{
  "message": "Audio file uploaded successfully",
  "file_path": "uploads/meeting_1/audio.mp3"
}
```

#### Transcribe Meeting
```http
POST /api/meetings/{meeting_id}/transcribe
```

Query Parameters:
- `provider` (optional): Transcription provider ("huggingface" or "whisper")

Response:
```json
{
  "message": "Transcription completed",
  "transcript": "Meeting transcript text..."
}
```

#### Summarize Meeting
```http
POST /api/meetings/{meeting_id}/summarize
```

Response:
```json
{
  "message": "Summarization completed",
  "summary": "Meeting summary text...",
  "action_items": [
    {
      "title": "Action item 1",
      "description": "Description of action item 1",
      "assignee": "john@example.com",
      "due_date": "2024-03-27"
    }
  ],
  "decisions": [
    {
      "title": "Decision 1",
      "description": "Description of decision 1",
      "decision_maker": "jane@example.com"
    }
  ]
}
```

#### Update Meeting
```http
PUT /api/meetings/{meeting_id}
```

Request Body (all fields are optional):
```json
{
  "title": "Updated Project Kickoff",
  "description": "Updated meeting description",
  "date": "2024-03-21T10:00:00Z",
  "duration": 90,
  "participants": ["john@example.com", "jane@example.com", "bob@example.com"],
  "status": "in_progress",
  "audio_file_path": "path/to/audio.mp3",
  "transcript": "Updated transcript text...",
  "summary": "Updated summary text..."
}
```

Response:
```json
{
  "id": 1,
  "title": "Updated Project Kickoff",
  "description": "Updated meeting description",
  "date": "2024-03-21T10:00:00Z",
  "duration": 90,
  "participants": ["john@example.com", "jane@example.com", "bob@example.com"],
  "status": "in_progress",
  "audio_file_path": "path/to/audio.mp3",
  "transcript": "Updated transcript text...",
  "summary": "Updated summary text...",
  "created_at": "2024-03-20T10:00:00Z",
  "updated_at": "2024-03-21T09:00:00Z"
}
```

Note: Only the fields you want to update need to be included in the request body. Fields not included will remain unchanged.

### Action Items

#### Create Action Item
```http
POST /api/action-items/
```

Request Body:
```json
{
  "meeting_id": 1,
  "title": "Setup development environment",
  "description": "Install required tools and dependencies",
  "assignee": "john@example.com",
  "due_date": "2024-03-27"
}
```

Response:
```json
{
  "id": 1,
  "meeting_id": 1,
  "title": "Setup development environment",
  "description": "Install required tools and dependencies",
  "assignee": "john@example.com",
  "due_date": "2024-03-27",
  "status": "pending"
}
```

#### List Action Items
```http
GET /api/action-items/
```

Query Parameters:
- `meeting_id` (optional): Filter by meeting ID
- `skip` (optional): Number of records to skip
- `limit` (optional): Maximum number of records to return

Response:
```json
[
  {
    "id": 1,
    "meeting_id": 1,
    "title": "Setup development environment",
    "description": "Install required tools and dependencies",
    "assignee": "john@example.com",
    "due_date": "2024-03-27",
    "status": "pending"
  }
]
```

### Decisions

#### Create Decision
```http
POST /api/decisions/
```

Request Body:
```json
{
  "meeting_id": 1,
  "title": "Project Timeline",
  "description": "Project will be completed in 3 months",
  "decision_maker": "jane@example.com",
  "rationale": "Based on team capacity and requirements"
}
```

Response:
```json
{
  "id": 1,
  "meeting_id": 1,
  "title": "Project Timeline",
  "description": "Project will be completed in 3 months",
  "decision_maker": "jane@example.com",
  "rationale": "Based on team capacity and requirements"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. This will be added in future versions.

## CORS

The API supports CORS and allows requests from any origin by default. This can be configured using the `ALLOWED_ORIGINS` environment variable. 
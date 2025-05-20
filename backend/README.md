# AI Meeting Summarizer Backend

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Calendar API credentials:
   - Go to the Google Cloud Console
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials and save as `credentials.json` in the backend directory
   - Note: Never commit `credentials.json` or `token.pickle` to version control

3. Initialize the database:
```bash
python create_db.py
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## Important Notes

- The `credentials.json` and `token.pickle` files contain sensitive information and should never be committed to version control
- Use `credentials.json.example` as a template for setting up your credentials
- The database file (`meetings.db`) is also excluded from version control as it may contain sensitive meeting information 
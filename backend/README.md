# AI Meeting Summarizer Backend

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
   - Create a `.env` file in the backend directory
   - Add the following variables:
   ```
   DATABASE_URL=sqlite:///./app.db
   SECRET_KEY=your_secret_key
   HUGGINGFACE_CACHE_DIR=./.cache/huggingface
   ```
   - To generate a secure SECRET_KEY, you can use Python:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   - Copy the generated key and replace `your_secret_key` in the `.env` file

3. Set up Google Calendar API credentials:
   - Go to the Google Cloud Console
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials and save as `credentials.json` in the backend directory
   - Note: Never commit `credentials.json` or `token.pickle` to version control

4. Initialize the database:
```bash
python create_db.py
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## Important Notes

- The `credentials.json` and `token.pickle` files contain sensitive information and should never be committed to version control
- Use `credentials.json.example` as a template for setting up your credentials
- The database file (`meetings.db`) is also excluded from version control as it may contain sensitive meeting information
- Keep your SECRET_KEY secure and never commit it to version control
- If you need to change the SECRET_KEY, make sure to update it in the `.env` file 
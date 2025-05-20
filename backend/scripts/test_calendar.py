"""
Test script to verify Google Calendar API credentials
"""

import os
import sys
import pickle
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.pickle'

def find_credentials():
    """Find credentials.json file"""
    credentials_paths = [
        'credentials.json',
        os.path.join(os.getcwd(), 'credentials.json'),
        os.path.join(os.path.dirname(os.getcwd()), 'credentials.json'),
        os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
    ]
    
    for path in credentials_paths:
        if os.path.exists(path):
            print(f"Found credentials at: {path}")
            return path
    
    print("No credentials.json file found! Please create one.")
    return None

def get_credentials():
    """Get or refresh Google Calendar credentials"""
    creds = None
    
    # Find credentials.json
    credentials_file = find_credentials()
    if not credentials_file:
        return None
    
    # Load token from file if it exists
    if os.path.exists(TOKEN_FILE):
        try:
            print(f"Loading existing token from {TOKEN_FILE}")
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
            print("Token loaded successfully")
        except Exception as e:
            print(f"Error loading token: {str(e)}")
    
    # If credentials don't exist or are invalid, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing expired token")
                creds.refresh(Request())
                print("Token refreshed successfully")
            except Exception as e:
                print(f"Error refreshing token: {str(e)}")
                return None
        else:
            try:
                print("Creating new token flow")
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
                print("Authorization flow completed successfully")
            except Exception as e:
                print(f"Error in authorization flow: {str(e)}")
                return None
        
        # Save credentials for future use
        try:
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
            print(f"Token saved to {TOKEN_FILE}")
        except Exception as e:
            print(f"Error saving token: {str(e)}")
    
    return creds

def test_calendar_api():
    """Test Google Calendar API by listing upcoming events"""
    creds = get_credentials()
    if not creds:
        print("Failed to get credentials. Cannot test Calendar API.")
        return
    
    try:
        print("Building calendar service")
        service = build('calendar', 'v3', credentials=creds)
        
        # Get current time in UTC
        now = datetime.utcnow().isoformat() + 'Z'
        print(f"Fetching events from {now}")
        
        # Get events
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            print("No upcoming events found.")
        else:
            print("Upcoming events:")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f" - {start}: {event['summary']}")
        
        # Try creating a test event
        start_time = datetime.utcnow() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        print(f"Creating test event at {start_time}")
        test_event = {
            'summary': 'Test Calendar API Event',
            'description': 'This is a test event created by the test script',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            }
        }
        
        event = service.events().insert(
            calendarId='primary',
            body=test_event
        ).execute()
        
        print(f"Test event created: {event.get('htmlLink')}")
        
        # Clean up by deleting the test event
        service.events().delete(
            calendarId='primary',
            eventId=event['id']
        ).execute()
        
        print("Test event deleted")
        print("Calendar API test completed successfully!")
        
    except Exception as e:
        print(f"Error testing Calendar API: {str(e)}")

if __name__ == "__main__":
    print("Running Google Calendar API test")
    test_calendar_api() 
import os
import datetime
from datetime import datetime as dt  # Add specific datetime import
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from fastapi import HTTPException
from app.core.config import settings
import json
import pickle
from typing import List, Dict, Any, Optional

class CalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    TOKEN_FILE = 'token.pickle'
    CREDENTIALS_FILE = 'credentials.json'

    @staticmethod
    def _get_credentials() -> Credentials:
        """Get or refresh Google Calendar credentials"""
        creds = None
        
        # Look for credentials in multiple locations
        credentials_paths = [
            CalendarService.CREDENTIALS_FILE,
            os.path.join(os.getcwd(), CalendarService.CREDENTIALS_FILE),
            os.path.join(os.path.dirname(os.getcwd()), CalendarService.CREDENTIALS_FILE)
        ]
        
        credentials_file = None
        for path in credentials_paths:
            if os.path.exists(path):
                credentials_file = path
                break
        
        # Load token from file if it exists
        if os.path.exists(CalendarService.TOKEN_FILE):
            try:
                with open(CalendarService.TOKEN_FILE, 'rb') as token:
                    creds = pickle.load(token)
            except Exception as e:
                print(f"Error loading credentials: {str(e)}")
        
        # If credentials don't exist or are invalid, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {str(e)}")
            else:
                if not credentials_file:
                    raise HTTPException(
                        status_code=500,
                        detail="Google Calendar credentials not found. Please place your desktop app credentials.json in the backend directory"
                    )
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_file,
                        CalendarService.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error creating credentials flow: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error creating credentials flow: {str(e)}"
                    )
            
            # Save credentials for future use
            try:
                with open(CalendarService.TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
            except Exception as e:
                print(f"Error saving credentials: {str(e)}")
        
        return creds

    @staticmethod
    def _get_calendar_service():
        """Get Google Calendar service instance"""
        try:
            creds = CalendarService._get_credentials()
            service = build('calendar', 'v3', credentials=creds)
            return service
        except Exception as e:
            print(f"Error creating calendar service: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error creating calendar service: {str(e)}"
            )

    @staticmethod
    def create_meeting_event(
        summary: str,
        description: str,
        start_time: datetime,
        end_time: datetime,
        attendees: Optional[List[Dict[str, str]]] = None,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a calendar event for a meeting"""
        try:
            service = CalendarService._get_calendar_service()
            
            # Prepare event details
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            # Add attendees if provided
            if attendees:
                event['attendees'] = [
                    {'email': attendee['email']} for attendee in attendees
                ]
            
            # Add location if provided
            if location:
                event['location'] = location
            
            # Create the event
            event = service.events().insert(
                calendarId='primary',
                body=event,
                sendUpdates='all'
            ).execute()
            
            return {
                'event_id': event['id'],
                'html_link': event['htmlLink'],
                'meet_link': event.get('hangoutLink'),
                'start_time': event['start']['dateTime'],
                'end_time': event['end']['dateTime']
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating calendar event: {str(e)}"
            )

    @staticmethod
    def get_upcoming_meetings(max_results: int = 10) -> List[Dict[str, Any]]:
        """Get upcoming calendar events"""
        try:
            service = CalendarService._get_calendar_service()
            
            # Get current time in UTC
            now = dt.utcnow().isoformat() + 'Z'  # Use dt instead of datetime.utcnow
            
            # Get events
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Format events
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                formatted_events.append({
                    'id': event['id'],
                    'summary': event['summary'],
                    'description': event.get('description', ''),
                    'start_time': start,
                    'end_time': end,
                    'html_link': event['htmlLink'],
                    'meet_link': event.get('hangoutLink'),
                    'attendees': [
                        attendee['email'] for attendee in event.get('attendees', [])
                    ]
                })
            
            return formatted_events
            
        except Exception as e:
            print(f"Error retrieving calendar events: {str(e)}")  # Add debug print
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving calendar events: {str(e)}"
            )

    @staticmethod
    def update_meeting_event(
        event_id: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        attendees: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Update an existing calendar event"""
        try:
            service = CalendarService._get_calendar_service()
            
            # Get existing event
            event = service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            # Update fields if provided
            if summary:
                event['summary'] = summary
            if description:
                event['description'] = description
            if start_time:
                event['start']['dateTime'] = start_time.isoformat()
            if end_time:
                event['end']['dateTime'] = end_time.isoformat()
            if attendees:
                event['attendees'] = [
                    {'email': attendee['email']} for attendee in attendees
                ]
            
            # Update the event
            updated_event = service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event,
                sendUpdates='all'
            ).execute()
            
            return {
                'event_id': updated_event['id'],
                'html_link': updated_event['htmlLink'],
                'meet_link': updated_event.get('hangoutLink'),
                'start_time': updated_event['start']['dateTime'],
                'end_time': updated_event['end']['dateTime']
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error updating calendar event: {str(e)}"
            )

    @staticmethod
    def delete_meeting_event(event_id: str) -> bool:
        """Delete a calendar event"""
        try:
            service = CalendarService._get_calendar_service()
            
            service.events().delete(
                calendarId='primary',
                eventId=event_id,
                sendUpdates='all'
            ).execute()
            
            return True
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting calendar event: {str(e)}"
            ) 
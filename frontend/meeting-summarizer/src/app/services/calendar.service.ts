import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CalendarEvent {
  event_id: string;
  html_link: string;
  meet_link?: string;
  start_time: string;
  end_time: string;
}

@Injectable({
  providedIn: 'root'
})
export class CalendarService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  // Schedule a meeting
  scheduleMeeting(
    meetingId: number,
    startTime: string,
    endTime: string,
    attendees: { email: string }[]
  ): Observable<CalendarEvent> {
    return this.http.post<CalendarEvent>(`${this.apiUrl}/meetings/${meetingId}/schedule`, {
      start_time: startTime,
      end_time: endTime,
      attendees
    });
  }

  // Get upcoming meetings
  getUpcomingMeetings(): Observable<CalendarEvent[]> {
    return this.http.get<CalendarEvent[]>(`${this.apiUrl}/meetings/calendar/upcoming`);
  }

  // Update a calendar event
  updateEvent(
    eventId: string,
    updates: {
      summary?: string;
      description?: string;
      start_time?: string;
      end_time?: string;
      attendees?: { email: string }[];
    }
  ): Observable<CalendarEvent> {
    return this.http.put<CalendarEvent>(`${this.apiUrl}/meetings/calendar/events/${eventId}`, updates);
  }

  // Delete a calendar event
  deleteEvent(eventId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/meetings/calendar/events/${eventId}`);
  }
} 
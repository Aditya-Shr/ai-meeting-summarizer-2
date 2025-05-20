import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Meeting {
  id: number;
  title: string;
  description: string;
  transcript?: string;
  summary?: string;
  action_items?: any[];
  decisions?: any[];
  created_at: string;
  updated_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class MeetingService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  // Get all meetings
  getMeetings(): Observable<Meeting[]> {
    return this.http.get<Meeting[]>(`${this.apiUrl}/meetings`);
  }

  // Get a single meeting
  getMeeting(id: number): Observable<Meeting> {
    return this.http.get<Meeting>(`${this.apiUrl}/meetings/${id}`);
  }

  // Create a new meeting
  createMeeting(meeting: Partial<Meeting>): Observable<Meeting> {
    return this.http.post<Meeting>(`${this.apiUrl}/meetings`, meeting);
  }

  // Upload audio for a meeting
  uploadAudio(meetingId: number, audioFile: File): Observable<any> {
    const formData = new FormData();
    formData.append('audio', audioFile);
    return this.http.post(`${this.apiUrl}/meetings/${meetingId}/audio`, formData);
  }

  // Transcribe audio for a meeting
  transcribeAudio(meetingId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/meetings/${meetingId}/transcribe`, {});
  }

  // Get transcript for a meeting
  getTranscript(meetingId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/meetings/${meetingId}/transcript`);
  }

  // Generate summary for a meeting
  generateSummary(meetingId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/meetings/${meetingId}/summarize`, {});
  }

  // Get action items for a meeting
  getActionItems(meetingId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/meetings/${meetingId}/action-items`);
  }

  // Get decisions for a meeting
  getDecisions(meetingId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/meetings/${meetingId}/decisions`);
  }

  // Delete a meeting
  deleteMeeting(meetingId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/meetings/${meetingId}`);
  }
} 
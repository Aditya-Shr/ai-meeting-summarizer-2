import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MeetingService, Meeting } from '../../services/meeting.service';

@Component({
  selector: 'app-meeting-list',
  template: `
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Meetings</h2>
        <button class="btn btn-primary" (click)="createNewMeeting()">New Meeting</button>
      </div>

      <div class="row">
        <div class="col-md-4 mb-4" *ngFor="let meeting of meetings">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ meeting.title }}</h5>
              <p class="card-text">{{ meeting.description }}</p>
              <div class="d-flex justify-content-between">
                <button class="btn btn-info" (click)="viewMeeting(meeting.id)">View Details</button>
                <button class="btn btn-danger" (click)="deleteMeeting(meeting.id)">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .card {
      height: 100%;
      transition: transform 0.2s;
    }
    .card:hover {
      transform: translateY(-5px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
  `]
})
export class MeetingListComponent implements OnInit {
  meetings: Meeting[] = [];

  constructor(
    private meetingService: MeetingService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadMeetings();
  }

  loadMeetings(): void {
    this.meetingService.getMeetings().subscribe(
      meetings => this.meetings = meetings,
      error => console.error('Error loading meetings:', error)
    );
  }

  createNewMeeting(): void {
    this.router.navigate(['/meetings/create']);
  }

  viewMeeting(id: number): void {
    this.router.navigate(['/meetings', id]);
  }

  deleteMeeting(id: number): void {
    if (confirm('Are you sure you want to delete this meeting?')) {
      this.meetingService.deleteMeeting(id).subscribe(
        () => {
          this.meetings = this.meetings.filter(m => m.id !== id);
        },
        error => console.error('Error deleting meeting:', error)
      );
    }
  }
} 
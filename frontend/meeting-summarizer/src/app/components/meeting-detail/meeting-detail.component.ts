import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MeetingService, Meeting } from '../../services/meeting.service';
import { CalendarService } from '../../services/calendar.service';

@Component({
  selector: 'app-meeting-detail',
  template: `
    <div class="container mt-4" *ngIf="meeting">
      <div class="row">
        <div class="col-md-8">
          <h2>{{ meeting.title }}</h2>
          <p class="text-muted">{{ meeting.description }}</p>
          
          <!-- Audio Upload Section -->
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">Audio Recording</h5>
              <input type="file" class="form-control mb-2" (change)="onFileSelected($event)" accept="audio/*">
              <button class="btn btn-primary" (click)="uploadAudio()" [disabled]="!selectedFile">Upload Audio</button>
              <button class="btn btn-info" (click)="transcribeAudio()" [disabled]="!meeting.audio_file">Transcribe</button>
            </div>
          </div>

          <!-- Transcript Section -->
          <div class="card mb-4" *ngIf="meeting.transcript">
            <div class="card-body">
              <h5 class="card-title">Transcript</h5>
              <p class="card-text">{{ meeting.transcript }}</p>
              <button class="btn btn-primary" (click)="generateSummary()">Generate Summary</button>
            </div>
          </div>

          <!-- Summary Section -->
          <div class="card mb-4" *ngIf="meeting.summary">
            <div class="card-body">
              <h5 class="card-title">Summary</h5>
              <p class="card-text">{{ meeting.summary }}</p>
            </div>
          </div>

          <!-- Action Items Section -->
          <div class="card mb-4" *ngIf="meeting.action_items?.length">
            <div class="card-body">
              <h5 class="card-title">Action Items</h5>
              <ul class="list-group">
                <li class="list-group-item" *ngFor="let item of meeting.action_items">
                  {{ item.description }} - {{ item.owner }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Decisions Section -->
          <div class="card mb-4" *ngIf="meeting.decisions?.length">
            <div class="card-body">
              <h5 class="card-title">Decisions</h5>
              <ul class="list-group">
                <li class="list-group-item" *ngFor="let decision of meeting.decisions">
                  {{ decision.description }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Calendar Integration -->
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Schedule Meeting</h5>
              <form (ngSubmit)="scheduleMeeting()">
                <div class="mb-3">
                  <label class="form-label">Start Time</label>
                  <input type="datetime-local" class="form-control" [(ngModel)]="startTime" name="startTime" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">End Time</label>
                  <input type="datetime-local" class="form-control" [(ngModel)]="endTime" name="endTime" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">Attendees (one per line)</label>
                  <textarea class="form-control" [(ngModel)]="attendees" name="attendees" rows="3" placeholder="email@example.com"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Schedule</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .card {
      margin-bottom: 1rem;
    }
    .list-group-item {
      border-left: none;
      border-right: none;
    }
  `]
})
export class MeetingDetailComponent implements OnInit {
  meeting: Meeting | null = null;
  selectedFile: File | null = null;
  startTime: string = '';
  endTime: string = '';
  attendees: string = '';

  constructor(
    private route: ActivatedRoute,
    private meetingService: MeetingService,
    private calendarService: CalendarService
  ) { }

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadMeeting(id);
  }

  loadMeeting(id: number): void {
    this.meetingService.getMeeting(id).subscribe(
      meeting => this.meeting = meeting,
      error => console.error('Error loading meeting:', error)
    );
  }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  uploadAudio(): void {
    if (this.selectedFile && this.meeting) {
      this.meetingService.uploadAudio(this.meeting.id, this.selectedFile).subscribe(
        () => {
          this.loadMeeting(this.meeting!.id);
          this.selectedFile = null;
        },
        error => console.error('Error uploading audio:', error)
      );
    }
  }

  transcribeAudio(): void {
    if (this.meeting) {
      this.meetingService.transcribeAudio(this.meeting.id).subscribe(
        () => this.loadMeeting(this.meeting!.id),
        error => console.error('Error transcribing audio:', error)
      );
    }
  }

  generateSummary(): void {
    if (this.meeting) {
      this.meetingService.generateSummary(this.meeting.id).subscribe(
        () => this.loadMeeting(this.meeting!.id),
        error => console.error('Error generating summary:', error)
      );
    }
  }

  scheduleMeeting(): void {
    if (this.meeting && this.startTime && this.endTime) {
      const attendeeList = this.attendees
        .split('\n')
        .map(email => email.trim())
        .filter(email => email)
        .map(email => ({ email }));

      this.calendarService.scheduleMeeting(
        this.meeting.id,
        this.startTime,
        this.endTime,
        attendeeList
      ).subscribe(
        () => {
          alert('Meeting scheduled successfully!');
          this.startTime = '';
          this.endTime = '';
          this.attendees = '';
        },
        error => console.error('Error scheduling meeting:', error)
      );
    }
  }
} 
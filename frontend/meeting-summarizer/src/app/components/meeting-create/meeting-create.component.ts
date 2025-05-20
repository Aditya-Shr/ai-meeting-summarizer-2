import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MeetingService } from '../../services/meeting.service';

@Component({
  selector: 'app-meeting-create',
  template: `
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
            <div class="card-body">
              <h2 class="card-title">Create New Meeting</h2>
              <form (ngSubmit)="createMeeting()">
                <div class="mb-3">
                  <label for="title" class="form-label">Title</label>
                  <input
                    type="text"
                    class="form-control"
                    id="title"
                    [(ngModel)]="title"
                    name="title"
                    required
                  >
                </div>
                <div class="mb-3">
                  <label for="description" class="form-label">Description</label>
                  <textarea
                    class="form-control"
                    id="description"
                    [(ngModel)]="description"
                    name="description"
                    rows="3"
                    required
                  ></textarea>
                </div>
                <div class="d-flex justify-content-between">
                  <button type="button" class="btn btn-secondary" (click)="goBack()">Cancel</button>
                  <button type="submit" class="btn btn-primary">Create Meeting</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .card {
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
  `]
})
export class MeetingCreateComponent {
  title: string = '';
  description: string = '';

  constructor(
    private meetingService: MeetingService,
    private router: Router
  ) { }

  createMeeting(): void {
    this.meetingService.createMeeting({
      title: this.title,
      description: this.description
    }).subscribe(
      meeting => {
        this.router.navigate(['/meetings', meeting.id]);
      },
      error => console.error('Error creating meeting:', error)
    );
  }

  goBack(): void {
    this.router.navigate(['/meetings']);
  }
} 
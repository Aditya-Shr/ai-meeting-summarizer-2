import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MeetingListComponent } from './components/meeting-list/meeting-list.component';
import { MeetingDetailComponent } from './components/meeting-detail/meeting-detail.component';
import { MeetingCreateComponent } from './components/meeting-create/meeting-create.component';

const routes: Routes = [
  { path: '', redirectTo: '/meetings', pathMatch: 'full' },
  { path: 'meetings', component: MeetingListComponent },
  { path: 'meetings/create', component: MeetingCreateComponent },
  { path: 'meetings/:id', component: MeetingDetailComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { } 
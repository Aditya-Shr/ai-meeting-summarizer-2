import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MeetingListComponent } from './components/meeting-list/meeting-list.component';
import { MeetingDetailComponent } from './components/meeting-detail/meeting-detail.component';
import { MeetingCreateComponent } from './components/meeting-create/meeting-create.component';

@NgModule({
  declarations: [
    AppComponent,
    MeetingListComponent,
    MeetingDetailComponent,
    MeetingCreateComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { } 
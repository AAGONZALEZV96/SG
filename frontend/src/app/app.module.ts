import { NgModule } from "@angular/core"
import { BrowserModule } from "@angular/platform-browser"
import { ReactiveFormsModule } from "@angular/forms"
import { HttpClientModule } from "@angular/common/http"

import { AppRoutingModule } from "./app-routing.module"
import { AppComponent } from "./app.component"
import { LoginComponent } from "./components/login/login.component"
import { RegisterComponent } from "./components/register/register.component"
import { ProfileComponent } from "./components/profile/profile.component"
import { StudentDashboardComponent } from "./components/student-dashboard/student-dashboard.component"

@NgModule({
  declarations: [AppComponent, LoginComponent, RegisterComponent, ProfileComponent, StudentDashboardComponent],
  imports: [BrowserModule, AppRoutingModule, ReactiveFormsModule, HttpClientModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}

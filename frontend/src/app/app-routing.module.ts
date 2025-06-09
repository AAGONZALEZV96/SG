import { NgModule } from "@angular/core"
import { RouterModule, type Routes } from "@angular/router"
import { LoginComponent } from "./components/login/login.component"
import { RegisterComponent } from "./components/register/register.component"
import { ProfileComponent } from "./components/profile/profile.component"
import { StudentDashboardComponent } from "./components/student-dashboard/student-dashboard.component"
import { AuthGuard } from "./guards/auth.guard"

const routes: Routes = [
  { path: "", redirectTo: "/login", pathMatch: "full" },
  { path: "login", component: LoginComponent },
  {
    path: "register",
    component: RegisterComponent,
    canActivate: [AuthGuard],
    data: { role: "admin" },
  },
  {
    path: "profile",
    component: ProfileComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard",
    component: StudentDashboardComponent,
    canActivate: [AuthGuard],
  },
  { path: "**", redirectTo: "/login" },
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}

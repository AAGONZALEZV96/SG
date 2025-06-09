import { Component,  OnInit } from "@angular/core"
import  { AuthService } from "../../services/auth.service"
import  { User } from "../../models/user.model"
import  { Grade } from "../../models/grade.model"
import { Router } from "@angular/router"

@Component({
  selector: "app-student-dashboard",
  templateUrl: "./student-dashboard.component.html",
  styleUrls: ["./student-dashboard.component.css"],
})
export class StudentDashboardComponent implements OnInit {
  currentUser: User | null = null
  courseProgress = 75
  attendanceCount = 18
  totalClasses = 24
  recentGrades: Grade[] = []

  constructor(
    public authService: AuthService,
    public router: Router) {}

  ngOnInit(): void {
    this.currentUser = this.authService.currentUserValue
    this.loadRecentGrades()
  }

  loadRecentGrades(): void {
    // Mock data - replace with actual API call
    this.recentGrades = [
      {
        id: "1",
        studentId: this.currentUser?.userId || "",
        studentName: this.currentUser?.name || "",
        subject: "Matemáticas",
        grade: 6.5,
        comment: "Excelente trabajo",
        date: "2024-01-15",
      },
      {
        id: "2",
        studentId: this.currentUser?.userId || "",
        studentName: this.currentUser?.name || "",
        subject: "Ciencias",
        grade: 6.0,
        comment: "Muy bien",
        date: "2024-01-12",
      },
      {
        id: "3",
        studentId: this.currentUser?.userId || "",
        studentName: this.currentUser?.name || "",
        subject: "Historia",
        grade: 5.8,
        comment: "Buen esfuerzo",
        date: "2024-01-10",
      },
      {
        id: "4",
        studentId: this.currentUser?.userId || "",
        studentName: this.currentUser?.name || "",
        subject: "Literatura",
        grade: 5.2,
        comment: "Mejorando",
        date: "2024-01-08",
      },
      {
        id: "5",
        studentId: this.currentUser?.userId || "",
        studentName: this.currentUser?.name || "",
        subject: "Inglés",
        grade: 6.2,
        comment: "Excelente",
        date: "2024-01-05",
      },
    ]
  }

  get attendancePercentage(): number {
    return Math.round((this.attendanceCount / this.totalClasses) * 100)
  }

  getGradeColor(grade: number): string {
    if (grade >= 7) return "#28a745"
    if (grade >= 4) return "#ffc107"
    return "#dc3545"
  }
}

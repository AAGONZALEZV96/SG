import { Injectable } from "@angular/core"
import  { HttpClient } from "@angular/common/http"
import { BehaviorSubject, Observable } from "rxjs"
import  { User, LoginRequest } from "../models/user.model"

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private currentUserSubject: BehaviorSubject<User | null>
  public currentUser: Observable<User | null>
  private apiUrl = "https://your-api-gateway-url.com" // Replace with your actual API URL

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<User | null>(
      JSON.parse(localStorage.getItem("currentUser") || "null"),
    )
    this.currentUser = this.currentUserSubject.asObservable()
  }

  public get currentUserValue(): User | null {
    return this.currentUserSubject.value
  }

  login(credentials: LoginRequest): Observable<User> {
    // Mock login - replace with actual API call
    return new Observable((observer) => {
      setTimeout(() => {
        const mockUser: User = {
          userId: "1",
          name: "Usuario Demo",
          email: credentials.email,
          role: credentials.email.includes("admin")
            ? "admin"
            : credentials.email.includes("teacher")
              ? "teacher"
              : "student",
        }

        localStorage.setItem("currentUser", JSON.stringify(mockUser))
        this.currentUserSubject.next(mockUser)
        observer.next(mockUser)
        observer.complete()
      }, 1000)
    })
  }

  logout(): void {
    localStorage.removeItem("currentUser")
    this.currentUserSubject.next(null)
  }

  isAuthenticated(): boolean {
    return !!this.currentUserValue
  }

  hasRole(role: string): boolean {
    const user = this.currentUserValue
    return user ? user.role === role : false
  }
}

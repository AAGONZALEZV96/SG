import { Injectable } from "@angular/core"
import  { HttpClient } from "@angular/common/http"
import {  Observable, of } from "rxjs"
import  { User, RegisterRequest } from "../models/user.model"

@Injectable({
  providedIn: "root",
})
export class UserService {
  private apiUrl = "https://your-api-gateway-url.com" // Replace with your actual API URL

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    // Mock data - replace with actual API call
    const mockUsers: User[] = [
      { userId: "1", name: "Ana García", email: "ana@example.com", role: "teacher", phone: "123456789" },
      { userId: "2", name: "Carlos López", email: "carlos@example.com", role: "student", phone: "987654321" },
      { userId: "3", name: "María Rodríguez", email: "maria@example.com", role: "student", phone: "456789123" },
    ]
    return of(mockUsers)
  }

  getUserById(id: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/${id}`)
  }

  createUser(user: RegisterRequest): Observable<User> {
    // Mock creation - replace with actual API call
    const newUser: User = {
      userId: Date.now().toString(),
      name: user.name,
      email: user.email,
      role: user.role,
      phone: user.phone,
    }
    return of(newUser)
  }

  updateUser(id: string, user: Partial<User>): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/users/${id}`, user)
  }

  deleteUser(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/users/${id}`)
  }
}

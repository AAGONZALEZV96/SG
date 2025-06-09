export interface User {
  userId: string
  name: string
  email: string
  role: "admin" | "teacher" | "student"
  phone?: string
  profilePicture?: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  name: string
  email: string
  password: string
  phone: string
  role: "teacher" | "student"
}

import { Component,  OnInit } from "@angular/core"
import {  FormBuilder,  FormGroup, Validators } from "@angular/forms"
import  { AuthService } from "../../services/auth.service"
import  { UserService } from "../../services/user.service"
import  { User } from "../../models/user.model"

@Component({
  selector: "app-profile",
  templateUrl: "./profile.component.html",
  styleUrls: ["./profile.component.css"],
})
export class ProfileComponent implements OnInit {
  profileForm: FormGroup
  currentUser: User | null = null
  loading = false
  editing = false
  success = ""
  error = ""

  constructor(
    public formBuilder: FormBuilder,
    public authService: AuthService,
    public userService: UserService,
  ) {
    this.profileForm = this.formBuilder.group({
      name: ["", [Validators.required, Validators.minLength(2)]],
      email: ["", [Validators.required, Validators.email]],
      phone: ["", [Validators.pattern(/^\d{9,}$/)]],
    })
  }

  ngOnInit(): void {
    this.currentUser = this.authService.currentUserValue
    if (this.currentUser) {
      this.profileForm.patchValue({
        name: this.currentUser.name,
        email: this.currentUser.email,
        phone: this.currentUser.phone || "",
      })
    }
  }

  get f() {
    return this.profileForm.controls
  }

  toggleEdit(): void {
    this.editing = !this.editing
    if (!this.editing) {
      // Reset form if canceling edit
      this.ngOnInit()
    }
  }

  onSubmit(): void {
    if (this.profileForm.invalid || !this.currentUser) {
      return
    }

    this.loading = true
    const updatedData = this.profileForm.value

    this.userService.updateUser(this.currentUser.userId, updatedData).subscribe({
      next: (updatedUser) => {
        this.success = "Perfil actualizado exitosamente"
        this.editing = false
        this.loading = false
        // Update current user in auth service
        const newUser = { ...this.currentUser!, ...updatedData }
        localStorage.setItem("currentUser", JSON.stringify(newUser))
      },
      error: (error) => {
        this.error = "Error al actualizar el perfil"
        this.loading = false
      },
    })
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0]
    if (file) {
      // Mock file upload - replace with actual implementation
      const reader = new FileReader()
      reader.onload = (e: any) => {
        if (this.currentUser) {
          this.currentUser.profilePicture = e.target.result
        }
      }
      reader.readAsDataURL(file)
    }
  }
}

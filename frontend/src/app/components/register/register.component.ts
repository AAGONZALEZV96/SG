import { Component,  OnInit } from "@angular/core"
import {  FormBuilder,  FormGroup, Validators } from "@angular/forms"
import  { Router } from "@angular/router"
import  { UserService } from "../../services/user.service"
import  { AuthService } from "../../services/auth.service"

@Component({
  selector: "app-register",
  templateUrl: "./register.component.html",
  styleUrls: ["./register.component.css"],
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup
  loading = false
  submitted = false
  error = ""
  success = ""

  constructor(
    public formBuilder: FormBuilder,
    public router: Router,
    public userService: UserService,
    public authService: AuthService,
  ) {
    this.registerForm = this.formBuilder.group({
      name: ["", [Validators.required, Validators.minLength(2)]],
      email: ["", [Validators.required, Validators.email]],
      password: ["", [Validators.required, Validators.minLength(6)]],
      phone: ["", [Validators.required, Validators.pattern(/^\d{9,}$/)]],
      role: ["student", Validators.required],
    })
  }

  ngOnInit(): void {
    // Only admin can access this component
    if (!this.authService.hasRole("admin")) {
      this.router.navigate(["/dashboard"])
    }
  }

  get f() {
    return this.registerForm.controls
  }

  onSubmit(): void {
    this.submitted = true

    if (this.registerForm.invalid) {
      return
    }

    this.loading = true
    this.userService.createUser(this.registerForm.value).subscribe({
      next: () => {
        this.success = "Usuario creado exitosamente"
        this.registerForm.reset()
        this.registerForm.patchValue({ role: "student" })
        this.submitted = false
        this.loading = false
      },
      error: (error) => {
        this.error = "Error al crear el usuario"
        this.loading = false
      },
    })
  }
}

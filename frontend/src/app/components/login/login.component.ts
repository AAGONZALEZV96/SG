import { Component,  OnInit } from "@angular/core"
import {  FormBuilder,  FormGroup, Validators } from "@angular/forms"
import  { Router, ActivatedRoute } from "@angular/router"
import  { AuthService } from "../../services/auth.service"

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
  styleUrls: ["./login.component.css"],
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup
  loading = false
  submitted = false
  error = ""
  returnUrl: string

  constructor(
    public formBuilder: FormBuilder,
    public route: ActivatedRoute,
    public router: Router,
    public authService: AuthService,
  ) {
    this.loginForm = this.formBuilder.group({
      email: ["", [Validators.required, Validators.email]],
      password: ["", [Validators.required, Validators.minLength(6)]],
    })

    this.returnUrl = this.route.snapshot.queryParams["returnUrl"] || "/dashboard"
  }

  ngOnInit(): void {
    if (this.authService.currentUserValue) {
      this.router.navigate([this.returnUrl])
    }
  }

  get f() {
    return this.loginForm.controls
  }

  onSubmit(): void {
    this.submitted = true

    if (this.loginForm.invalid) {
      return
    }

    this.loading = true
    this.authService.login(this.loginForm.value).subscribe({
      next: () => {
        this.router.navigate([this.returnUrl])
      },
      error: (error) => {
        this.error = "Email o contraseña incorrectos"
        this.loading = false
      },
    })
  }
}

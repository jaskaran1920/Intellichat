import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html'
})
export class LoginComponent {
  username = '';
  password = '';
  error = '';

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    // const headers = new HttpHeaders({
    //   'Content-Type': 'application/json'
    // });

    // console.log("🔐 Sending login:", this.username, this.password);

    // this.http.post<any>('http://127.0.0.1:5000/login', {
    //   username: this.username,
    //   password: this.password
    // }, { headers }).subscribe({
    //   next: (res) => {
    //     console.log("✅ Login success:", res);
    //     localStorage.setItem('token', res.access_token);
    //     this.router.navigate(['/chat']);
    //   },
    //   error: (err) => {
    //     console.error("❌ Login error:", err);
    //     this.error = err.error?.error || 'Invalid login';
    //   }
    // });
    this.router.navigate(['/chat']);  
  }
}

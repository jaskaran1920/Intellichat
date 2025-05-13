import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html'
})
export class ChatComponent {
  question = '';
  answer = '';
  error = '';

  constructor(private http: HttpClient) {}

  sendMessage() {
    const token = localStorage.getItem('token');
    if (!token) {
      this.error = 'Not authenticated';
      return;
    }

    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    this.http.post<any>('http://localhost:5000/chat', { question: this.question }, { headers })
      .subscribe({
        next: (res) => {
          this.answer = res.answer;
          this.error = '';
        },
        error: (err) => {
          this.error = 'Error: ' + (err.error?.message || 'Something went wrong');
        }
      });
  }
}

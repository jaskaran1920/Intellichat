import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent {
  question = '';
  answer = '';
  error = '';
  messages: { sender: 'user' | 'bot', text: string }[] = [];

  constructor(private http: HttpClient) {}

  sendMessage() {
    if (!this.question.trim()) return;
  
    // Add user message
    this.messages.push({ sender: 'user', text: this.question });
  
    this.http.post<any>('http://127.0.0.1:5000/chat', {
      question: this.question
    }).subscribe({
      next: (res) => {
        this.messages.push({ sender: 'bot', text: res.answer });
        this.question = '';
        this.error = '';
      },
      error: (err) => {
        this.error = err.error?.message || 'Something went wrong';
      }
    });
  }
  upgradeToPremium() {
    const user = 'guest';  // Replace with actual username/email if available
  
    this.http.post<any>(`http://127.0.0.1:5000/create-checkout-session?user=${user}`, {})
      .subscribe({
        next: (res) => {
          if (res.checkout_url) {
            window.location.href = res.checkout_url;
          } else {
            this.error = 'Payment failed. No checkout URL received.';
          }
        },
        error: (err) => {
          this.error = 'Payment failed. Please try again.';
          console.error(err);
        }
      });
  }
  
  
}

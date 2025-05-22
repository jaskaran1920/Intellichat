import { Component, OnInit } from '@angular/core';  // ✅ OnInit imported
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
export class ChatComponent implements OnInit {  // ✅ implements OnInit

  messageCount = 0;
  isPremium = false;
  maxFreeMessages = 4;
  question = '';
  answer = '';
  error = '';
  messages: { sender: 'user' | 'bot', text: string }[] = [];

  // 🔽 CSV upload
  selectedFile: File | null = null;
  uploadMessage = '';

  constructor(private http: HttpClient) {}

  // ✅ This runs automatically when component loads
  ngOnInit(): void {
    this.checkPremiumStatus();
  
    if (typeof window !== 'undefined') {
      const queryParams = new URLSearchParams(window.location.search);
      if (queryParams.get('premium') === 'success') {
        console.log("✅ Returned from Stripe. Rechecking premium status...");
        this.checkPremiumStatus(); // second check after Stripe
        window.history.replaceState({}, document.title, '/chat'); // remove query param
      }
    }
  }
  
  
  
  

  // 🔽 Handle sending message to Flask chatbot
  sendMessage() {
    if (!this.question.trim()) return;

    // 🔒 Check if free limit reached
    if (!this.isPremium && this.messageCount >= this.maxFreeMessages) {
      this.error = 'Free limit reached. Please upgrade to premium.';
      return;
    }

    this.messages.push({ sender: 'user', text: this.question });

    this.http.post<any>('http://127.0.0.1:5000/chat', {
      question: this.question
    }).subscribe({
      next: (res) => {
        this.messages.push({ sender: 'bot', text: res.answer });
        this.question = '';
        this.error = '';
        this.messageCount++;
      },
      error: (err) => {
        this.error = err.error?.message || 'Something went wrong';
      }
    });
  }

  // 🔽 Stripe: Redirect to checkout
  upgradeToPremium() {
    const user = 'guest';

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

  // 🔽 File selected handler
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  // 🔽 Upload CSV to Flask
  uploadCSV() {
    if (!this.selectedFile) {
      console.warn("⚠️ No file selected.");
      return;
    }
  
    const formData = new FormData();
    formData.append('file', this.selectedFile);
  
    console.log("📤 Uploading file:", this.selectedFile.name);
  
    this.http.post<any>('http://127.0.0.1:5000/upload-csv', formData).subscribe({
      next: (res) => {
        console.log("✅ Upload successful:", res);
        this.uploadMessage = res.message || 'CSV uploaded successfully!';
        this.error = '';
      },
      error: (err) => {
        console.error("❌ Upload failed:", err);
        this.uploadMessage = '';
        this.error = 'CSV upload failed: ' + (err.error?.error || 'Unknown error');
      }
    });
  }
  
  

  // 🔍 Check with backend if user is premium
  checkPremiumStatus() {
    const user = 'guest';
  
    this.http.get<any>(`http://127.0.0.1:5000/premium-status?user=${user}`).subscribe({
      next: (res) => {
        this.isPremium = res.premium;
        console.log("🔐 Premium status:", this.isPremium); // ✅ Add this log
        if (this.isPremium) {
          this.messageCount = 0;  // reset limit
          this.error = '';
        }
      },
      error: () => {
        this.isPremium = false;
        console.error("❌ Failed to fetch premium status.");
      }
    });
  }
  
}

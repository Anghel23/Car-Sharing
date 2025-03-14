import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  imports: [RouterLink, FormsModule, CommonModule]
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    const body = new URLSearchParams();
    body.set('username', this.email);
    body.set('password', this.password);

    const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' });

    this.http.post('http://127.0.0.1:8000/users/token', body.toString(), { headers, observe: 'response' })
      .subscribe({
        next: (response) => {
          console.log('📩 Date trimise:', { email: this.email, password: this.password });  
          console.log('🔹 Răspuns primit:', response);
          if (response.status === 200 && response.body) {
            console.log('✅ Autentificare reușită!', response.body);
            const token = (response.body as any).access_token;
            localStorage.setItem('token', token); // ✅ Salvează token-ul
            this.router.navigate(['/rent-map']); // ✅ Redirecționează utilizatorul către prima pagină
          } else {
            console.warn('⚠️ Autentificare eșuată, răspuns neașteptat:', response);
          }
        },
        error: (error) => {
          console.log('📩 Date trimise:', { email: this.email, password: this.password });
          console.error('❌ Eroare la autentificare:', error);
          if (error.status === 401) {
            console.warn('⛔ Autentificare eșuată! Credențiale invalide.', error.error);
            alert('Autentificare eșuată! Verifică email-ul și parola.');
          } else {
            console.warn('⚠️ Altă eroare:', error.status, error.message, error.error);
            alert('A apărut o eroare. Încearcă din nou.');
          }
        }
      });
  }
}

import { Component } from '@angular/core';
import { AuthService } from '../../../services/auth/auth.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  standalone: true,
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  imports: [HttpClientModule, FormsModule, CommonModule]
})
export class RegisterComponent {
  full_name: string = '';
  email: string = '';
  password: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  register() {
    console.log('📩 Date trimise:', { full_name: this.full_name, email: this.email, password: this.password });

    this.authService.register(this.full_name, this.email, this.password).subscribe({
      next: (response) => {
        console.log('✅ Înregistrare reușită!', response);
        alert('Cont creat cu succes!');

        // Autentificare imediată după înregistrare
        this.authService.login(this.email, this.password).subscribe({
          next: (loginResponse) => {
            console.log('✅ Autentificare reușită!', loginResponse);
            alert('Autentificare reușită!');
            this.router.navigate(['/add-payment']);
          },
          error: (loginError) => {
            console.error('❌ Eroare la autentificare:', loginError);
            alert('Eroare la autentificare: ' + (loginError.error.detail || 'Verifică datele introduse.'));
          }
        });
      },
      error: (error) => {
        console.error('❌ Eroare la înregistrare:', error);
        alert('Eroare la înregistrare: ' + (error.error.detail || 'Verifică datele introduse.'));
      }
    });
  }
}
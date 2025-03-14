import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-payment',
  standalone: true,
  templateUrl: './add-payment.component.html',
  styleUrls: ['./add-payment.component.css'],
  imports: [CommonModule, ReactiveFormsModule]
})
export class AddPaymentComponent {
  paymentForm: FormGroup;

  constructor(private fb: FormBuilder, private router: Router) {
    this.paymentForm = this.fb.group({
      cardHolder: ['', [Validators.required, Validators.pattern(/^[a-zA-Z\s]+$/)]],
      cardNumber: ['', [Validators.required, Validators.pattern(/^\d{4} \d{4} \d{4} \d{4}$/)]],
      expiryDate: ['', [Validators.required, Validators.pattern(/^(0[1-9]|1[0-2])\/\d{2}$/)]],
      cvv: ['', [Validators.required, Validators.pattern(/^\d{3}$/)]],
    });
  }

  formatCardNumber(event: any) {
    let input = event.target.value.replace(/\D/g, '').substring(0, 16);
    input = input.match(/.{1,4}/g)?.join(' ') || '';
    this.paymentForm.controls['cardNumber'].setValue(input);
  }

  formatExpiryDate(event: any) {
    let input = event.target.value.replace(/\D/g, '').substring(0, 4);
    if (input.length > 2) {
      input = input.substring(0, 2) + '/' + input.substring(2);
    }
    this.paymentForm.controls['expiryDate'].setValue(input);
  }

  onSubmit() {
    if (this.paymentForm.valid) {
      console.log('✅ Metodă de plată adăugată cu succes!');
      alert('Metodă de plată adăugată cu succes!');
      this.router.navigate(['/add-documents']); // Redirect către pagina de adăugare a documentelor
    } else {
      console.error('❌ Eroare la adăugarea metodei de plată.');
      alert('Eroare la adăugarea metodei de plată. Verifică datele introduse.');
    }
  }
}
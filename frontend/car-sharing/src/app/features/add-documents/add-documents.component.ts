import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-documents',
  standalone: true,
  templateUrl: './add-documents.component.html',
  styleUrls: ['./add-documents.component.css'],
  imports: [CommonModule]
})
export class AddDocumentsComponent {
  selectedImage: string | null = null;

  constructor(private router: Router) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.selectedImage = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  onSubmit() {
    if (this.selectedImage) {
      console.log('✅ Document adăugat cu succes!');
      alert('Document adăugat cu succes!');
      this.router.navigate(['/rent-map']);
    } else {
      console.error('❌ Eroare la adăugarea documentului.');
      alert('Eroare la adăugarea documentului. Te rugăm să selectezi un document.');
    }
  }
}
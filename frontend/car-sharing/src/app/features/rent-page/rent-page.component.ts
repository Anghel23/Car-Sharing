import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-rent-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './rent-page.component.html',
  styleUrls: ['./rent-page.component.css']
})
export class RentPageComponent implements OnInit {
  model: string = '';
  plate: string = '';
  remainingTime: number = 0;
  interval: any;
  rentalId: string = '';
  showDialog: boolean = false;
  dialogMessage: string = '';

  constructor(private route: ActivatedRoute, private router: Router, private http: HttpClient) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.model = params['model'];
      this.plate = params['plate'];
      this.setDuration(params['duration']);
      this.rentalId = params['rental_id'];
    });

    this.startTimer();
  }

  setDuration(duration: string) {
    const times: Record<string, number> = { 
      '30 min': 1800, 
      '1 oră': 3600, 
      '2 ore': 7200, 
      '4 ore': 14400 
    };

    this.remainingTime = times[duration] || 1800;
  }

  startTimer() {
    this.interval = setInterval(() => {
      if (this.remainingTime > 0) {
        this.remainingTime--;
      } else {
        clearInterval(this.interval);
        this.router.navigate(['/rent-map']);
      }
    }, 1000);
  }

  checkCanStopRental() {
    this.http.get(`http://127.0.0.1:8000/rent/can-stop/${this.rentalId}`).subscribe({
      next: (response: any) => {
        if (response.can_stop) {
          this.stopRental();
        } else {
          this.dialogMessage = 'Mașina nu poate fi oprită din următoarele motive:';
          if (response.reasons) {
            this.dialogMessage += '\n' + response.reasons.join('\n');
          }
          this.showDialog = true;
        }
      },
      error: (error) => {
        console.error('Failed to check if rental can be stopped:', error);
        this.dialogMessage = 'A apărut o eroare la verificarea stării mașinii.';
        this.showDialog = true;
      }
    });
  }

  stopRental() {
    clearInterval(this.interval);
    this.http.delete(`http://127.0.0.1:8000/rent/${this.rentalId}`).subscribe({
      next: () => {
        console.log('Rental deleted successfully.');
        this.router.navigate(['/rent-map']);
      },
      error: (error) => {
        console.error('Failed to delete rental:', error);
        this.router.navigate(['/rent-map']);
      }
    });
  }

  closeDialog() {
    this.showDialog = false;
  }

  formatTime(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${this.pad(minutes)}:${this.pad(remainingSeconds)}`;
  }

  pad(value: number): string {
    return value < 10 ? `0${value}` : `${value}`;
  }
}
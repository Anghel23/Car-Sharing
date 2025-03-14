import { Component, AfterViewInit, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-rent-map',
  standalone: true, 
  imports: [CommonModule, FormsModule],
  templateUrl: './rent-map.component.html',
  styleUrls: ['./rent-map.component.css']
})
export class RentMapComponent implements AfterViewInit {
  private map!: any;
  selectedCar: any = null;
  isRenting = false;
  selectedDuration = '30 min';
  selectedPrice = 80;

  rentalOptions = [
    { time: '30 min', price: 80 },
    { time: '1 oră', price: 140 },
    { time: '2 ore', price: 220 },
    { time: '4 ore', price: 300 }
  ];

  constructor(
    @Inject(PLATFORM_ID) private platformId: object, 
    private http: HttpClient, 
    private router: Router,
    private authService: AuthService
  ) {}

  async ngAfterViewInit() {
    if (isPlatformBrowser(this.platformId)) {
      const L = await import('leaflet');
      this.initMap(L);
      this.loadCars(L);
    }
  }

  private initMap(L: any): void {
    this.map = L.map('map', {
      center: [47.1585, 27.6014],
      zoom: 13,
      zoomControl: true, 
      dragging: true,
      scrollWheelZoom: true,
      touchZoom: true,
      doubleClickZoom: true,
      boxZoom: true,
      keyboard: true
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 10,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map);

    setTimeout(() => {
      this.map.invalidateSize();
    }, 500);
  }

  private loadCars(L: any): void {
    this.http.get<any[]>('http://127.0.0.1:8000/cars/available').subscribe(cars => {
      const carIcon = L.icon({
        iconUrl: 'icons/car-location-icon.png',
        iconSize: [45, 45],
        iconAnchor: [19, 38],
        popupAnchor: [0, -30] 
      });

      cars.forEach(car => {
        const marker = L.marker([car.latitude, car.longitude], { icon: carIcon }).addTo(this.map)
          .bindPopup(`<b>${car.model}</b><br>Număr: ${car.license_plate}<br>Combustibil: ${car.fuel_level}%`);

        marker.on('click', () => {
          this.selectedCar = car;
          this.isRenting = false;
        });
      });
    });
  }

  rentCar(): void {
    if (this.selectedCar) {
      this.isRenting = true;
      this.map.eachLayer((layer: any) => {
        if (layer.getLatLng && layer.getLatLng().lat === this.selectedCar.latitude && layer.getLatLng().lng === this.selectedCar.longitude) {
          layer.closePopup();
        }
      });
    }
  }

  updatePrice(): void {
    const selectedOption = this.rentalOptions.find(option => option.time === this.selectedDuration);
    if (selectedOption) {
      this.selectedPrice = selectedOption.price;
    }
  }

  confirmRental(): void {
    const userId = this.authService.getUserId();
    if (!userId) {
      alert('Trebuie să fii autentificat pentru a închiria o mașină.');
      return;
    }

    const rentalData = {
      car_id: this.selectedCar.id,
      user_id: userId,
      duration_minutes: this.getDurationInMinutes(this.selectedDuration)
    };

    this.http.post('http://127.0.0.1:8000/rent', rentalData).subscribe({
      next: (response: any) => {
        console.log('Rental confirmed:', response);
        alert('Închirierea a fost confirmată!');
        this.router.navigate(['/renting'], { 
          queryParams: { 
            model: this.selectedCar.model, 
            plate: this.selectedCar.license_plate, 
            duration: this.selectedDuration,
            rental_id: response.id
          } 
        });
      },
      error: (error) => {
        console.error('Failed to confirm rental:', error);
        alert('A apărut o eroare la confirmarea închirierii.');
      }
    });
  }

  closeRentMenu(): void {
    this.isRenting = false;
    this.selectedCar = null;
  }

  private getDurationInMinutes(duration: string): number {
    const times: Record<string, number> = { 
      '30 min': 30, 
      '1 oră': 60, 
      '2 ore': 120, 
      '4 ore': 240 
    };
    return times[duration] || 30;
  }
}
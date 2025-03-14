import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { LoginComponent } from './features/auth/login/login.component';
import { RegisterComponent } from './features/auth/register/register.component';
import { RentMapComponent } from './features/rent-map/rent-map.component';
import { RentPageComponent } from './features/rent-page/rent-page.component';
import { AddPaymentComponent } from './features/add-payment/add-payment.component';
import { AddDocumentsComponent } from './features/add-documents/add-documents.component';
import { AuthGuard } from './services/guard/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent},
  { path: 'register', component: RegisterComponent},
  { path: 'rent-map', component: RentMapComponent, canActivate: [AuthGuard], data: {ssr: false} },
  { path: 'renting', component: RentPageComponent, canActivate: [AuthGuard] },
  { path: 'add-payment', component: AddPaymentComponent, canActivate: [AuthGuard] },
  { path: 'add-documents', component: AddDocumentsComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: '' },
];
import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8000/users/';
  private loginUrl = 'http://127.0.0.1:8000/users/token';
  private platformId = inject(PLATFORM_ID);

  constructor(private http: HttpClient) {}

  register(full_name: string, email: string, password: string): Observable<any> {
    return this.http.post(this.apiUrl, { full_name, email, password }, { 
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }) 
    });
  }

  login(email: string, password: string): Observable<any> {
    const body = new URLSearchParams();
    body.set('username', email);
    body.set('password', password);

    const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' });

    return this.http.post<{ access_token: string }>(this.loginUrl, body.toString(), { headers })
      .pipe(
        tap(response => {
          if (isPlatformBrowser(this.platformId) && response.access_token) {
            console.log("AuthService: Saving token to localStorage.");
            localStorage.setItem('token', response.access_token);
          }
        })
      );
  }

  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      console.log("AuthService: Removing token.");
      localStorage.removeItem('token');
    }
  }

  isLoggedIn(): boolean {
    if (!isPlatformBrowser(this.platformId)) {
      return false;
    }

    const token = localStorage.getItem('token');

    if (!token) {
      return false;
    }

    try {
      const decoded: any = jwtDecode(token);
      const isExpired = decoded.exp * 1000 < Date.now();

      if (isExpired) {
        this.logout();
        return false;
      }

      return true;

    } catch (error) {
      this.logout();
      return false;
    }
  }

  getToken(): string | null {
    if (!isPlatformBrowser(this.platformId)) {
      return null;
    }
    return localStorage.getItem('token');
  }

  getUserId(): string | null {
    const token = this.getToken();
    if (token) {
      const decoded: any = jwtDecode(token);
      return decoded.id;
    }
    return null;
  }
}
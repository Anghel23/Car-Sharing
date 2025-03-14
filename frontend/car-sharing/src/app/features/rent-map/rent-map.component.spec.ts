import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RentMapComponent } from './rent-map.component';

describe('RentMapComponent', () => {
  let component: RentMapComponent;
  let fixture: ComponentFixture<RentMapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RentMapComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RentMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

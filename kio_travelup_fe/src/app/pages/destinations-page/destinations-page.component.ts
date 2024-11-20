import { Component } from '@angular/core';
import {DestinationModel} from "../../models/DestinationModel";
import {Router} from "@angular/router";

@Component({
  selector: 'app-destinations-page',
  templateUrl: './destinations-page.component.html',
  styleUrls: ['./destinations-page.component.scss']
})
export class DestinationsPageComponent {

  menuItems = ["ACASA", "CONTACT", "DESTINATII"];

  destinations: DestinationModel[] = [
    new DestinationModel('Maldives Beach', 'Maldives', 'Beautiful beachside resort', 500, 10, 20),
    new DestinationModel('Eiffel Tower View', 'Paris', 'See the Eiffel Tower from your window!', 350, 5, 15),
    new DestinationModel('Safari Adventure', 'Kenya', 'Experience the wild in luxury tents', 450, 8, 10)
  ];

  constructor(private router: Router) {
  }


  toggleDropdown(): void {
    const dropdown = document.getElementById("myDropdown");
    if (dropdown) {
      dropdown.classList.toggle("show");
    }
  }

  redirect(item: string) {
    switch (item) {
      case("DESTINATII"):
        this.router.navigate(['destinations']);
        localStorage.setItem('offers', 'false');
        break;

      case("ACASA"):
        this.router.navigate(['']);
        break;

      case("CONTACT"):
        this.router.navigate(['contact']);
        break;
    }
  }
}

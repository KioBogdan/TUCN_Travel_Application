import {Component} from '@angular/core';
import {Router} from "@angular/router";
import {FormBuilder} from "@angular/forms";

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent {
  menuItems = ["ACASA", "CONTACT", "DESTINATII"]

  constructor(private router: Router,
              private fb: FormBuilder) {
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

  goToOffers() {
    const dropdown = document.getElementById("offersDropdown");
    if (dropdown) {
      dropdown.classList.toggle("show-offers");
    }
  }

  goToSpecificOffers() {
    this.router.navigate(['destinations']);
    localStorage.setItem('offers', 'true');
  }


  handleSearchInputEvent() {
    this.router.navigate(['destinations'])
  }
}

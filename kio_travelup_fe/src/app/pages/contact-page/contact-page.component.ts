import {Component} from '@angular/core';
import {FormBuilder, FormGroup} from "@angular/forms";
import {Router} from "@angular/router";

@Component({
  selector: 'app-contact-page',
  templateUrl: './contact-page.component.html',
  styleUrls: ['./contact-page.component.scss']
})
export class ContactPageComponent {
  form!: FormGroup;
  menuItems = ["ACASA", "CONTACT", "DESTINATII"]

  constructor(private fb: FormBuilder,
              private router: Router) {
  }

  ngOnInit() {
    this.initForm();
  }

  initForm(): void {
    this.form = this.fb.group({
      message: ''
    });
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

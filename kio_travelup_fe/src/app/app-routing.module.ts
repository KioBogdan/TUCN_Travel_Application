import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MainPageComponent} from "./pages/main-page/main-page.component";
import {DestinationsPageComponent} from "./pages/destinations-page/destinations-page.component";
import {ContactPageComponent} from "./pages/contact-page/contact-page.component";

const routes: Routes = [
  {path: '', component: MainPageComponent},
  {path: 'destinations', component: DestinationsPageComponent},
  {path: 'contact', component: ContactPageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}

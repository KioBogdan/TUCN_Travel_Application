import {Component, Input, OnInit} from '@angular/core';
import {DestinationModel} from "../models/DestinationModel";

@Component({
  selector: 'app-destination-card',
  templateUrl: './destination-card.component.html',
  styleUrls: ['./destination-card.component.scss']
})
export class DestinationCardComponent implements OnInit {
  @Input() destination!: DestinationModel;
  imagine = '';

  ngOnInit(): void {
    this.imagine = "assets/" + this.destination!.location + ".jpg";
    console.log(this.imagine)
  }
}

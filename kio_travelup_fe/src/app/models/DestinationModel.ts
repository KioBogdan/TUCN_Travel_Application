export class DestinationModel {
  id!: number;
  name!: string;
  location!: string;
  description!: string;
  pricePerNight!: number;
  discount!: number;
  availableSeats!: number;

  constructor(
    name: string,
    location: string,
    description: string,
    pricePerNight: number,
    discount: number,
    availableSeats: number,
  ) {
    this.name = name;
    this.location = location;
    this.pricePerNight = pricePerNight;
    this.description = description;
    this.availableSeats = availableSeats;
    this.discount = discount;
  }
}


from sqlalchemy.orm import Session

from . import models, schemas

from datetime import datetime

#Tutorial
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email = user.email, hashed_password = fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user 

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id = user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#Mine
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email = user.email, hashed_password = fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user 

def create_destination(db: Session, destination: schemas.Destination):
    db_destination = models.Destination(title = destination.title, 
                                        description = destination.description, 
                                        location = destination.location, 
                                        price = destination.price,
                                        no_places = destination.no_places,
                                        percentage = destination.percentage)
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination 

def get_destinations(db: Session, skip: int = 0, limit: int = 1000): #get all stored destinations from db
    return db.query(models.Destination).offset(skip).limit(limit).all()

def get_destinations_only_id(db: Session): #get all stored destinations from db
    destination_ids = db.query(models.Destination.id).all()
    return [id_[0] for id_ in destination_ids]

def get_destinations_by_ids(db: Session, destination_ids: list[int]):
    destinations = db.query(models.Destination).filter(models.Destination.id.in_(destination_ids)).all()
    return destinations

def get_discounted_destinations(db: Session): #get all discounted destinations
    return db.query(models.Destination).filter(models.Destination.percentage > 0).all()

def get_destination_by_location(db: Session, location: str):
    return db.query(models.Destination).filter(models.Destination.location == location).first()

def get_all_reservations(db: Session):
    return db.query(models.Reservation).all()

def get_overlapping_reservations(db: Session, start_date_str: str, end_date_str: str):

    start_date = datetime.fromisoformat(start_date_str) #converts from str to Date
    end_date = datetime.fromisoformat(end_date_str)

    # Query reservations where the end date is after the specified start date
    # and the start date is before the specified end date
    overlapping_reservations = db.query(models.Reservation).filter(
        models.Reservation.end_date > start_date,
        models.Reservation.begin_date < end_date
    ).all()

    return overlapping_reservations



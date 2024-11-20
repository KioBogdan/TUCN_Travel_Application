from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, Float, Date
from sqlalchemy.orm import Relationship

from .database import Base

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     email= Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = Relationship("Item",back_populates="owner")

# class Item(Base):
#     __tablename__ = 'items'

#     id=Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description=Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = Relationship("User", back_populates="items")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Destination(Base):
    __tablename__ = 'destinations'

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, index=True)
    description=Column(String, index=True)
    location=Column(String, index=True)
    price=Column(Float)
    no_places=Column(Integer)
    percentage=Column(Float, index=True) #discount applied to the specified destination

    reservations = Relationship("Reservation", back_populates="destination")

class Reservation(Base):
    __tablename__ = 'reservations'

    id=Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey('destinations.id'))
    reservation_date=Column(String, index=True)
    begin_date=Column(String, index=True)
    end_date=Column(String, index=True)
    total_cost=Column(Integer, index=True)

    destination = Relationship("Destination", back_populates="reservations")



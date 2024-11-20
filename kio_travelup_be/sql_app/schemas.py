from pydantic import BaseModel
from datetime import date
# class UserBase(BaseModel):
#     email: str

# class UserCreate(UserBase):
#     password: str 

# class User(UserBase):
#     id: int 
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         from_attributes = True

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int 

    class Config:
        from_attributes=True

class DestinationBase(BaseModel):
    title: str
    description: str | None = None
    location: str | None = None
    price: float | None = None
    no_places: int | None = None 
    percentage: int | None = None

class DestinationCreate(DestinationBase):
    pass 

class Destination(DestinationBase):
    id: int 
    # title: str
    # description: str 
    # location: str 
    # price: float
    # no_places: int | None = None 
    # percentage: int | None = None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class LoginUserModel(BaseModel):
    email: str
    password: str 

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    hashed_password: str 

class User(UserBase):
    id: int 

    class Config:
        from_attributes = True

class ReservationModelFE(BaseModel):
    destinationId: int
    startDate: str
    endDate: str
    currentDate: str
    totalPrice: float

class DateModel(BaseModel):
    start_date: str
    end_date: str

# class ReservationModel(ReservationModelFE):
#     id: int
#     idDest: int

#     class Config: 
#         from_attributes=True
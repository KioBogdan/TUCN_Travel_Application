from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from .ouath2 import OAuth2PasswordRequestFormEmail

#All other imports 
from pydantic import BaseModel 
from enum import Enum
from typing import Optional
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import timedelta, datetime
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#JWT configuration
SECRET_KEY="4fea795daad4e5122d0616d805b3c4671dfb87d5d9cead0c9baecfd48834c653" #randomly generated JWT secret
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 150

#Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

#Token variables
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme2 = OAuth2PasswordBearer(tokenUrl="login")

#CORS Configuration
# Allow all origins for simplicity. Adjust as needed.
origins = ["http://localhost:4200"]  # Update with your Angular app's URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/users_db/", response_model=schemas.User, status_code=201)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user: 
#         raise HTTPException(
#             status_code=400,
#             detail="Email already registered"
#         )
#     return crud.create_user(db, user)

@app.get("/users_db/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users

@app.get("/users_db/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None: 
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return db_user

# @app.post("/users_db/{user_id}/items/", response_model=schemas.Item, status_code=201)
# def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     return crud.create_user_item(db, item, user_id)

# @app.get("/items_db/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip, limit)
#     return items

#Mine
def verify_password(plain_password, hashed_password): 
    pwd_context.verify(plain_password, hashed_password)
    return True

def get_password_hash(password):
    return pwd_context.hash(password)

# def get_user(db, email: str):
#     if email in db:
#         user_dict = db[email]
#         return UserDb(**user_dict)
    
def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if not user:
        print("User not found")
        return False
    if not verify_password(password, user.hashed_password):
        print("Password verification failed")
        return False
    print("User authenticated")
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None,  additional_claims: dict = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    if additional_claims:
        to_encode.update(additional_claims)

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.LoginUserModel, db: Session = Depends(get_db)): 
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user: 
        raise HTTPException(
            status_code=401,
            detail = "Incorrect email or password",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.email}, 
        expires_delta= access_token_expires,
        additional_claims={"role": "CLIENT"}
    )

    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme2), db: Session = Depends(get_db)):
    credential_exceptions = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: 
            raise credential_exceptions
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credential_exceptions
    
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credential_exceptions
    return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return current_user

# @app.post("/users_db/", response_model=schemas.User, status_code=201)
# def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user: 
#         raise HTTPException(
#             status_code=400,
#             detail="Email already registered"
#         )
#     return crud.create_user(db, user)

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.hashed_password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/destinations_db/create", response_model=schemas.Destination, status_code=201)
def create_destination(destination: schemas.DestinationCreate, db: Session = Depends(get_db)):
    return crud.create_destination(db, destination)

@app.get("/destinations_db/", response_model=list[schemas.Destination])
def get_destinations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    destinations = crud.get_destinations(db, skip, limit)
    return destinations

@app.get("/destinations_db/discount", response_model=list[schemas.Destination])
def get_discounted_destinations(db: Session = Depends(get_db)):
    discounted = crud.get_discounted_destinations(db)
    return discounted

@app.get("/destinations_db/search/", response_model=schemas.Destination)
def get_destination_by_location(db: Session = Depends(get_db), location: str = Query(...)):
    destination = crud.get_destination_by_location(db, location)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination 

@app.post("/reservations/")
def create_reservation(reservation: schemas.ReservationModelFE, db: Session = Depends(get_db)):
    db_reservation = models.Reservation(
        destination_id=reservation.destinationId,
        begin_date=reservation.startDate,
        end_date=reservation.endDate,
        reservation_date=reservation.currentDate,
        total_cost=reservation.totalPrice
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@app.post("/available_destinations/", response_model=list[schemas.Destination])
def get_available_destinations(db: Session = Depends(get_db), dateM: schemas.DateModel = Body(...)):

    overlapping_reservations = crud.get_overlapping_reservations(db, dateM.start_date, dateM.end_date)

    # Extract destination IDs from the overlapping reservations
    overlapping_destination_ids = {reservation.destination_id for reservation in overlapping_reservations}

    # Query all destination IDs
    all_destination_ids = crud.get_destinations_only_id(db)

    # Filter out destination IDs that have overlapping reservations
    available_destination_ids = set(all_destination_ids) - overlapping_destination_ids

    available = list(available_destination_ids)
    
    return crud.get_destinations_by_ids(db, available)

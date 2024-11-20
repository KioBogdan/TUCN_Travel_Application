from enum import Enum
from typing import Optional
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import timedelta, datetime

app = FastAPI()

@app.get('/') #decorator
async def root():
    return {"message": "hello world1"}

@app.post('/')
async def post():
    return {"message": "Return from the post route"}

@app.put('/')
async def put():
    return {"Message": "Return from the put route"}


# @app.get("/items/{item_id}")
# async def get_item(item_id: int): #specify type of returned value; default is All
#     return {"item_id": item_id}

class FoodNum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

#path parameter
@app.get("/foods/{food_name}")
async def get_food(food_name: FoodNum):
    if food_name == FoodNum.vegetables:
        return {"food_name": food_name, "message": "you are healthy"}
    if food_name == FoodNum.fruits:
        return {"food_name": food_name, "message": "you are healthy and sweet"}
    #if food_name.value == "dairy":
    return {"food_name": food_name, "message": "you like dairy"}

items_db = [{"item_name": "foo"}, {"item_name" : "bar"}, {"item_name": "low"}]
#query params
@app.get('/items')
async def list_items(skip: int = 0, limit: int = 10):
    return items_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def get_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        #return {"item_id": item_id, "q": q}
        item.update({"q": q})
    if not short:
        item.update({"description": "Lorem ipsum"})
    #return {"item_id": item_id}
    return item


class Item(BaseModel):
    name: str
    description: str | None = None #works for Python>3.10
    price: float
    tax: float | None = None
    
#request body
@app.post("/items1")
async def create_item(item: Item) -> Item:
    #return item
    item_dict = dict(item)
    if item.tax:
        price_with_tax = item.price + item.tax
        #item_dict.update({"price_with_tax": price_with_tax})
        item_dict['price_with_tax'] = price_with_tax
    return item_dict

#work. Login flow
class User(BaseModel):
    username: str
    password: str

@app.post("/login-json/")
async def login(user: User):
    return user

#for using fetch or axios
@app.post("/login-body/")
async def login_body(username: str = Body(...), password: str = Body(...)):
    return username

#Security
#on what it depends? some Oauth2 schemes that FastAPI provides
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

fake_users_db = {
    "johndoe": dict(
        username="johndoe",
        full_name="John Doe",
        email="John@gmail.com",
        hashed_password="fakehashedsecret",
        disabled=False,
    ),
    "alice": dict(
        username="aliceD",
        full_name="Alice Doe",
        email="Alice@gmail.com",
        hashed_password="fakehashedsecret2",
        disabled=True,
    )
}

def fake_hash_password(password: str):
    return f"fakehashed{password}"

class User2(BaseModel): #inherits BaseModel
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDb(User2):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict= db[username]
        return UserInDb(**user_dict)
    
def fake_decode_token(token):
    return get_user(fake_users_db, token)
    #return User2(
    #    username=f"{token}fakedecoded", email="foo@example.com", full_name="Joe Me"
    #)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

async def get_current_active_user(current_user: User2 = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=400,
            details="Inactive user"
        )
    return current_user

# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     users_dict = fake_users_db.get(form_data.username)
#     if not users_dict:
#         raise HTTPException(
#             status_code=400,
#             detail= "Incorrect username or password"
#         )
#     user=UserInDb(**users_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(
#             status_code=400,
#             detail= "Incorrect username or password"
#         )
#     return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/items3")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

#JWT
SECRET_KEY="4fea795daad4e5122d0616d805b3c4671dfb87d5d9cead0c9baecfd48834c653" #randomly generated JWT secret
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db1 = dict(
    johndoe=dict(
        username="johndoe",
        full_name="John Doe",
        email="John@gmail.com",
        hashed_password="$2b$12$wE2zWurIvPM0Moa8W3WZR.OiWzYvnTEwTz6s2k.rOmxL7w/nxFpGi",
        disabled=False,
    ),
    # "alice": dict(
    #     username="aliceD",
    #     full_name="Alice Doe",
    #     email="Alice@gmail.com",
    #     hashed_password="fakehashedsecret2",
    #     disabled=True,
    # )
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User3(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False 

class UserInDb3(User3):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme2 = OAuth2PasswordBearer(tokenUrl="token")

#checking the plain password with the hashed password, in order to not store a plain password in the db
def verify_password(plain_password, hashed_password): 
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user2(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDb3(**user_dict)
    
def authenticate_user(fake_db, username: str, password: str):
    user = get_user2(fake_db, username)
    if not user: 
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user 

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db1, form_data.username, form_data.password)
    if not user: 
        raise HTTPException(
            status_code=401,
            detail = "Incorrect username or password",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.username}, expires_delta= access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user2(token: str = Depends(oauth2_scheme2)):
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
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exceptions
    
    user = get_user2(fake_users_db1, username=token_data.username)
    if user is None:
        raise credential_exceptions
    return user

async def get_current_active_user2(current_user: User3 = Depends(get_current_user2)):
    if current_user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return current_user

@app.get("/users/me2", response_model=User3)
async def get_me(current_user: User3 = Depends(get_current_active_user2)):
    return current_user

@app.get("/users/me2/items")
async def read_own_items(current_user: User3 = Depends(get_current_active_user2)):
    return [{"item_id": "foo", "owner": current_user.username}]
from pydantic import BaseModel, EmailStr
from typing import Optional
class Token(BaseModel):
    access_token: str
    token_type: str

class NewUser(BaseModel):
    fio: str
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
    password: str
    
class Product(BaseModel):
    name: str
    description: str
    price: float

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
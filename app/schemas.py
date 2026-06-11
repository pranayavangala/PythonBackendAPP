from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

class Config:
        from_attributes = True

class UserLogin(BaseModel):
            email: EmailStr
            password: str

class TokenResponse(BaseModel):
            access_token: str
            token_type: str

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str


class FlowerResponse(BaseModel):
    id: int
    name: str
    price: float
    image: str

    class Config:
        from_attributes = True

class FlowerCreate(BaseModel):
    name: str
    price: float
    image: str


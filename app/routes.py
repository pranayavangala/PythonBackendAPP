from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import SessionLocal
from app.models import User

from app.schemas import UserCreate, UserResponse, UserLogin, TokenResponse ,UserUpdate
from app.auth import verify_password, create_access_token ,get_current_user
from app.models import User, Flower
from fastapi import UploadFile, File ,Form

from typing import Optional
import shutil
import os

from app.schemas import FlowerCreate, FlowerResponse


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=TokenResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


@router.get("/flowers",
            response_model=list[FlowerResponse])
def get_flowers(
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = db.query(Flower)

    if name:
        query = query.filter(
            Flower.name.ilike(f"%{name}%")
        )

    return query.all()

@router.post("/flowers")
def create_flower(
    name: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    upload_dir = "uploads"

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, image.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_flower = Flower(
        name=name,
        price=price,
        image=image.filename
    )

    db.add(new_flower)
    db.commit()
    db.refresh(new_flower)

    return {
        "message": "Flower added successfully",
        "flower": {
            "id": new_flower.id,
            "name": new_flower.name,
            "price": float(new_flower.price),
            "image": new_flower.image
        }
    }

@router.post("/upload")
def upload_image(file: UploadFile = File(...)):

    upload_dir = "uploads"

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Image uploaded successfully",
        "filename": file.filename,
        "url": f"http://localhost:8000/uploads/{file.filename}"
    }

@router.put("/flowers/{flower_id}",
            response_model=FlowerResponse)
def update_flower(
    flower_id: int,
    flower: FlowerCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Flower).filter(
        Flower.id == flower_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Flower not found"
        )

    existing.name = flower.name
    existing.price = flower.price
    existing.image = flower.image

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/flowers/{flower_id}")
def delete_flower(
    flower_id: int,
    db: Session = Depends(get_db)
):

    flower = db.query(Flower).filter(
        Flower.id == flower_id
    ).first()

    if not flower:
        raise HTTPException(
            status_code=404,
            detail="Flower not found"
        )

    db.delete(flower)
    db.commit()

    return {
        "message":"Flower deleted successfully"
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, User
from app.schemas import UserCreate, UserLogin

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Username does not exist")
    
    if db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Username and password do not match")
    
    return {"message": "Login successful"}

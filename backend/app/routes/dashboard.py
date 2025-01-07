from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import RandomNumber
import random
from datetime import datetime

router = APIRouter()

@router.get("/generate-random-numbers/")
def generate_random_numbers(db: Session = Depends(get_db)):
    random_number = random.uniform(1, 100)  # Generate a random number
    timestamp = datetime.utcnow()

    # Save to the database
    new_entry = RandomNumber(timestamp=timestamp, number=random_number)
    db.add(new_entry)
    db.commit()

    return {"timestamp": timestamp, "number": random_number}

@router.get("/get-random-numbers/")
def get_random_numbers(db: Session = Depends(get_db)):
    # Fetch the last 10 random numbers from the database
    random_numbers = db.query(RandomNumber).order_by(RandomNumber.id.desc()).limit(10).all()
    return random_numbers

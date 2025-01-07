from fastapi import APIRouter, HTTPException, File, UploadFile
import pandas as pd
from app.database import SessionLocal
import os

router = APIRouter()

CSV_FILE = "random_numbers.csv"

@router.get("/fetch-csv/")
def fetch_csv():
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, detail="CSV file not found")
    
    return {"message": "Fetched CSV successfully"}

@router.post("/upload-csv/")
def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    df.to_csv(CSV_FILE, index=False)
    return {"message": "CSV uploaded successfully"}

@router.get("/get-previous-version/")
def get_previous_csv():
    # Logic for fetching the previous version
    pass

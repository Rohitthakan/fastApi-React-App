from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.crud import get_csv_data, create_csv_entry, update_csv_entry, delete_csv_entry, create_backup
from app.routes import router as user_router  
from app.routes.dashboard import router as dashboard_router
from app.routes.auth import router as auth_router
from fastapi.responses import JSONResponse
from . import crud, database
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import random
import csv
from typing import List
from pydantic import BaseModel




app = FastAPI()

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fast-api-react-app.vercel.app"],  # Allow all origins; restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    endpoints = {
        "Welcome to the FastAPI Backend": "/",

        "Generate Random Numbers": "/dashboard/random-numbers/",
        "Get Random Numbers": "/dashboard/get-random-numbers/",
        "Fetch CSV": "/csv/fetch-csv/",
        "Upload CSV": "/csv/upload-csv/",
        "Update CSV Entry": "/csv/update-csv/{user_id}",
        "Delete CSV Entry": "/csv/delete-csv/{user_id}",
        "Get Previous CSV Version": "/csv/get-previous-version/",
        "User Registration": "/user/register/",
        "User Login": "/user/login/",
        "Generate Random Numbers (CSV)": "/csv/generate-random-numbers/",
        "Get Random Numbers (CSV)": "/csv/get-random-numbers/"
    }
    
    formatted_endpoints = "\n".join([f"{key}: {value}" for key, value in endpoints.items()])
    
    return formatted_endpoints


@app.get("/dashboard/random-numbers/", response_model=List[dict])
def get_random_numbers(db: Session = Depends(database.get_db)):

    random_numbers = crud.get_random_numbers(db)
    
    return random_numbers



class CsvEntry(BaseModel):
    user: str
    broker: str
    API_key: str
    API_secret: str
    pnl: float
    margin: float
    max_risk: float

@app.get("/csv/fetch-csv/")
async def fetch_csv():
    try:
        data = get_csv_data()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/csv/upload-csv/")
async def upload_csv(entry: CsvEntry):
    try:
        create_csv_entry(entry.dict())
        return {"message": "CSV entry added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/csv/update-csv/{user_id}")
async def update_csv(user_id: str, entry: CsvEntry):
    try:
        update_csv_entry(user_id, entry.dict())
        return {"message": "CSV entry updated successfully!"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/csv/delete-csv/{user_id}")
async def delete_csv(user_id: str):
    try:
        delete_csv_entry(user_id)
        return {"message": "CSV entry deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/csv/get-previous-version/")
async def retrieve_csv():
    try:
        
        backup_file = create_backup()  

        with open(backup_file, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader] 
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

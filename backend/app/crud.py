from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from . import models
from filelock import FileLock
import os
import shutil
import csv
import time
import random
import time
import threading
import queue


CSV_FILE_PATH = 'backend/backend_table.csv'
BACKUP_DIR = 'backend/backups/'

    
random_number_queue = queue.Queue()

# Lock to ensure only one thread generates random numbers at a time
random_number_lock = threading.Lock()

# Function to generate random numbers in the background
def generate_random_numbers():
    i = 1
    while True:
        with random_number_lock:
            # Generate a random number and put it in the queue
            random_number = {"id": i, "number": random.randint(1000, 9999), "timestamp": datetime.now().isoformat()}
            if random_number_queue.qsize() >= 10:
                random_number_queue.get()
            random_number_queue.put(random_number)
            i += 1
        time.sleep(1)  # Wait for 1 second before generating the next number

# Function to get random numbers
def get_random_numbers(db):
    try:
        if random_number_queue.empty():
            print("Starting background thread to generate random numbers...")
            random_number_thread = threading.Thread(target=generate_random_numbers)
            random_number_thread.daemon = True  
            random_number_thread.start()

        random_numbers = []
        while not random_number_queue.empty():
            random_numbers.append(random_number_queue.get())


        return random_numbers

    except Exception as e:
        # Log any exceptions
        print(f"Error fetching random numbers: {e}")
        return []
    



def create_random_number(db: Session, number: float):
    new_number = models.RandomNumber(number=number)
    db.add(new_number)
    db.commit()
    db.refresh(new_number)
    return new_number


def create_backup():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"backend_table_{timestamp}.csv")
    shutil.copy(CSV_FILE_PATH, backup_file)
    return backup_file


def lock_file():
    lock = FileLock(f"{CSV_FILE_PATH}.lock")
    return lock


def read_csv():
    lock = lock_file()
    with lock:
        with open(CSV_FILE_PATH, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]


def write_csv(rows):
    lock = lock_file()
    with lock:
        try:
            
            backup_file = create_backup()

            if not os.path.exists(CSV_FILE_PATH):
                raise FileNotFoundError(f"CSV file not found: {CSV_FILE_PATH}")

            with open(CSV_FILE_PATH, mode='w', newline='') as file:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"CSV file updated successfully! Backup created at {backup_file}")

        except Exception as e:
            print(f"Error writing to CSV file: {e}")
            raise HTTPException(status_code=500, detail="Failed to write CSV data")
        


    
def get_csv_data():
    return read_csv()

# Create Operation
def create_csv_entry(entry: dict):
    rows = read_csv()
    rows.append(entry)
    write_csv(rows)

def update_csv_entry(user_id: str, updated_entry: dict):
    rows = read_csv()
    updated = False
    for row in rows:
        if row['user'].strip().lower() == user_id.strip().lower():  
            row.update(updated_entry)
            updated = True
            break
    if updated:
        write_csv(rows)
    else:
        raise HTTPException(status_code=404, detail="User not found")


def delete_csv_entry(user_id: str):
    rows = read_csv()
    updated_rows = [row for row in rows if row['user'].strip().lower() != user_id.strip().lower()] 
    if len(updated_rows) == len(rows):  
        raise HTTPException(status_code=404, detail="User not found")
    write_csv(updated_rows)


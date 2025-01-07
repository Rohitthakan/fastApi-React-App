from sqlalchemy.orm import Session
from datetime import datetime
from . import models
import random
import time
import threading
import queue

    
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
        # Start the background thread to generate random numbers (only once)
        if random_number_queue.empty():
            print("Starting background thread to generate random numbers...")
            random_number_thread = threading.Thread(target=generate_random_numbers)
            random_number_thread.daemon = True  # Daemon thread will exit when the main program exits
            random_number_thread.start()

        # Fetch random numbers from the queue, only one number per second
        random_numbers = []
        while not random_number_queue.empty():
            random_numbers.append(random_number_queue.get())

        # Print the generated random numbers to debug
        # print(f"Generated random numbers: {random_numbers}")

        return random_numbers

    except Exception as e:
        # Log any exceptions
        print(f"Error fetching random numbers: {e}")
        return []
    


# Function to create a new random number entry in the database
def create_random_number(db: Session, number: float):
    # Create a new RandomNumber object and add it to the session
    new_number = models.RandomNumber(number=number)
    db.add(new_number)
    db.commit()
    db.refresh(new_number)
    return new_number








from filelock import FileLock
import os
import shutil
import csv
import time
from fastapi import HTTPException


CSV_FILE_PATH = 'backend_table.csv'
BACKUP_DIR = 'backups/'

# Function to create a backup of the CSV file
def create_backup():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"backend_table_{timestamp}.csv")
    shutil.copy(CSV_FILE_PATH, backup_file)
    return backup_file

# Lock the CSV file to prevent concurrent access
def lock_file():
    lock = FileLock(f"{CSV_FILE_PATH}.lock")
    return lock

# Function to read the CSV file
def read_csv():
    lock = lock_file()
    with lock:
        with open(CSV_FILE_PATH, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

# Function to write to the CSV file
# def write_csv(rows):
#     lock = lock_file()
#     with lock:
#         # Create a backup before overwriting the file
#         create_backup()

#         # Write data back to the CSV file
#         with open(CSV_FILE_PATH, mode='w', newline='') as file:
#             fieldnames = rows[0].keys()
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(rows)

def write_csv(rows):
    lock = lock_file()
    with lock:
        try:
            # Create a backup before overwriting the file
            backup_file = create_backup()

            # Ensure the CSV file exists before writing
            if not os.path.exists(CSV_FILE_PATH):
                raise FileNotFoundError(f"CSV file not found: {CSV_FILE_PATH}")

            # Write data back to the CSV file
            with open(CSV_FILE_PATH, mode='w', newline='') as file:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"CSV file updated successfully! Backup created at {backup_file}")

        except Exception as e:
            print(f"Error writing to CSV file: {e}")
            raise HTTPException(status_code=500, detail="Failed to write CSV data")
        


        

# CRUD operations for CSV

# Read Operation
def get_csv_data():
    return read_csv()

# Create Operation
def create_csv_entry(entry: dict):
    rows = read_csv()
    rows.append(entry)
    write_csv(rows)

# Update Operation
# def update_csv_entry(user_id: str, updated_entry: dict):
#     rows = read_csv()
#     updated = False
#     for row in rows:
#         if row['user'] == user_id:
#             row.update(updated_entry)
#             updated = True
#             break
#     if updated:
#         write_csv(rows)
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

# # Delete Operation
# def delete_csv_entry(user_id: str):
#     rows = read_csv()
#     rows = [row for row in rows if row['user'] != user_id]
#     write_csv(rows)



# Update Operation: Ensure user exists before updating
def update_csv_entry(user_id: str, updated_entry: dict):
    rows = read_csv()
    updated = False
    for row in rows:
        if row['user'].strip().lower() == user_id.strip().lower():  # Case-insensitive comparison
            row.update(updated_entry)
            updated = True
            break
    if updated:
        write_csv(rows)
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Delete Operation: Ensure user exists before deleting
def delete_csv_entry(user_id: str):
    rows = read_csv()
    updated_rows = [row for row in rows if row['user'].strip().lower() != user_id.strip().lower()]  # Case-insensitive comparison
    if len(updated_rows) == len(rows):  # No user matched
        raise HTTPException(status_code=404, detail="User not found")
    write_csv(updated_rows)


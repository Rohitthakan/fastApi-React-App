# FastAPI & React Full-Stack Project

This project is a full-stack application consisting of a **FastAPI backend** and a **React frontend**. The application allows users to interact with a set of endpoints for data management, including functionalities like CSV handling and random number generation.

### **Frontend Link**
- [Frontend Link](https://fast-api-react-app.vercel.app/)

### **Tech Stack**
- **Frontend**:
  - React
  - JavaScript
  - HTML/CSS
  - Vercel for hosting
- **Backend**:
  - FastAPI
  - Python
  - SQLAlchemy (for database interaction)
  - SQLite (or any preferred database)
  - CORS middleware for cross-origin requests

---

### **Features**
- **User Authentication**:
  - User registration and login
  - Password validation and hashing
- **CSV Handling**:
  - Upload and fetch CSV files
  - Update and delete CSV entries
  - Backup and retrieve previous CSV versions
- **Random Numbers**:
  - Generate random numbers and store them in the database
  - Retrieve the latest random numbers
---

### **Frontend Setup**

1. Clone the frontend repository:
    ```bash
    git clone https://github.com/Rohitthakan/fastApi-React-App.git
    ```

2. Navigate into the project folder:
    ```bash
    cd frontend
    ```

3. Install the required dependencies:
    ```bash
    npm install
    ```

4. Run the frontend locally:
    ```bash
    npm start
    ```

The frontend will be running at `http://localhost:3000/` by default.

---

### **Backend Setup**

1. Clone the backend repository:
    ```bash
    git clone https://github.com/Rohitthakan/fastApi-React-App.git
    ```

2. Navigate into the project folder:
    ```bash
    cd backend
    ```

3. Set up a Python virtual environment (if using `venv`):
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Run the backend locally:
    ```bash
    uvicorn main:app --reload
    ```

The backend will be running at `http://127.0.0.1:8000/` by default.

---

### **Database Setup**
The backend uses **SQLite** (or another database if specified). Ensure that the database file is created after running the backend for the first time.

---

### **Deployment**

- The frontend is hosted on **Vercel** at [Frontend Link](https://fast-api-react-app.vercel.app/).
- The backend is hosted on **Render** at [Backend Link](https://fastapi-react-app.onrender.com/).

---



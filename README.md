# Buguard-Backend-Intern-Assessment

This repository contains the backend assessment for the Buguard internship program.

## Project Setup and Running

### 1. Prerequisites
- Python 3.9+
- PostgreSQL

### 2. Environment Setup
- Clone the repository:
  ```bash
  git clone <repository_url>
  cd Buguard-Backend-Intern-Assessment
  ```
- Create and activate a virtual environment:
  ```bash
  python -m venv venv
  # On Windows
  venv\Scripts\activate
  # On macOS/Linux
  source venv/bin/activate
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Create a `.env` file from the example and update it with your database credentials:
  ```bash
  copy .env.example .env
  ```
  Edit the `.env` file with your database URL and a secret API key.

### 3. Database Setup
- Ensure you have a PostgreSQL database created with the name specified in your `.env` file (e.g., `darkatlas`).

### 4. Running the Application
- Run the FastAPI server:
  ```bash
  uvicorn app.main:app --reload
  ```
- The application will be available at `http://127.0.0.1:8000`.
- API documentation can be found at `http://127.0.0.1:8000/docs`.

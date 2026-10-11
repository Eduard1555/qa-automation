# ShopGuard QA

A demo e-commerce API built with Python and FastAPI, designed for practicing API testing and test automation.

## Features

- REST API for managing products
- SQLite database with sample products
- Product creation and retrieval
- Input validation for product names, prices, and stock
- Automated API tests using pytest

## Tech Stack

- Python
- FastAPI
- SQLite
- pytest
- HTTPX

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd shopguard-qa
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

Open the interactive API documentation at:

http://127.0.0.1:8000/docs

## Running Tests

```bash
python -m pytest -v
```

The test suite covers successful requests, missing products, invalid product IDs, input validation, and product listing.

## Project Status

The API and initial automated test suite are implemented. Additional testing and browser automation will be added as the project evolves.
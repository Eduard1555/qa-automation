
# QA Automation

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
cd qa-automation
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

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

Open the interactive API documentation:

http://127.0.0.1:8000/docs

## Running Tests

```bash
python -m pytest -v
```

## Test Coverage

The current test suite covers:

- Retrieving existing products
- Handling nonexistent products
- Rejecting invalid product IDs
- Creating products successfully
- Rejecting negative prices and stock values
- Validating product names
- Accepting zero stock
- Rejecting zero prices

## Project Status

The API and initial automated test suite are implemented. Browser automation and continuous integration are planned as future improvements.

# QA Automation Demo

[![QA Automation Tests](https://github.com/Eduard1555/qa-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/Eduard1555/qa-automation/actions/workflows/tests.yml)

A full-stack QA automation project demonstrating API testing, browser-based UI testing, test coverage, and continuous integration using Python, FastAPI, pytest, Playwright, React, and GitHub Actions.

## Project Overview

This project provides a product management dashboard backed by a REST API. It is designed to demonstrate practical software testing skills through automated functional tests, negative testing, input validation, database testing, and browser automation.

### Key Features

- REST API built with FastAPI.
- SQLite database with product creation and retrieval.
- Automated API tests using pytest and FastAPI TestClient.
- Browser-based end-to-end tests using Playwright.
- UI validation for product search, creation, and invalid input.
- API and frontend integration through HTTP requests.
- Automated CI testing with GitHub Actions.
- Code coverage reporting with pytest-cov.

## Tech Stack

| Area | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Database | SQLite |
| API Testing | pytest, TestClient, HTTPX |
| Frontend | React, Vite, JavaScript |
| UI Automation | Playwright |
| Coverage | pytest-cov |
| CI/CD | GitHub Actions |
| Version Control | Git, GitHub |

## Automated Tests

### API Testing

The API test suite covers:

- Retrieving the product catalog.
- Retrieving an existing product.
- Handling nonexistent products.
- Rejecting invalid product IDs.
- Creating products successfully.
- Validating product names, prices, and stock quantities.
- Initializing the database and preventing duplicate seed data.
- Verifying database transaction rollback.

### UI Testing

The Playwright suite covers:

- Dashboard rendering and API connection status.
- Loading products from the API.
- Searching and filtering products.
- Creating a product successfully.
- Rejecting missing product names.
- Rejecting zero prices and negative stock.
- Limiting product names to the maximum length of 100 characters.
- Displaying out-of-stock status.

## Test Results

| Test Suite | Results |
|---|---:|
| API tests | 22 passed |
| Playwright UI tests | 9 passed |
| Total automated tests | 31 passed |
| Backend code coverage | 96% |

The reported coverage is for `main.py` and `database.py`, with branch coverage enabled. `main.py` has 100% coverage and `database.py` has 90% coverage.

## Getting Started

### Prerequisites

- Python 3.14
- Node.js 24 and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Eduard1555/qa-automation.git
cd qa-automation
```

### 2. Set up the Python environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the API

From the project root:

```powershell
python -m uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 4. Start the frontend

Open a separate terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open the local URL printed by Vite, normally `http://localhost:5173`.

## Running the Tests

### API tests with coverage

From the project root:

```powershell
python -m pytest --cov=main --cov=database --cov-report=term-missing -v
```

### Playwright UI tests

From the `frontend` directory:

```powershell
npx playwright install chromium
npx playwright test
```

The Playwright configuration starts the frontend and API automatically when they are not already running.

## Continuous Integration

GitHub Actions automatically executes the API and UI test suites on pushes and pull requests.

The API job generates terminal coverage results and a `coverage.xml` artifact. The UI job installs Chromium and executes the Playwright suite.

[View workflow runs](https://github.com/Eduard1555/qa-automation/actions)

## Project Structure

```text
qa-automation/
├── .github/
│   └── workflows/
│       └── tests.yml
├── frontend/
│   ├── src/
│   ├── tests/
│   │   └── products.spec.js
│   ├── package.json
│   └── playwright.config.js
├── tests_api/
│   ├── conftest.py
│   └── test_products.py
├── database.py
├── main.py
├── pytest.ini
├── requirements.txt
└── readme.md
```

## Purpose

This project demonstrates practical skills in:

- Writing maintainable automated tests.
- Testing REST APIs and HTTP responses.
- Validating user input and error handling.
- Testing database initialization and transaction behavior.
- Automating browser interactions with Playwright.
- Measuring code coverage.
- Integrating automated tests into a CI pipeline.

---

**Repository:** [github.com/Eduard1555/qa-automation](https://github.com/Eduard1555/qa-automation)
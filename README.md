# URL Shortener

A small URL shortening service implemented as a test task.

The application provides endpoints to create a shortened URL and redirect to the 
original link.

---

## Tech Stack

- Python 3.12+
- FastAPI
- SQLite3
- Pytest
- Ruff
- uv (dependency management)

---

## Installation

Clone repository and install dependencies:

```
uv sync
```

---

## Running the Application

```
uv run uvicorn app.main:app --reload
```

---

## API docs available at:

```
http://127.0.0.1:8000/docs
```

---

## Running Tests

```
uv run pytest
```

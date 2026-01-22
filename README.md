# Task Dependency Management System

A full-stack Task Dependency Management System where tasks can depend on other tasks, with automatic status updates and circular dependency prevention.

---

## Features

- Create, update, and delete tasks
- Add dependencies between tasks
- Prevent circular dependencies with exact cycle path detection
- Automatic task status updates based on dependencies
- Visual dependency graph using SVG (no graph libraries)
- Clean REST API using Django REST Framework
- React + Tailwind frontend

---

## Tech Stack

### Backend
- Django 4.x
- Django REST Framework
- MySQL (or SQLite for local development)

### Frontend
- React 18
- Vite
- Tailwind CSS
- SVG-based dependency graph

---

## Setup Instructions

### Backend

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Backend runs at:
http://127.0.0.1:8000

Frontend
cd frontend
npm install
npm run dev


Frontend runs at:
http://localhost:5173
```

# API Endpoints

-GET /api/tasks/

-POST /api/tasks/

-PATCH /api/tasks/{id}/

-POST /api/tasks/{id}/dependencies/

# Dependency Rules

Tasks cannot depend on themselves

Circular dependencies are detected and blocked

Exact cycle path is returned in API response

Task status auto-updates when dependencies change

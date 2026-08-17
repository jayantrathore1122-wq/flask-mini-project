# Flask Task Manager

A simple CRUD web app built with Flask, demonstrating backend fundamentals.

## Features
- Flask routing and Jinja2 templates
- Form handling with both GET and POST
- Basic CRUD (Create, Read, Update, Delete) using a JSON file as storage (no database needed)
- Clean, responsive UI using Bootstrap 5

## Requirements
- Python 3.8+
- Flask (`pip install flask`)

## How to run

1. Install Flask:
   ```
   pip install flask
   ```

2. From this folder, run:
   ```
   python3 app.py
   ```

3. Open your browser to:
   ```
   http://127.0.0.1:5000
   ```

## Project structure
```
flask_task_manager/
├── app.py               # Main Flask app with all routes
├── tasks.json            # File-based storage for tasks (auto-created if missing)
├── templates/
│   ├── base.html          # Shared layout with Bootstrap + navbar
│   ├── index.html         # List all tasks
│   ├── add_task.html      # Add task form
│   └── edit_task.html     # Edit task form
└── README.md
```

## Routes
| Route                  | Method    | Purpose                        |
|-------------------------|-----------|---------------------------------|
| `/`                     | GET       | View all tasks                  |
| `/add`                  | GET, POST | Show form / create a new task   |
| `/edit/<task_id>`       | GET, POST | Show form / update a task       |
| `/complete/<task_id>`   | GET       | Toggle a task's done status     |
| `/delete/<task_id>`     | GET       | Delete a task                   |

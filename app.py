"""
Flask Mini Project - Task Manager
Alfido Tech Assignment 4

Goal: Build a simple web app demonstrating backend fundamentals.

Requirements covered:
    - Flask routing and templates
    - Form handling (GET & POST)
    - Basic CRUD using file storage (JSON) - no database needed
    - Clean UI using Bootstrap
"""

import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"  # needed for flash messages

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


# ---------------------------------------------------------------------------
# DATA STORAGE HELPERS (file-based "database")
# ---------------------------------------------------------------------------

def load_tasks():
    """Read all tasks from the JSON file. Returns an empty list if missing."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Write the full task list back to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def get_next_id(tasks):
    """Generate the next task id (simple auto-increment)."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """READ: show all tasks."""
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    """CREATE: show a form (GET) and handle its submission (POST)."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")

        # --- Basic form validation ---
        if not title:
            flash("Title is required.", "danger")
            return render_template("add_task.html", title=title, description=description, priority=priority)

        tasks = load_tasks()
        new_task = {
            "id": get_next_id(tasks),
            "title": title,
            "description": description,
            "priority": priority,
            "done": False,
        }
        tasks.append(new_task)
        save_tasks(tasks)
        flash(f"Task '{title}' added successfully!", "success")
        return redirect(url_for("index"))

    # GET request -> just show the empty form
    return render_template("add_task.html", title="", description="", priority="Medium")


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    """UPDATE: pre-fill a form (GET) and save changes (POST)."""
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        flash("Task not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "danger")
            return render_template("edit_task.html", task=task)

        task["title"] = title
        task["description"] = request.form.get("description", "").strip()
        task["priority"] = request.form.get("priority", "Medium")
        save_tasks(tasks)
        flash(f"Task '{title}' updated!", "success")
        return redirect(url_for("index"))

    return render_template("edit_task.html", task=task)


@app.route("/complete/<int:task_id>")
def toggle_complete(task_id):
    """UPDATE: toggle a task's done status."""
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            break
    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """DELETE: remove a task by id."""
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    flash("Task deleted.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # debug=True gives auto-reload + error pages during development
    app.run(debug=True)

"""
Student Record Management System — Website edition
CodeNova Python Programming Internship — Task 1

Run locally:
    python -m pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import re
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "students.db"

app = Flask(__name__)
app.secret_key = "change-this-local-development-secret-before-deployment"


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY COLLATE NOCASE,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK (age BETWEEN 1 AND 120),
                email TEXT NOT NULL COLLATE NOCASE,
                course TEXT NOT NULL,
                gpa REAL NOT NULL CHECK (gpa BETWEEN 0 AND 4)
            )
        """)


def validate_form(form):
    student_id = form.get("student_id", "").strip()
    name = form.get("name", "").strip()
    age_text = form.get("age", "").strip()
    email = form.get("email", "").strip()
    course = form.get("course", "").strip()
    gpa_text = form.get("gpa", "").strip()

    if not student_id:
        raise ValueError("Student ID is required.")
    if not name:
        raise ValueError("Student name is required.")
    if not age_text.isdigit() or not 1 <= int(age_text) <= 120:
        raise ValueError("Age must be a whole number between 1 and 120.")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Enter a valid email address.")
    if not course:
        raise ValueError("Course is required.")
    try:
        gpa = float(gpa_text)
    except ValueError as exc:
        raise ValueError("GPA must be a number from 0.0 to 4.0.") from exc
    if not 0 <= gpa <= 10:
        raise ValueError("GPA must be between 0.0 and 4.0.")

    return {
        "student_id": student_id,
        "name": name,
        "age": int(age_text),
        "email": email,
        "course": course,
        "gpa": gpa,
    }


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    with connect_db() as db:
        if query:
            pattern = f"%{query}%"
            students = db.execute("""
                SELECT * FROM students
                WHERE student_id LIKE ? COLLATE NOCASE
                   OR name LIKE ? COLLATE NOCASE
                   OR course LIKE ? COLLATE NOCASE
                ORDER BY name COLLATE NOCASE
            """, (pattern, pattern, pattern)).fetchall()
        else:
            students = db.execute(
                "SELECT * FROM students ORDER BY name COLLATE NOCASE"
            ).fetchall()
        stats = db.execute("""
            SELECT COUNT(*) AS total,
                   COALESCE(AVG(gpa), 0) AS avg_gpa,
                   COALESCE(SUM(CASE WHEN gpa >= 3.5 THEN 1 ELSE 0 END), 0) AS high_gpa
            FROM students
        """).fetchone()
    return render_template("index.html", students=students, query=query, stats=stats)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        try:
            student = validate_form(request.form)
            with connect_db() as db:
                db.execute("""
                    INSERT INTO students (student_id, name, age, email, course, gpa)
                    VALUES (:student_id, :name, :age, :email, :course, :gpa)
                """, student)
            flash(f"{student['name']} was added successfully.", "success")
            return redirect(url_for("index"))
        except ValueError as exc:
            flash(str(exc), "error")
        except sqlite3.IntegrityError:
            flash("That student ID already exists. Please use a unique ID.", "error")
        except sqlite3.Error:
            flash("The database operation failed. Please try again.", "error")
    return render_template("form.html", page_title="Add student", student=None, button_label="Save student")


@app.route("/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with connect_db() as db:
        existing = db.execute(
            "SELECT * FROM students WHERE student_id = ? COLLATE NOCASE",
            (student_id,)
        ).fetchone()
    if existing is None:
        flash("Student record not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            student = validate_form(request.form)
            # Keep the original ID stable for the edit operation.
            student["student_id"] = existing["student_id"]
            with connect_db() as db:
                db.execute("""
                    UPDATE students
                    SET name = :name, age = :age, email = :email,
                        course = :course, gpa = :gpa
                    WHERE student_id = :student_id COLLATE NOCASE
                """, student)
            flash(f"{student['name']}'s record was updated.", "success")
            return redirect(url_for("index"))
        except ValueError as exc:
            flash(str(exc), "error")
        except sqlite3.Error:
            flash("The database operation failed. Please try again.", "error")
    return render_template("form.html", page_title="Edit student", student=existing, button_label="Update student")


@app.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    try:
        with connect_db() as db:
            cursor = db.execute(
                "DELETE FROM students WHERE student_id = ? COLLATE NOCASE",
                (student_id,)
            )
        if cursor.rowcount:
            flash("Student record deleted.", "success")
        else:
            flash("Student record was not found.", "error")
    except sqlite3.Error:
        flash("Could not delete the record. Please try again.", "error")
    return redirect(url_for("index"))


@app.errorhandler(500)
def internal_error(_error):
    return render_template("error.html"), 500


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

# StudentHub — Student Record Management Website

**CodeNova Python Programming Internship — Task 1**

A responsive web interface for managing student records, built with Python, Flask, SQLite, HTML, and CSS.

## Features
- Dashboard with total student count, average GPA, and count of students with GPA >= 3.5
- Add, view, search, edit, and delete student records (full CRUD)
- Case-insensitive partial search by student ID, student name, or course
- SQLite persistence across restarts
- Server-side validation for unique student IDs, name, age, email, course, and GPA
- Friendly success/error messages and delete confirmation
- Responsive layout for desktop and mobile
- No paid APIs or external database required

## Requirements
- Python 3.9+
- Internet access is only needed to load the optional Google Fonts; the application itself runs locally without an API.

## Run locally
1. Extract this folder.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended):
   - Windows: `python -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `python -m pip install -r requirements.txt`
5. Start the website: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

The app creates `students.db` automatically on startup.

## Security and deployment notes
- This is a learning/demo project. Before public deployment, set a strong secret key via an environment variable, turn off Flask debug mode, configure HTTPS, and use a production WSGI server.
- Do not expose the Flask development server to the public internet.
- The default configuration is intended for local testing only. `debug=True` should be changed to `debug=False` for deployment.
- Do not enter sensitive real student data in a public demo.

## Suggested screenshots for the internship
1. Dashboard with several sample records
2. Add-student form
3. Search results for a partial name
4. Validation message for a duplicate student ID
5. Edit and delete workflows
6. Mobile-width dashboard (optional)

## GitHub deliverables
Include `app.py`, `requirements.txt`, `templates/`, `static/`, and this README. The SQLite database is generated locally and should usually be excluded from version control if it contains real data. Consider adding a `.gitignore` for `.venv/`, `__pycache__/`, `students.db`, and `.env`.

This project is a local website until deployed. A public live URL requires deploying it to a hosting provider; the app does not automatically publish itself.

from flask import Flask, render_template, request
import sqlite3
import os

import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Base folder: ...\Group_13_DAB_111_2025_Fall
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database path: ...\Group_13_DAB_111_2025_Fall\database\data.db
DB_PATH = os.path.join(BASE_DIR, "database", "data.db")


def get_db_conn():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    dataset_info = {
        "name": "Employees Dataset",
        "source": "employees.xlsx",
        "description": "Each row represents one employee with department, salary, hire date and status."
    }

    variables = [
        {"name": "emp_id", "type": "INTEGER", "description": "Unique employee ID."},
        {"name": "first_name", "type": "TEXT", "description": "Employee first name."},
        {"name": "last_name", "type": "TEXT", "description": "Employee last name."},
        {"name": "department", "type": "TEXT", "description": "Department name."},
        {"name": "salary", "type": "REAL", "description": "Annual salary."},
        {"name": "hire_date", "type": "DATE", "description": "Date the employee was hired."},
        {"name": "email", "type": "TEXT", "description": "Work email address."},
        {"name": "is_active", "type": "INTEGER", "description": "1 = active, 0 = not active."}
    ]

    return render_template("about.html", dataset=dataset_info, variables=variables)


@app.route("/data")
def data_page():
    """Show employees data, with optional filter by department."""
    search_department = request.args.get("department", "").strip()

    conn = get_db_conn()
    cur = conn.cursor()

    base_query = """
        SELECT emp_id, first_name, last_name, department,
               salary, hire_date, email, is_active
        FROM employees
    """

    if search_department:
        cur.execute(base_query + " WHERE department = ? ORDER BY emp_id;", (search_department,))
    else:
        cur.execute(base_query + " ORDER BY emp_id;")

    rows = cur.fetchall()
    conn.close()

    columns = rows[0].keys() if rows else []

    return render_template(
        "data.html",
        rows=rows,
        columns=columns,
        search_department=search_department
    )


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Upload employees.xlsx / CSV and store it as table 'employees'
    in data.db.
    """
    message = ""

    if request.method == "POST":
        if "file" not in request.files:
            message = "No file part in the request."
            return render_template("upload.html", message=message)

        file = request.files["file"]

        if file.filename == "":
            message = "Please choose a file."
            return render_template("upload.html", message=message)

        filename = secure_filename(file.filename)
        temp_path = os.path.join(BASE_DIR, filename)
        file.save(temp_path)

        # Read the file into a DataFrame
        try:
            fname = filename.lower()
            if fname.endswith(".csv"):
                df = pd.read_csv(temp_path)
            elif fname.endswith(".xls") or fname.endswith(".xlsx"):
                df = pd.read_excel(temp_path)
            else:
                message = "Unsupported file type. Use CSV, XLS or XLSX."
                os.remove(temp_path)
                return render_template("upload.html", message=message)
        except Exception as e:
            message = f"Error reading file: {e}"
            os.remove(temp_path)
            return render_template("upload.html", message=message)

        # Save to SQLite as table 'employees'
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("employees", conn, if_exists="replace", index=False)
        conn.close()

        os.remove(temp_path)
        message = "Employees data uploaded into table 'employees'."

    return render_template("upload.html", message=message)


@app.route("/add", methods=["GET", "POST"])
def add_record():
    """Add a new employee row."""
    message = ""

    if request.method == "POST":
        emp_id = request.form.get("emp_id")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        department = request.form.get("department")
        salary = request.form.get("salary")
        hire_date = request.form.get("hire_date")
        email = request.form.get("email")
        is_active = request.form.get("is_active")

        conn = get_db_conn()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO employees
            (emp_id, first_name, last_name, department,
             salary, hire_date, email, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (emp_id, first_name, last_name, department,
             salary, hire_date, email, is_active)
        )

        conn.commit()
        conn.close()

        message = "Employee record added."

    return render_template("add.html", message=message)


@app.route("/delete", methods=["GET", "POST"])
def delete_record():
    """Delete an employee by emp_id."""
    message = ""

    if request.method == "POST":
        emp_id = request.form.get("emp_id")

        conn = get_db_conn()
        cur = conn.cursor()

        cur.execute("DELETE FROM employees WHERE emp_id = ?;", (emp_id,))
        conn.commit()
        deleted_rows = cur.rowcount
        conn.close()

        if deleted_rows > 0:
            message = f"Employee with ID {emp_id} deleted."
        else:
            message = f"No employee found with ID {emp_id}."

    return render_template("delete.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)

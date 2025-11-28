import os
import sqlite3
import pandas as pd

from flask import Flask, render_template, request
from function_app import plot_hist_stats,add_new_records,del_records,upload_data,display_data,display_about


# -------- PATHS --------
main_dir             = os.path.dirname(os.path.abspath(__file__))
templates_page       = os.path.join(main_dir, "website", "templates")
st_css_img_page      = os.path.join(main_dir, "static")
data_folder          = os.path.join(main_dir, "database", "books.db")

app = Flask(__name__, template_folder=templates_page, static_folder=st_css_img_page)

def get_db_connection():
    """
    This function connects to the SQLite database and returns the connection.
    """
    conn = sqlite3.connect(data_folder)
    conn.row_factory = sqlite3.Row
    return conn

def check_database_and_table():
    """
    Checks:
    - If the database file exists
    - If connection works

    Returns:
        (conn, cursor, error_message)
        If error occurs: (None, None, "message")
    """
    if not os.path.exists(data_folder):
        return None, None, "Database not found. Please upload a CSV file first."
    try:
        conn = get_db_connection()
        cur = conn.cursor()
    except Exception as e:
        return None, None, f"Database connection failed: {e}"

    return conn, cur, None

#################################################################################33

@app.route("/")
def home():
    return render_template("home.html")


display_about(app)
upload_data(app, check_database_and_table)
display_data(app, check_database_and_table)
add_new_records(app, check_database_and_table)
del_records(app, check_database_and_table)
plot_hist_stats(app, check_database_and_table)


# Main
if __name__ == "__main__":
    app.run(debug=True)

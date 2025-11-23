from flask import Flask, render_template, request
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64   
from werkzeug.utils import secure_filename

# -------- PATHS --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PATH = os.path.join(BASE_DIR, "website", "templates")
STATIC_PATH = os.path.join(BASE_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "database", "books.db")

app = Flask(__name__, template_folder=TEMPLATE_PATH, static_folder=STATIC_PATH)


# -------- DB CONNECTION --------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)     # FIXED (correct variable)
    conn.row_factory = sqlite3.Row
    return conn


# -------- ROUTES --------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    conn = get_db_connection()
    cur = conn.cursor()

    # Count records from books table
    cur.execute("SELECT COUNT(*) FROM books")
    total_records = cur.fetchone()[0]

    conn.close()

    # You selected 500 records
    selected_records = 500

    dataset = {
        "name": "Book Dataset",
        "description": "A dataset with prices, reviews, ratings, and categories.",
        "source": "Loaded into SQLite Database",
        "total_records": total_records,
        "selected_records": selected_records
    }

    variables = [
        {"name": "BookID", "type": "Integer", "description": "Unique ID for each book"},
        {"name": "Title", "type": "Text", "description": "Book title"},
        {"name": "Category", "type": "Text", "description": "Book category or genre"},
        {"name": "Price", "type": "Float", "description": "Book price"},
        {"name": "Price_After_Tax", "type": "Float", "description": "Final price including tax"},
        {"name": "Tax_amount", "type": "Float", "description": "Applied tax amount"},
        {"name": "Avilability", "type": "Text", "description": "Stock availability"},
        {"name": "Number_of_reviews", "type": "Integer", "description": "Total customer reviews"},
        {"name": "Book_Description", "type": "Text", "description": "Short summary of the book"},
        {"name": "Image_Link", "type": "URL", "description": "Cover image URL"},
        {"name": "Stars", "type": "Integer", "description": "Rating from 0–5 stars"}
    ]

    return render_template("about.html", dataset=dataset, variables=variables)


# ========================
#   DISPLAY BOOKS TABLE
# ========================
@app.route("/data")
def data_page():
    search_query = request.args.get("search", "")

    conn = get_db_connection()
    cur = conn.cursor()

    if search_query:
        cur.execute("""
            SELECT * FROM books
            WHERE Title or Category LIKE ?
        """, ('%' + search_query + '%',))
    else:
        cur.execute("SELECT * FROM books")

    rows = cur.fetchall()
    conn.close()
    '''
        is used to safely get the column names from the first row of data without causing errors.
        If the database query returns rows, rows[0].keys() extracts the column names.
        If the query returns no rows, the expression returns an empty list instead.
        This prevents the program from crashing with an IndexError and ensures your table header logic continues working even when the database is empty or the search finds no results.
    '''
    columns = rows[0].keys() if rows else []

    return render_template("data.html", rows=rows, columns=columns)

# ========================
#       UPLOAD CSV
# ========================
@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    message = ""

    if request.method == "POST":
        if "file" not in request.files:
            return render_template("upload.html", message="No file selected.")

        file = request.files["file"]

        if file.filename == "":
            return render_template("upload.html", message="Please choose a CSV file.")

        filename = secure_filename(file.filename)
        temp_path = os.path.join(BASE_DIR, filename)
        file.save(temp_path)

        # Load CSV into DataFrame
        try:
            
            df = pd.read_csv(temp_path, encoding="latin1", on_bad_lines='skip').head(500)
        except Exception as e:
            os.remove(temp_path)
            return render_template("upload.html", message=f"Error: {e}")

        # Save into SQLite as "books"
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("books", conn, if_exists="replace", index=False)
        conn.close()
        os.remove(temp_path)

        message = "Books dataset uploaded successfully into table 'books'."
        total_records_csv = df.count()


    return render_template("upload.html", message=message)


# ========================
#       ADD NEW BOOK
# ========================
@app.route("/add", methods=["GET", "POST"])
def add_page():
    message = ""

    if request.method == "POST":
        BookID = request.form.get("BookID")
        Title = request.form.get("Title")
        Category = request.form.get("Category")
        Price = request.form.get("Price")
        Price_After_Tax = request.form.get("Price_After_Tax")
        Tax_amount = request.form.get("Tax_amount")
        Avilability = request.form.get("Avilability")     # same spelling as column
        Number_of_reviews = request.form.get("Number_of_reviews")
        Stars = request.form.get("Stars")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO books (
                BookID, Title, Category, Price, Price_After_Tax, Tax_amount,
                Avilability, Number_of_reviews, Stars
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            BookID, Title, Category, Price, Price_After_Tax, Tax_amount,
            Avilability, Number_of_reviews,  Stars
        ))

        conn.commit()
        conn.close()

        message = "Book added successfully."

    return render_template("add.html", message=message)


# ========================
#      DELETE BOOK
# ========================
@app.route("/delete", methods=["GET", "POST"])
def delete_page():
    message = ""

    if request.method == "POST":
        BookID = request.form.get("BookID")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM books WHERE BookID = ?;", (BookID,))
        conn.commit()

        deleted = cur.rowcount
        conn.close()

        if deleted > 0:
            message = f"Book with ID {BookID} deleted."
        else:
            message = f"No book found with ID {BookID}."

    return render_template("delete.html", message=message)

import io, base64
import pandas as pd
import matplotlib.pyplot as plt

@app.route("/hist_stats")
def hist_stats():
    # 1. Read Category from DB
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT Category FROM books", conn)
    conn.close()

    # 2. Count books per category
    cat_counts = df["Category"].value_counts()

    # 3. Count how many categories share the same count
    #    (e.g. 1 book -> 10 categories, 2 books -> 1 category, etc.)
    freq_of_counts = cat_counts.value_counts().sort_index()

    # 4. Make a colored "histogram" (bar plot of frequency of counts)
    plt.clf()
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(freq_of_counts.index.astype(str), freq_of_counts.values, color="orange")

    ax.set_xlabel("Book Count per Category", fontsize=14)
    ax.set_ylabel("Number of Categories", fontsize=14)
    ax.set_title("How Many Categories Have Each Book Count", fontsize=18)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # 5. Convert plot to base64 for HTML
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode("utf-8")

    return render_template("hist_stats.html", plot_url=plot_url)




# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -------- PATHS --------
main_dir = os.path.dirname(os.path.abspath(__file__))

templates_page = os.path.join(main_dir, "website", "templates")
st_css_img_page = os.path.join(main_dir, "static")
data_folder = os.path.join(main_dir, "database", "books.db")


# Make sure static folder exists (for saving plots)
os.makedirs(st_css_img_page, exist_ok=True)

#### clean Data###
data_processing_path = os.path.join(main_dir, "data processing")
os.makedirs(data_processing_path, exist_ok=True)

data_collection_path = os.path.join(main_dir, "data collection")
os.makedirs(data_collection_path, exist_ok=True)

raw_csv_path = os.path.join(data_processing_path, "Book_Dataset_1.csv")
clean_csv_path = os.path.join(data_collection_path, "cl_book_ds.csv")

#####

app = Flask(__name__, template_folder=templates_page, static_folder=st_css_img_page)



# -------- DB CONNECTION --------
def get_db_connection():
    conn = sqlite3.connect(data_folder)
    conn.row_factory = sqlite3.Row
    return conn

def check_database_and_table():
    """
    Checks:
    - If the database file exists
    - If connection works
    - If 'books' table exists

    Returns:
        (conn, cursor, error_message)
        If error occurs: (None, None, "message")
    """

    # 1. Database file must exist
    if not os.path.exists(data_folder):
        return None, None, "Database not found. Please upload a CSV file first."

    try:
        conn = get_db_connection()
        cur = conn.cursor()
    except Exception as e:
        return None, None, f"Database connection failed: {e}"

    # 2. Check table exists
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
        if cur.fetchone() is None:
            conn.close()
            return None, None, "Table 'books' does not exist. Upload a CSV file first."
    except Exception as e:
        conn.close()
        return None, None, f"Error checking table: {e}"

    # Everything OK
    return conn, cur, None

## Clean Function


 #################################################################################33

# -------- ROUTES --------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    dataset = {
        "name": "Book Dataset",
        "description": "A dataset with prices, reviews, ratings, and categories.",
        "source": "Loaded into SQLite Database"

    }

    variables = [
        {"name": "BookID", "type": "Integer", "description": "Unique ID for each book"},
        {"name": "Title", "type": "Text", "description": "Book title"},
        {"name": "Category", "type": "Text", "description": "Book category or genre"},
        {"name": "Price", "type": "Float", "description": "Book price"},
        {"name": "Price_After_Tax", "type": "Float", "description": "Final price including tax"},
        {"name": "Tax_amount", "type": "Float", "description": "Applied tax amount"},
        {"name": "Avilability", "type": "Integer", "description": "Stock availability"},
        {"name": "Number_of_reviews", "type": "Integer", "description": "Total customer reviews"},
        {"name": "Stars", "type": "Integer", "description": "Rating from 0–5 stars"}
    ]

    return render_template("about.html", dataset=dataset, variables=variables)


# ========================
#   DISPLAY BOOKS TABLE
# ========================
@app.route("/data")
def data_page():
    search_query = request.args.get("search", "").strip()

    conn, cur, error = check_database_and_table()
    if error:
        return render_template("data.html", rows=[], columns=[], error=error)

    # Run search or load all data
    try:
        if search_query:
            like_text = f"%{search_query}%"
            cur.execute("""
                SELECT * FROM books
                WHERE Title LIKE ? OR Category LIKE ? OR BookID like  ?
            """, (like_text, like_text,like_text))
        else:
            cur.execute("SELECT * FROM books")

        rows = cur.fetchall()
        columns = rows[0].keys() if rows else []

        conn.close()
        return render_template("data.html", rows=rows, columns=columns)

    except Exception as e:
        conn.close()
        return render_template("data.html", rows=[], columns=[], error=f"Error loading data: {e}")


# ========================
#       UPLOAD CSV
# ========================
@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    message = ""

    if request.method == "POST":
        file = request.files.get("file")

        # No file selected
        if file is None or file.filename == "":
            message = "Please select a CSV file."
            return render_template("upload.html", message=message)

        # Read CSV directly from memory (NO TEMP PATH)
        try:
            df = pd.read_csv(file.stream, encoding="latin1", on_bad_lines='skip').head(500)
        except Exception as e:
            message = f"Error reading CSV file: {e}"
            return render_template("upload.html", message=message)

        #  Save DataFrame to SQLite as "books"
        conn = sqlite3.connect(data_folder)   # connect to your database file
        df.to_sql("books", conn, if_exists="replace", index=False)
        conn.close()

        message = "CSV uploaded and saved into the 'books' table successfully."

    return render_template("upload.html", message=message)


def clean_and_save_books_csv():
    """
    Simple cleaning:
    1. Read Book_Dataset_1.csv from data processing
    2. Drop long text + URL columns
    3. Rename columns
    4. Save cleaned CSV to data collection
    """

    # Read raw CSV
    raw_df = pd.read_csv(raw_csv_path, encoding="latin1", on_bad_lines="skip")

    # Drop columns we do not need
    cols_to_drop = ["Book_Description", "Image_Link"]
    raw_df = raw_df.drop(columns=[c for c in cols_to_drop if c in raw_df.columns])

  
    # Rename columns
    rename_map = {
        "Unnamed: 0": "BookID",
        "Title": "Title",
        "Category": "Category",
        "Price": "Price",
        "Price_After_Tax": "PriceTax",
        "Tax_amount": "Tax",
        "Avilability": "Stock",
        "Number_of_reviews": "Reviews",
        "Stars": "Rating"
    }
    raw_df = raw_df.rename(columns=rename_map)

    # Reorder columns
    final_cols = ["BookID", "Title", "Category", "Price", "PriceTax", "Tax", "Stock", "Reviews", "Rating"]
    raw_df = raw_df[final_cols]

    # Save cleaned CSV
    raw_df.to_csv(clean_csv_path, index=False, encoding="utf-8")

    return "Cleaning completed. Clean CSV saved!"


# ========================
#       ADD NEW BOOK
# ========================
@app.route("/add", methods=["GET", "POST"])
def add_page():
    message = None
    error = None

    # 0. Check database + table
    conn, cur, error = check_database_and_table()
    if error:
        return render_template("add.html", message=None, error=error)

    # 1. If this is a POST, insert a new record
    if request.method == "POST":
        BookID = request.form.get("BookID")
        Title = request.form.get("Title")
        Category = request.form.get("Category")
        Price = request.form.get("Price")
        Price_After_Tax = request.form.get("PriceTax")
        Tax_amount = request.form.get("Tax")
        Avilability = request.form.get("Stock")   # same spelling as DB
        Number_of_reviews = request.form.get("Reviews")
        Stars = request.form.get("Rating")

        # Simple validation
        if not BookID or not Title:
            conn.close()
            error = "Book ID and Title are required."
            return render_template("add.html", message=None, error=error)

        try:
            cur.execute(
                """
                INSERT INTO books (
                    BookID, Title, Category, Price, PriceTax,
                    Tax, Stock, Reviews, Rating
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    BookID, Title, Category, Price, Price_After_Tax,
                    Tax_amount, Avilability, Number_of_reviews, Stars
                )
            )

            conn.commit()
            conn.close()

            message = f"Book '{Title}' added successfully."

            return render_template("add.html", message=message, error=None)

        except Exception as e:
            conn.close()
            error = f"Error inserting record: {e}"
            return render_template("add.html", message=None, error=error)

    # 2. GET request → show empty form
    conn.close()
    return render_template("add.html", message=None, error=None)


# ========================
#      DELETE BOOK
# ========================
@app.route("/delete", methods=["GET", "POST"])
def delete_page():
    message = None
    error = None

    # 0. Check database file + 'books' table (same as hist_stats)
    conn, cur, error = check_database_and_table()
    if error:
        # No need to keep connection if there was an error
        return render_template("delete.html", message=None, error=error)

    # 1. If this is a POST, try to delete a book
    if request.method == "POST":
        BookID = request.form.get("BookID")

        if not BookID:
            conn.close()
            error = "Please enter a Book ID."
            return render_template("delete.html", message=None, error=error)

        cur.execute("DELETE FROM books WHERE BookID = ?;", (BookID,))
        conn.commit()

        deleted = cur.rowcount
        conn.close()

        if deleted > 0:
            message = f"Book with ID {BookID} deleted."
        else:
            message = f"No book found with ID {BookID}."

        return render_template("delete.html", message=message, error=None)

    # 2. GET request → just show the form (no message)
    conn.close()
    return render_template("delete.html", message=None, error=None)



# ========================
#   HISTOGRAM / STATS
# ========================
@app.route("/hist_stats")
def hist_stats():
    conn, cur, error = check_database_and_table()
    if error:
        return render_template("hist_stats.html",
                               plot_filename=None,
                               error=error,
                               message=None)

    try:
        df = pd.read_sql_query("SELECT Category FROM books", conn)
        conn.close()

        if df.empty:
            return render_template("hist_stats.html",
                                   plot_filename=None,
                                   error=None,
                                   message="No data available to plot.")

        cat_counts = df["Category"].value_counts()
        freq_of_counts = cat_counts.value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(freq_of_counts.index.astype(str), freq_of_counts.values, color="orange")
        plt.tight_layout()

        plot_filename = "hist_stats.png"
        output_path = os.path.join(st_css_img_page, plot_filename)
        fig.savefig(output_path)

        return render_template("hist_stats.html",
                               plot_filename=plot_filename,
                               error=None,
                               message=None)

    except Exception as e:
        return render_template("hist_stats.html",
                               plot_filename=None,
                               error=f"Error creating plot: {e}",
                               message=None)


# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)

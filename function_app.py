
# Application Function function_app.py

import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import sqlite3
import os
matplotlib.use("Agg")  # must be before importing pyplot
from flask import render_template, request



def display_about(app):

    ''' This function to display the Data set information in about pages and also display readme.md'''

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



def display_data(app, check_database_avl):

    ''' This function to display the Data from DB and Search by  Title ,  Category and BookID '''

    @app.route("/data")
    
    def data_page():
        search_query = request.args.get("search", "").strip()
        conn, cur, error = check_database_avl()
        if error:
            return render_template("data.html", rows=[], columns=[], error=error)
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

def upload_data(app,data_folder):

    ''' This function upload the Data from CVS file to DB also create DB if not exist '''

    @app.route("/upload", methods=["GET", "POST"])
    def upload_page():
        message = ""

        if request.method == "POST":
            limit = request.form.get("limit", "").strip()
            if limit == "":
                message = "Please enter how many records to upload."
                return render_template("upload.html", message=message)
            if not limit.isdigit():
                message = "Record number must be a positive number."
                return render_template("upload.html", message=message)
            limit = int(limit)
            if limit <= 1:
                message = "Record number must be greater than 1."
                return render_template("upload.html", message=message)
            file = request.files.get("file")
            if file is None or file.filename == "":
                message = "Please select a CSV file."
                return render_template("upload.html", message=message)

            try:
                df = pd.read_csv(file.stream, encoding="latin1", on_bad_lines='skip').head(limit)
            except Exception as e:
                message = f"Error reading CSV: {e}"
                return render_template("upload.html", message=message)

            try:
               conn = sqlite3.connect(data_folder)
               df.to_sql("books", conn, if_exists="replace", index=False)
               conn.close()
               message = f"{len(df)} records uploaded successfully!"
            except Exception as e:
               error = f"Error writing to database: {e}"

        return render_template("upload.html", message=message)

def add_new_records(app, check_database_avl):

    ''' This function Add new record bfore that check if record avilabe  display message the record found Bfore '''

    @app.route("/add", methods=["GET", "POST"])
    def add_page():
        message = None
        error = None

        conn, cur, error = check_database_avl()
        if error:
            return render_template("add.html", message=None, error=error)

        if request.method == "POST":
            try:
                # Read form values
                BookID          = (request.form.get("BookID") or "").strip()
                Title           = (request.form.get("Title") or "").strip()
                Category        = (request.form.get("Category") or "").strip()
                Price           = request.form.get("Price") or None
                Price_After_Tax = request.form.get("PriceTax") or None
                Tax_amount      = request.form.get("Tax") or None
                Stock           = request.form.get("Stock") or None
                Reviews         = request.form.get("Reviews") or None
                Rating          = request.form.get("Rating") or None

                if not BookID or not Title:
                    raise ValueError("Book ID and Title are required.")
                
                cur.execute("SELECT BookID FROM books WHERE BookID = ?", (BookID,))
                existing = cur.fetchone()

                if existing:
                    # Book ID already exists
                    error = f"Book ID '{BookID}' already exists. Please use a different ID."
                    return render_template("add.html", message=None, error=error)

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
                            Tax_amount, Stock, Reviews, Rating
                        )
                    )

                conn.commit()
                message = f"Book '{Title}' added successfully."
                return render_template("add.html", message=message, error=None)
            except Exception as e:
                    conn.rollback()
                    error = f"Error inserting record: {e}"
                    return render_template("add.html", message=None, error=error)

            finally:
                    conn.close()

        conn.close()
        return render_template("add.html", message=None, error=None)


def del_records(app, check_database_avl):
    ''' This function Delete the record from databasee '''

    @app.route("/delete", methods=["GET", "POST"])
    def delete_page():
            message = None
            error = None

            conn, cur, error = check_database_avl()
            if error:
                return render_template("delete.html", message=None, error=error)

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

            conn.close()
            return render_template("delete.html", message=None, error=None)


def plot_hist_stats(app, check_database_and_table):
    
    """    This function plot histogram    """

    @app.route("/hist_stats")
    def hist_stats():
        conn, cur, error = check_database_and_table()
        if error:
            return render_template(
                "hist_stats.html",
                plot_cat_url=None,
                error=error,
                message=None
            )

        try:
            cur.execute("""
                SELECT Category, COUNT(*) 
                FROM books
                GROUP BY Category
                ORDER BY COUNT(*) DESC
            """)
            cat_results = cur.fetchall()
            conn.close()

            if not cat_results:
                return render_template(
                    "hist_stats.html",
                    plot_cat_url=None,
                    error=None,
                    message="No data available to plot."
                )

            categories = [row[0] for row in cat_results]
            counts = [row[1] for row in cat_results]

            # Sort by count descending
            sorted_pairs = sorted(zip(categories, counts), key=lambda x: x[1], reverse=True)
            categories, counts = zip(*sorted_pairs)

            # Create bar chart
            fig, ax = plt.subplots(figsize=(16, 6))
            colors = plt.cm.tab20(range(len(categories)))
            bars = ax.bar(categories, counts, color=colors)

            ax.set_title("Book Count per Category")
            ax.set_xlabel("Category")
            ax.set_ylabel("Number of Books")
            plt.xticks(rotation=45, ha="right")

            # Add values on top of bars
            for bar, value in zip(bars, counts):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    value + 0.5,
                    str(value),
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    fontweight='bold'
                )

            # Convert to Base64
            img = io.BytesIO()
            fig.savefig(img, format="png", bbox_inches="tight")
            img.seek(0)
            plt.close(fig)

            plot_cat_url = base64.b64encode(img.getvalue()).decode("utf-8")

            return render_template(
                "hist_stats.html",
                plot_cat_url=plot_cat_url,
                error=None,
                message=None
            )

        except Exception as e:
            return render_template(
                "hist_stats.html",
                plot_cat_url=None,
                error=f"Error creating plot: {e}",
                message=None
            )

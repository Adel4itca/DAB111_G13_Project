
# Application Function function_app.py

import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import sqlite3
matplotlib.use("Agg")  # must be before importing pyplot
from flask import render_template, request



def display_about(app):

    ''' This function displays the dataset information and all variable descriptions on the About page,
        and also display readme.md'''

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

    ''' This function to display the Data from DB and Search by  Title ,  Category and BookID:
      User opens the page     -	Shows all books or only matching books
      Get search text         -	If user types “python”, it will search for “python” in the database
      Connect to database     - Makes sure the database exists and can be opened
      Decide which SQL to run -	If empty → show everything with SELECT * FROM books
      Run SQL query	          - Gets rows of book data from the table
      Fetch results	          - Reads all matching records
      Get column names	      - Needed to display table headers (Title, Category, Price…)
      Show data on webpage    - Sends data to HTML so user can see it
       Error handling	      - Prevents app crash and helps user know what went wrong
    '''

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

    ''' This function upload the Data from CVS file to DB also create DB if not exist
    User opens /upload page
    User chooses a CSV file
    User enters how many rows to upload
    The file is read using pandas
    Only first N rows are taken
    A new SQLite database (books table) is created automatically
    Data is inserted
    Success message is shown 
    '''

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
                book_ds = pd.read_csv(file.stream, encoding="latin1", on_bad_lines='skip').head(limit)
            except Exception as e:
                message = f"Error reading CSV: {e}"
                return render_template("upload.html", message=message)

            try:
               db_connection = sqlite3.connect(data_folder)
               book_ds.to_sql("books", db_connection, if_exists="replace", index=False)
               db_connection.close()
               message = f"{len(df)} records uploaded successfully!"
            except Exception as e:
               error = f"Error writing to database: {e}"

        return render_template("upload.html", message=message)

def add_new_records(app, check_database_avl):

    ''' This function adds a new book to the database, but first checks if the BookID already exists to prevent duplicate
        User opens the Add page	        -	Shows an empty form where the user can enter book information.
        Connect to the database	        -	Makes sure the database exists and can be opened before adding anything.
        Check if form was submitted	    -	Detects if the user clicked the “Add Book” button.
        Read form values	            -	Collects BookID, Title, Category, Price, Stock, Rating, etc. from the form.
        Validate required fields	    -	Ensures BookID and Title are not empty because they are required.
        Check if BookID already exists	-	Looks in the database; if the ID exists, shows an error message.
        Insert new book	                -	Adds the book into the database using an SQL INSERT statement.
        Save changes	                -	Commits the insert so the new book is stored permanently.
        Show success message	        -	Tells the user the book was added successfully.
        Handle any errors	            -	If something goes wrong, cancels the insert and shows an error message.
        Close the database	            -	Safely closes the connection after finishing the work.
    '''

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
    ''' This function deletes a book by BookID and tells the user whether the record existed or not.
    User opens the delete page	        -	The user visits /delete to delete a book.
    Connect to the database	            -	The function checks if the database is available.
    User submits BookID in the form	    -	User types a BookID they want to delete.
    Validate BookID	                    -	If the BookID is empty, show an error message.
    Delete the record	                -	The system tries to delete the book with that BookID.
    Check if deletion happened	        -	If rowcount > 0, deletion was successful.
    Show success or not-found message	-	Tell the user if the book was deleted or if the ID doesn’t exist.
    Close the database	                -	The database connection is safely closed.
    Reload delete page	                -	Page refreshes to allow deleting another record.
    '''

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
    
    """This function reads category counts from the database, creates a bar chart, converts it to an image, 
    and displays it on the histogram page.
    Connect to the database	-	Opens the database and checks if the books table exists.
    Read category counts	-	Runs a SQL query to count how many books are in each category.
    Prepare the data	    -	Creates two lists: categories and their book counts, sorted from biggest to smallest.
    Create the bar chart	-	Draws a colorful bar chart showing how many books are in each category.
    Convert the chart and send to HTML	-	Saves the chart as Base64 and displays it on the webpage (hist_stats.html).
    """

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

import os
from flask import Flask, render_template, request
from function_app import plot_hist_stats,add_new_records,del_records,upload_data,display_data,display_about
import sqlite3

# -------- PATHS --------
main_dir             = os.path.dirname(os.path.abspath(__file__))
templates_page       = os.path.join(main_dir, "website", "templates")
st_css_img_page      = os.path.join(main_dir, "static")
data_folder          = os.path.join(main_dir, "database", "books.db")


app = Flask(__name__, template_folder=templates_page, static_folder=st_css_img_page)

def get_db_connection():

    """This function opens the SQLite database and returns a connection that allows rows to be accessed like dictionaries.
    """
    main_db_co = sqlite3.connect(data_folder)
    main_db_co.row_factory = sqlite3.Row
    return main_db_co

def check_database_avl():
    """ This function checks if the database exists and returns a connection so other pages can safely read or write data.
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

@app.route("/")                         #Displays the homepage of the Book Project website.
def home():
    return render_template("home.html")



display_about(app)                       #Shows dataset information and variable descriptions on the About page.
upload_data(app,data_folder)             #Uploads a CSV file and saves the first N records into the database.
display_data(app, check_database_avl)    #Displays all books and supports searching by Title, Category, or BookID.
add_new_records(app, check_database_avl) #Adds a new book but checks if the BookID already exists before inserting.
del_records(app, check_database_avl)     #Deletes a book from the database using a BookID entered by the user.
plot_hist_stats(app, check_database_avl) #Creates a bar chart showing how many books are in each category.


# Main -Starts the Flask app in debug mode so you can run the website locally.
if __name__ == "__main__":
    app.run(debug=True)

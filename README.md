#  DAB111 Group 13 

This project is a complete Flask-based web application built for the
**DAB111** course.\
It integrates **data collection, data uploading, database storage, and
data visualization** into one system.\
The application allows users to upload Excel files, store multiple
sheets into SQLite tables, and view or manage the data directly from a
web interface.

##  Features

### 🔹 1. Data Upload System

-   Upload an `Book_Dataset_1.csv` file 
-   Uses `pandas` to read csv files
-   Uses `sqlite3` to write tables into the database

### 🔹 2. SQLite Database Integration

-   Database: `books.db`
-   Automatic table creation (if not exists)

### 🔹 3. Full Flask Web UI (Jinja2 Templates)

-   `home.html` -- Homepage\
-   `about.html` -- Shows statistics, counts, metadata\
-   `data.html` -- Display selected table\
-   `upload.html` -- Upload Excel file\
-   `add.html` -- Add a new record\
-   `delete.html` -- Delete records\
-   `hist_stats.html` -- Statistics & charts\
-   Base template for all pages for easy editing

### 🔹 4. Static Assets

-   CSS styles under `static/css/`
-   Images under `static/images/`


## 🗂️ Project Structure

    DAB111_G13_Project/
    │
    ├── app.py
    ├── requirements.txt
    ├── README.md
    │
    ├── database/
    │   └── books.db
    │
    ├── data_collection/
    │   └── (uploaded Excel files)
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── images/
    │
    └── website/
        ├── templates/
        │   ├── base.html
        │   ├── home.html
        │   ├── about.html
        │   ├── data.html
        │   ├── upload.html
        │   ├── add.html
        │   ├── delete.html
        │   └── hist_stats.html

##  Installation & Setup

### **1. Clone the Repository**

    git clone https://github.com/Adel4itca/DAB111_G13_Project.git
    cd DAB111_G13_Project

### **2. Create a Virtual Environment**

    python -m venv venv

Activate it:

**Windows:**

    venv\Scriptsctivate

### **3. Install Dependencies**

    pip install -r requirements.txt

## ▶️ Run the Application

Start Flask:

    python app.py

Open in browser:

    http://127.0.0.1:5000

##  How to Upload Excel Files

1.  Go to **Upload Page**
2.  Select an `.csv` file containing 3 sheets
3.  Click Upload
4.  Data is stored in **SQLite** automatically

##  Data Pages

-   View tables
-   Search data
-   Add new records
-   Delete records
-   View statistics (record count, selected rows, chart)

##  Technologies Used

-   Python 3
-   Flask
-   SQLite
-   Pandas
-   Matplotlib
-   HTML/CSS (Jinja2 templates)

##  Team Members -- Group 13

-   Adel Hasan 0888146
-   Sumit Singh Gulshan 0888735

## License

This project is for educational use for the DAB111 course at St. Clair
College.

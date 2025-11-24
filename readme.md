````markdown
# DAB111 Group 13 – Flask Data Website Project

This project is developed for the **DAB111 / DBA111** course at St. Clair College.  
It is a Flask-based web application that allows users to upload CSV files, convert them into SQLite database tables, display the data, and interact with it through a simple web interface.

## Dataset Information

### About the Dataset
This dataset was created as a result of practicing scraping using the `requests` and `bs4` libraries in Python. Web scraping or collecting data is one of the most basic and important steps for any data-related field. This was my attempt to do scraping and present it clearly and understandably. The notebook for scraping, along with comments, is in the code section of the original dataset. The data has also been cleaned as required.

**Dataset Source:**  
https://www.kaggle.com/datasets/jalota/books-dataset

### The dataset has attributes/columns as follows:
- Title: The title of the book.
- Category: Category of the book.
- Price: The price of the book.
- Price After Tax: The cost of the book including tax.
- Tax Amount: Tax on the book.
- Availability: The quantity available in stock.
- Number of Reviews: Number of people who reviewed the book.
- Book Description: Description of the book.
- Image Link: Link to the image of the book.
- Stars: Star rating for each book out of 5.

### What can we do with this?
We can perform Exploratory Data Analysis, clustering of books by category, and build a content-based recommendation engine using various fields from the book description.

### File Format
CSV format.

### License
Refer to the dataset's Kaggle page for usage terms.

## Features

###  1. Data Upload System

- Upload a `Book_Dataset_1.csv` file
- Uses `pandas` to read CSV files
- Uses `sqlite3` to write tables into the database

###  2. SQLite Database Integration

- Database: `books.db`
- Automatic table creation (if not exists)

###  3. Flask Web UI (Jinja2 Templates)

- `home.html` – Homepage  
- `about.html` – Shows statistics, counts, metadata  
- `data.html` – Display selected table  
- `upload.html` – Upload CSV file  
- `add.html` – Add a new record  
- `delete.html` – Delete records  
- `hist_stats.html` – Statistics & charts  
- `base.html` – Base template for all pages

###  4. Static Assets

- CSS styles under `static/css/`
- Images under `static/images/`

##  Project Structure

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
    │   └── (uploaded CSV files)
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

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Adel4itca/DAB111_G13_Project.git
cd DAB111_G13_Project
````

###  Create a Virtual Environment

```bash
python -m venv venv
```

###  Install Dependencies

```bash
pip install -r requirements.txt
```

##  Run the Application

Start Flask:

```bash
python app.py
```

Open in a browser:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

## How to Upload CSV Files

1. Go to the **Upload** page
2. Select a `.csv` file based on the books dataset
3. Click **Upload**
4. Data is stored in **SQLite** automatically

## Data Pages

* View tables
* Search data
* Add new records
* Delete records
* View statistics (record count, selected rows, charts)

## Technologies Used

* Python 3
* Flask
* SQLite
* Pandas
* Matplotlib
* HTML/CSS (Jinja2 templates)

## Team Members — Group 13

* Adel Hasan – 0888146
* Sumit Singh Gulshan – 0888735

##License

This project is for educational use for the DAB111 course at St. Clair
College.

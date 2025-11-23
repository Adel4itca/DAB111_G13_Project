**DAB111 Group Project**

##  Project Title: Books Data Management System (Flask + SQLite)**

**Course:** DAB111
**Project Type:** Data Collection → Database → Flask Website
**Group:** Adel Hasan 0888146 ,Sumit Singh Gulshan 0888735

**1. Overview**

This project demonstrates a complete data workflow using Python, SQLite, and Flask.
It includes:

* Collecting a real dataset
* Storing it inside a SQLite database
* Displaying the data through a Flask-based website
* Allowing users to search, add, and delete records
* Visualizing basic statistics (Histogram of categories)

The goal is to show practical skills in data processing, database management, and web development—using a single dataset end-to-end.

## **2. Dataset Information**

**Dataset Source:**
Kaggle – *Books Dataset*
🔗 [https://www.kaggle.com/datasets/jalota/books-dataset](https://www.kaggle.com/datasets/jalota/books-dataset)

This dataset contains several variables such as book titles, categories, prices, ratings, reviews, and images. It is suitable for storage in a spreadsheet and meets project requirements (5+ variables, multiple data types).

### **Variables Used in This Project**

| Variable          | Type     | Description              |
| ----------------- | -------- | ------------------------ |
| BookID            | Integer  | Unique book identifier   |
| Title             | Text     | Name of the book         |
| Category          | Text     | Genre/category           |
| Price             | Float    | Book selling price       |
| Price_After_Tax   | Float    | Final price with tax     |
| Tax_amount        | Float    | Tax added to the price   |
| Avilability       | Text     | In-stock or out-of-stock |
| Number_of_reviews | Integer  | Customer reviews         |
| Stars             | Integer  | Rating (0–5)             |
| Book_Description  | Text     | Description of the book  |
| Image_Link        | Text/URL | Book cover               |

(Defined in the About page and code base )

---

## 3. Database Design (SQLite)**

The project uses **SQLite**, a lightweight local database included with Python.

### **Database File**

```
database/books.db
```

### **Table**

Only one table is required: **books**

The table is automatically created using `pandas.to_sql()` when a dataset is uploaded.

### **Insertion**

Users can:

* Upload a CSV file
* Add a new book manually via the website
* Delete records using the BookID

All insertions are handled in the Flask backend using `sqlite3` (as required).

---

## 4. Flask Website**

A Flask web application serves the data and provides all required functionality.

### **Main Features**

Home page
About page (dataset + variable definitions)
Data page (view + search)
Upload CSV
Add new book
Delete book
Histogram chart for category frequency

---

### **Website Routes**

| Route         | Description                           |
| ------------- | ------------------------------------- |
| `/`           | Home page                             |
| `/about`      | Dataset details + variable dictionary |
| `/data`       | View books table + search bar         |
| `/upload`     | Upload new CSV → stored into SQLite   |
| `/add`        | Add a new book record                 |
| `/delete`     | Remove book by BookID                 |
| `/hist_stats` | Histogram visualization of categories |

(All functionality implemented in **app.py** )

---

## 5. Project Folder Structure**

```
DAB111_G13_Project/
│
├── data collection/
│   └── books dataset (Book_Dataset_1.csv)
│
├── database/
│   └── books.db
│
├── website/
│   ├── templates/
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── data.html
│   │   ├── upload.html
│   │   ├── add.html
│   │   ├── delete.html
│   │   └── hist_stats.html
│   └── static/
│       └── css/
│           └── style.css
│
├── app.py
├── README.md
└── requirements.txt
``` 
## 6. How to Run the Project**

  ### Step 1 — Install required packages**
       pip install -r requirements.txt
  ### **Step 2 — Run the Flask app**
        python app.py
  ### **Step 3 — Open in browser**
        http://127.0.0.1:5000/


## 7. Key Functionalities Demonstrated**

### ✔ Data Collection

* Data sourced from Kaggle
* Prepared using pandas

### ✔ Database

* SQLite DB with 1 table (`books`)
* Insert, delete, select operations using `sqlite3`

### ✔ Website

* Flask routes
* Search functionality
* Add & Delete CRUD operations
* Data display with HTML table
* Histogram visualization with matplotlib

### ✔ Requirements Met

* At least 5 variables
* Multiple data types
* One SQLite table
* Flask-based website
* About page with variable definitions
* Data page with data sample
* README.md explaining full project
* Requirements.txt for installation

---

## **📦 8. requirements.txt**

Example content:

```
Flask
pandas
matplotlib
```

Add more if used in your code.

---

## **📊 9. Visualization Example**

Your `/hist_stats` page generates a histogram that shows:

* How many categories contain `1`, `2`, `3`, … books
* Helps analyze how books are distributed across genres

(This plot is automatically embedded as a base64 image.)

---

## **👥 10. Group Members**

(Add names + IDs here)

---

## **📚 11. Academic Reference (Dataset)**

Jalota, R. *Books Dataset.* Kaggle.
[https://www.kaggle.com/datasets/jalota/books-dataset](https://www.kaggle.com/datasets/jalota/books-dataset)

---

## **✅ 12. Conclusion**

This project integrates data collection, data processing, database storage, and web development into a single hands-on system. It demonstrates practical skills in Python programming, SQL operations, and Flask-based application development—aligned with all DAB111 course requirements.



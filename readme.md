# **DAB111 Group 13 – Flask Data Website Project**

This project was developed as part of the **DAB111 / DBA111** course at **St. Clair College**.
It is a complete **Flask web application** that allows users to upload book data, convert it into a SQLite database, view and search the dataset, perform CRUD operations, and generate statistics and visualizations.

The project demonstrates core concepts of **databases, Python programming, web development, and data analytics**, aligned with course requirements.

---

## **Application Flowchart**

The following flowchart explains the full workflow of the Flask application, including routing, database validation, CSV upload, CRUD operations, and statistics generation.

![Flowchart](static/images/FlowChart.png)

---

# **Features of the Application**

### **1. CSV Upload System**

* Upload a dataset file (`.csv`) containing book data.
* Automatically reads the file using **Pandas**.
* Stores the first 500 rows into a SQLite database table named **books**.

---

### **2. Database Integration (SQLite)**

* The system uses a local **books.db** database.
* Automatically creates or replaces the `books` table when uploading new data.
* Ensures fast and efficient data storage and retrieval.

---

### **3. Search and Data Viewing**

The **Data** page allows users to:

* View the entire books table
* Search by:

  * **Title**
  * **Category**
  * **BookID**
* Uses SQL `LIKE` queries to support partial matches.

---

### **4. Application Functions **

* **Create:** Add new book records through a web form
* **Read:** View and filter book data
* **Delete:** Remove any book by its BookID

These operations are integrated with SQLite for persistent storage.

---

### **5. Visual Analytics**

* The **Statistics** page generates a histogram showing how often each category appears.
* Plot is created with **Matplotlib** and saved under `static/images/` so it can be displayed in the browser.

---

### **6. Clean & Organized Web UI**

The Flask application uses:


* Navigation menu for all pages
* Error messages when database/table is missing
* Success messages after actions (upload, add, delete)

---

### **7. Error Handling**

The app  handles:

* Missing database file
* Missing books table
* Invalid CSV uploads
* Empty search queries
* Nonexistent BookID during deletion

---

# **Dataset Information**

### **About the Dataset**

The dataset was found in kaggle for students analyses .The scraped dataset was cleaned and published on Kaggle.

**Original dataset source:**
[https://www.kaggle.com/datasets/jalota/books-dataset](https://www.kaggle.com/datasets/jalota/books-dataset)

---

### **Dataset Fields**

| Column Name           | Description                  |
| --------------------- | ---------------------------- |
| **BookID**            | Unique ID of each book       |
| **Title**             | Full book title              |
| **Category**          | Genre/category               |
| **Price**             | Price before tax             |
| **Price_After_Tax**   | Final price including tax    |
| **Tax_amount**        | Applied tax amount           |
| **Availability**      | Books in stock               |
| **Number_of_reviews** | Number of customer reviews   |
| **Book_Description**  | Summary/overview of the book |
| **Image_Link**        | URL to cover image           |
| **Stars**             | Rating (0–5)                 |

---

#  **Project Structure**

```
DAB111_G13_Project/
│
├── app.py
├── README.md
├── requirements.txt
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
│       └── FlowChart.png
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
```

---

#  **Installation & Setup**

### **1. Clone the Repository**

```bash
git clone https://github.com/Adel4itca/DAB111_G13_Project.git
cd DAB111_G13_Project
```

### **2. Create a Virtual Environment**

```bash
python -m venv venv
```

### **3. Activate the Virtual Environment**

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### **4. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **5. Run the Application**

```bash
python app.py
```

Open your browser:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

# 🧭 **How to Use the Application**

### **1. Home Page**

Basic welcome page and navigation.

---

### **2. Upload CSV**

* Navigate to **Upload**
* Select a `.csv` dataset
* The system loads the data into SQLite

---

### **3. View Data**

* View all books
* Search using title, category, or BookID
* Displayed in a clean, scrollable table

---

### **4. Add New Book**

* Fill the form fields
* Submit to insert a new record into SQLite
* Confirmation message appears

---

### **5. Delete Book**

* Enter the BookID to delete
* The system removes it from SQLite
* Shows success or "not found" message

---

### **6. Statistics**

* Generates histogram for category frequency
* Automatically updates if database changes

---


#  **Technologies Used**

* **Python 3.12+**
* **Flask Framework**
* **SQLite**
* **Pandas**
* **Matplotlib**
* **HTML / CSS**
* **Jinja2 Templates**

---

#  **Team Members — Group 13**

| Name                    | Student ID |
| ----------------------- | ---------- |
| **Adel Hasan**          | 0888146    |
| **Sumit Singh Gulshan** | 0888735    |

---

#  **License**

This project is created solely for educational use in the
**DAB111 – Database Fundamentals** course at **St. Clair College**.


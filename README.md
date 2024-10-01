File Upload and Analysis
Overview
This project provides a web application that allows users to upload CSV or Parquet files. The backend processes the uploaded files, analyzes the data, and returns information about each column, including data types, counts of unique, duplicate, null, and empty values, and the total number of records. The results are displayed in a user-friendly table format.

Features
Upload CSV and Parquet files.
Analyze the uploaded data for:
Column names
Data types
Unique values count
Duplicate values count
Null values count
Empty string count
Total records count
Display results in a structured table.
Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: Python with Flask
Data Processing: Pandas
Cross-Origin Resource Sharing (CORS): Flask-CORS
Clone the Repository
git clone https://github.com/your-username/your-repository.git
cd your-repository
File Structure
│
├── data_analyzer.py          # Flask backend application
├── interface.html      # Frontend HTML file
├── style.css      # CSS styles
└── actions.js       # JavaScript for frontend functionality
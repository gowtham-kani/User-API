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
Testing with Postman
You can also test the file upload API using Postman.

Open Postman.
Create a new request:
Set the request type to POST.
Enter the URL: http://127.0.0.1:5000/upload.
Select the Body tab:
Choose form-data.
Add a key named file and set the type to File.
Upload a CSV or Parquet file from your local system.
Send the Request:
Click the Send button.
You should receive a JSON response containing the analysis results.

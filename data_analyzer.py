from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import boto3
import os
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

# Set maximum upload size to 200 MB
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

@app.route('/upload', methods=['POST'])
def upload_file():
   # Check if an S3 URL is provided
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not (file.filename.endswith('.csv') or file.filename.endswith('.parquet')):
        return jsonify({"error": "Unsupported file type. Only .csv and .parquet are allowed."}), 400

    # Read the file using pandas
    try:
        results = []
        total_records = 0

        if file.filename.endswith('.csv'):
            # If the file is large, read it in chunks
            chunk_size = 10**6  # Adjust chunk size based on memory constraints
            data_iterator = pd.read_csv(file, chunksize=chunk_size)

            for chunk in data_iterator:
                total_records += len(chunk)
                results.extend(analyze_dataframe(chunk))

        elif file.filename.endswith('.parquet'):
            data = pd.read_parquet(file)
            total_records = len(data)
            results = analyze_dataframe(data)

        return jsonify({
            "results": results,
            "total_records": total_records,
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def analyze_dataframe(df):
    """Calculate metrics for the provided dataframe."""
    results = []
    total_records = len(df)

    for column in df.columns:
        col_data = df[column]
        col_type = str(col_data.dtype)

        # Analyze the types within the 'object' column
        type_analysis = analyze_object_column(col_data) if col_type == 'object' else None

        results.append({
            'column_name': column,
            'data_type': col_type,
            'specific_types': type_analysis,
            'unique_values': int(col_data.nunique()),
            'duplicate_values': int(total_records - col_data.nunique() - col_data.isnull().sum()),
            'null_values': int(col_data.isnull().sum()),
            'empty_values': int((col_data == '').sum()) if col_type == 'object' else 0,
            'total_records': total_records
        })

    return results

def analyze_object_column(column):
    """Analyzes the types of values within an object column."""
    type_counts = column.apply(lambda x: identify_type(x)).value_counts()
    
    # Return a summary of types found in the column
    return ', '.join([f"{t}: {count}" for t, count in type_counts.items()])    

def identify_type(value):
    """Identifies the type of a value."""
    if pd.isna(value):
        return 'NaN'
    elif isinstance(value, str):
        return 'string'
    elif isinstance(value, int):
        return 'integer'
    elif isinstance(value, float):
        return 'float'
    else:
        return 'other'

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.json
        s3_url = data.get('s3_url')
        bucket_name = data.get('bucket_name')

        if not s3_url:
            return jsonify({"error": "S3 URL is required"}), 400

        if not bucket_name:
            return jsonify({"error": "Bucket name is required"}), 400

        # Parse the S3 URL
        object_key = parse_s3_url(s3_url)

        # Ask for AWS credentials in the console
        aws_access_key_id = input("Enter AWS Access Key ID: ")
        aws_secret_access_key = input("Enter AWS Secret Access Key: ")

        # Set the local file path where the file will be downloaded
        local_file_path = os.path.join(os.getcwd(), object_key.split('/')[-1])

        # Download the file
        success = download_file_from_s3(bucket_name, object_key, aws_access_key_id, aws_secret_access_key, local_file_path)

        if success:
            return jsonify({"message": f"File downloaded successfully: {local_file_path}"}), 200
        else:
            return jsonify({"error": "File download failed."}), 500

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
def parse_s3_url(s3_url):
    """Parses the S3 URL and returns the object key."""
    parsed_url = urlparse(s3_url)
    
    if not parsed_url.scheme in ['s3', 'https']:
        raise ValueError("Invalid S3 URL format: URL must start with 'https://'.")
    
    object_key = parsed_url.path.lstrip('/')
    return object_key

def download_file_from_s3(bucket_name, object_key, aws_access_key_id, aws_secret_access_key, local_file_path):
    try:
        # Initialize S3 client with provided AWS credentials
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='us-east-2'  # Set the correct region
        )

        # Download the file from S3
        s3.download_file(bucket_name, object_key, local_file_path)
        return True
    except Exception as e:
        print(f"Error while downloading file: {e}")
        return False
if __name__ == '__main__':
    app.run(debug=True)

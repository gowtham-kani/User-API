from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import boto3
import os

app = Flask(__name__)
CORS(app)

# Set maximum upload size to 200 MB
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

@app.route('/upload', methods=['POST'])
def upload_file():
   # Check if an S3 URL is provided
    s3_url = request.form.get('s3Url')
    
    if s3_url and s3_url.startswith('https://'):
        # Download from S3
        bucket_name, object_key = extract_bucket_and_key(s3_url)
        
        # Create an S3 client (Assuming AWS credentials are set in environment variables)
        s3_client = boto3.client('s3')
        local_file_path = os.path.join('downloads', os.path.basename(object_key))
        os.makedirs('downloads', exist_ok=True)

        try:
            s3_client.download_file(bucket_name, object_key, local_file_path)
            file = open(local_file_path, 'rb')
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
    else:
        return jsonify({'error': 'No file or valid S3 URL provided'}), 400
    try:
        
        if file.filename.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.filename.endswith('.parquet'):
            data = pd.read_parquet(file)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        # Calculate metrics
        total_records = len(data)
        null_counts = data.isnull().sum()
        unique_counts = data.nunique()
        empty_counts = (data == '').sum()
        data_types = data.dtypes

        results = []
        for column in data.columns:
            col_type = str(data_types[column])
            if col_type == 'object':
                # Analyze the types within the 'object' column
                type_analysis = analyze_object_column(data[column])

            results.append({
                'column_name': column,
                'data_type': col_type + f" ({type_analysis})",
                'unique_values': int(unique_counts[column]),
                'duplicate_values': int(total_records - unique_counts[column] - null_counts[column]),
                'null_values': int(null_counts[column]),
                'empty_values': int(empty_counts[column]),
                'total_records': total_records
            })
        else:
                results.append({
                    'column_name': column,
                    'data_type': col_type,
                    'unique_values': int(unique_counts[column]),
                    'duplicate_values': int(total_records - unique_counts[column] - null_counts[column]),
                    'null_values': int(null_counts[column]),
                    'empty_values': int(empty_counts[column]),
                    'total_records': total_records
                })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_bucket_and_key(s3_url):
    """Extract bucket name and object key from S3 URL."""
    path_parts = s3_url.replace("https://", "").split("/")
    bucket_name = path_parts[0]
    object_key = "/".join(path_parts[1:])
    return bucket_name, object_key

def analyze_object_column(column):
    """Analyzes the types of values within an object column."""
    # Determine the types in the object column
    types_in_column = column.apply(lambda x: type(x).__name__).unique()
    
    # Determine the frequency of each type
    type_counts = column.apply(lambda x: type(x).__name__).value_counts()
    
    # Return a summary of types found in the column
    return ', '.join([f"{t}: {count}" for t, count in type_counts.items()])    

if __name__ == '__main__':
    app.run(debug=True)

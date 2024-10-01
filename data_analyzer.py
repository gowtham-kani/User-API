from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

# Set maximum upload size to 200 MB
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

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
            results.append({
                'column_name': column,
                'data_type': str(data_types[column]),
                'unique_values': int(unique_counts[column]),
                'duplicate_values': int(total_records - unique_counts[column] - null_counts[column]),
                'null_values': int(null_counts[column]),
                'empty_values': int(empty_counts[column]),
                'total_records': total_records
            })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const s3UrlInput = document.getElementById('s3Url');
    const formData = new FormData();
    const resultDiv = document.getElementById('result');
document.getElementById('clearButton').addEventListener('click', function() {
        // Clear the file input, S3 URL input, and results
        document.getElementById('fileInput').value = '';
        document.getElementById('s3Url').value = '';
        document.getElementById('result').innerHTML = '';
    });
    
    // Clear the result if user uploads a new file or provides a new S3 URL
    resultDiv.innerHTML = '';

    // Check if the user provided an S3 URL
    if (s3UrlInput.value) {
        // Reset file input and remove previously uploaded file
        fileInput.value = '';
        formData.append('s3Url', s3UrlInput.value);

        // Clear the previously uploaded file if a new S3 URL is provided
        alert('Previous file upload cleared. Processing S3 file...');

    } else if (fileInput.files.length > 0) {
        // If user uploaded a file, append it to the formData
        formData.append('file', fileInput.files[0]);
    } else {
        // If neither file nor S3 URL is provided, show an error
        alert('Please upload a file or provide a valid S3 URL.');
        return;
    }

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        displayResults(data);
        // If S3 file was downloaded, show a popup message
        if (s3UrlInput.value) {
            alert('S3 file successfully downloaded and processed.');
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    });
});

function displayResults(data) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `<h2>Analysis Results</h2>`;

    if (!data || data.length === 0) {
        resultDiv.innerHTML += `<p>No data received from the server.</p>`;
        return;
    }

    const table = document.createElement('table');
    const header = table.createTHead();
    const headerRow = header.insertRow(0);
    const headers = [
        'Column Name',
        'Data Type',
        'Unique Values',
        'Duplicate Values',
        'Null Values',
        'Empty Values',
        'Total Records'
    ];

    headers.forEach((text) => {
        const th = document.createElement('th');
        th.innerText = text;
        headerRow.appendChild(th);
    });

    const body = table.createTBody();
    data.forEach(row => {
        const newRow = body.insertRow();
        newRow.innerHTML = `
            <td>${row.column_name || 'N/A'}</td>
            <td>${row.data_type || 'N/A'}</td>
            <td>${row.unique_values || 0}</td>
            <td>${row.duplicate_values || 0}</td>
            <td>${row.null_values || 0}</td>
            <td>${row.empty_values || 0}</td>
            <td>${row.total_records || 0}</td>
        `;
    });

    resultDiv.appendChild(table);
}

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    const resultDiv = document.getElementById('uploadResult');

    
    // Clear the result if user uploads a new file or provides a new S3 URL
    resultDiv.innerHTML = '';

    // Check if the user provided an S3 URL
    if (fileInput.files.length > 0) {
        // If user uploaded a file, append it to the formData
        formData.append('file', fileInput.files[0]);
    } else {
        // If no file is provided, show an error
        alert('Please upload a file.');
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


// S3 Download Logic
document.getElementById('downloadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const s3Url = document.getElementById('s3Url').value;
    const bucketName = document.getElementById('bucketName').value;

    // Check if file upload form is filled
    if (document.getElementById('fileInput').files.length > 0) {
        alert('Please choose either file upload or S3 URL, not both.');
        return;
    }

    fetch('http://127.0.0.1:5000/download', {  // Change this to your backend URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            s3_url: s3Url,
            bucket_name: bucketName
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('downloadResult').innerText = data.message || data.error;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('downloadResult').innerText = 'Error: ' + error.message;
    });
});

// Clear button functionality
document.getElementById('clearButton').addEventListener('click', function() {
    // Clear all inputs and results
    document.getElementById('fileInput').value = '';
    document.getElementById('s3Url').value = '';
    document.getElementById('bucketName').value = '';
    document.getElementById('uploadResult').innerHTML = '';
    document.getElementById('downloadResult').innerText = '';
});
function displayResults(data) {
    const resultDiv = document.getElementById('uploadResult');
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

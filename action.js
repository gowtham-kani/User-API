document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

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

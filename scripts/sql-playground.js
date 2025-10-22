// scripts/sql-playground.js
document.addEventListener('DOMContentLoaded', function() {
    const sqlInput = document.getElementById('sql-input');
    const runButton = document.getElementById('run-sql');
    const resultContainer = document.getElementById('result-container');

    // Load the SQL.js library
    let db;
    initSqlJs().then(SQL => {
        // Load the SQLite database
        fetch('dados/banco_exemplo.sqlite')
            .then(response => response.arrayBuffer())
            .then(buffer => {
                db = new SQL.Database(new Uint8Array(buffer));
                console.log('Database loaded successfully');
            });
    });

    // Function to run SQL query
    runButton.addEventListener('click', () => {
        const sqlQuery = sqlInput.value;
        try {
            const result = db.exec(sqlQuery);
            displayResult(result);
        } catch (error) {
            resultContainer.innerHTML = `<p class="text-red-500">Erro: ${error.message}</p>`;
        }
    });

    // Function to display the result in a table
    function displayResult(result) {
        resultContainer.innerHTML = ''; // Clear previous results
        if (result.length === 0) {
            resultContainer.innerHTML = '<p>Nenhum resultado encontrado.</p>';
            return;
        }

        const table = document.createElement('table');
        table.className = 'min-w-full border-collapse border border-gray-200';
        
        // Create table headers
        const headerRow = document.createElement('tr');
        result[0].columns.forEach(column => {
            const th = document.createElement('th');
            th.className = 'border border-gray-300 p-2';
            th.textContent = column;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);

        // Create table rows
        result.forEach(res => {
            res.values.forEach(row => {
                const tr = document.createElement('tr');
                row.forEach(cell => {
                    const td = document.createElement('td');
                    td.className = 'border border-gray-300 p-2';
                    td.textContent = cell;
                    tr.appendChild(td);
                });
                table.appendChild(tr);
            });
        });

        resultContainer.appendChild(table);
    }
});
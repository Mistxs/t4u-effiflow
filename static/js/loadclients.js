function displayErrorMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.text(message);
    errorMessage.removeClass('alert-success').addClass('alert-danger').slideDown();
    setTimeout(function() {
        errorMessage.slideUp();
    }, 3000);
}

function displaySuccessMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.text(message);
    errorMessage.removeClass('alert-danger').addClass('alert-success').slideDown();
    setTimeout(function() {
        errorMessage.slideUp();
    }, 30000);
}

document.getElementById('upload-form').addEventListener('submit', function(event) {
            event.preventDefault();

            var formData = new FormData(this);
            const tableWrap = document.querySelector('.resultTable');
            tableWrap.classList.remove('slide-in');
            var resultContainer = document.getElementById('result');
            resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

            fetch('/clients/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
//                var resultDiv = document.getElementById('result');
                resultContainer.innerHTML = "";
                displaySuccessMessage(data.text)
//                tableWrap.innerHTML = '<h2>Результат:</h2><pre>' + JSON.stringify(data, null, 2) + '</pre>';
//                drawTable(clients)
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        });



function drawTable(clients) {
    const tableWrap = document.querySelector('.resultTable');

    tableWrap.style.display = 'block';
    tableWrap.classList.add('slide-in');

    var table = $('<table class="table">');
    var tbody = $('<tbody>');


    for (var i = 0; i < clients.length; i++) {
        var row = $('<tr>');
        for (var key in clients[i]) {
            row.append($('<td>').text(clients[i][key]));
        }
        tbody.append(row);
    }

    table.append(tbody);

    $('#result').empty().append(table);
}



function saveResult() {
    var salon_id = document.getElementById('salon').value;
    var login = document.getElementById('login').value;
    var password = document.getElementById('pass').value;

    var resultContainer = document.getElementById('result');


    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

     return fetch('/clients/saveClients', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'salon_id': salon_id,
            'login': login,
            'password': password
        })
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var clients = data.text
            resultContainer.innerHTML = "";
//            drawTable(clients)
        } else if (data.status === 'error') {
            displayErrorMessage(data.text);

        }
    })
}
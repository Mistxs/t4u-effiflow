// Вывод сообщений



function displayMessage(message, messageType) {

    var messageContainer = $('#message-container');
    var messageText = $('#message-text');

    messageText.text(message);

    if (messageType === 'error') {
        messageContainer.removeClass('alert-success alert-info').addClass('alert-danger');
    } else if (messageType === 'success') {
        messageContainer.removeClass('alert-danger alert-info').addClass('alert-success');
    } else if (messageType === 'info') {
        messageContainer.removeClass('alert-danger alert-success').addClass('alert-info');
    }

    openMessage(messageContainer);

    $('#close-message').on('click', function() {
        closeMessage(messageContainer);
    });
}

function openMessage(container) {
    container.slideDown();
}

function closeMessage(container) {
    container.slideUp();
}


function getClients() {
    var salon_id = document.getElementById('salon').value;
    var login = document.getElementById('login').value;
    var password = document.getElementById('pass').value;
    var resultContainer = document.getElementById('result');

    const buttonElement = document.getElementById('getbtn');
    const spinnerElement = document.getElementById('spinner');

    // Показываем спиннер и блокируем кнопку во время запроса
    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';


     return fetch('/getClients', {
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
            displayClients(clients)
            document.querySelectorAll('.btn').forEach(function(btn) {
                btn.disabled = false;
                btn.style.cursor = "pointer";
              });
             // Скрываем спиннер и разблокируем кнопку после выполнения запроса
            buttonElement.disabled = false;
            displayMessage("Клиенты получены", 'success');
            spinnerElement.style.display = 'none';
        } else if (data.status === 'error') {
            displayMessage(data.text, 'error');
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';

        }
    })
}

function displayClients(clients) {
    var table = $('<table class="table table-striped programs table-responsive">');
    var thead = $('<thead>').append('<tr><th>ID</th><th>Телефон</th><th>Имя</th><th>Отчество</th><th>Фамилия</th></tr>');
    table.append(thead);

    var tbody = $('<tbody>');
    for (var i = 0; i < clients.length; i++) {
        var record = clients[i];
        var row = $('<tr>');
        row.append('<td>' + record.id + '</td>');

        row.append('<td>' + record.phone + '</td>');
        row.append('<td>' + record.name + '</td>');
        row.append('<td>' + record.patronymic + '</td>');
        row.append('<td>' + record.surname + '</td>');

        tbody.append(row);
    }

    table.append(tbody);

    $('#result').empty().append(table);
}


function parseFIO() {
    var salon_id = document.getElementById('salon').value;
    var login = document.getElementById('login').value;
    var password = document.getElementById('pass').value;
    var resultContainer = document.getElementById('result');


    const buttonElement = document.getElementById('parsebtn');
    const spinnerElement = document.getElementById('spinner2');


    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';

    return fetch('/parsefio', {
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
            displayClients(clients)
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';
            displayMessage("Разбили на ФИО успешно", 'success');

            getReport()

        } else if (data.status === 'error') {
            displayMessage(data.text, 'error');
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';

        }
    })
}


function getError() {
    var resultContainer = document.getElementById('result');


      return fetch('/getError', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var clients = data.text
            resultContainer.innerHTML = "";
            displayClients(clients)
        } else if (data.status === 'error') {
            displayErrorMessage(data.text);

        }
    })
}


function getReport() {
    var resultContainer = document.getElementById('result');

    return fetch('/getReport', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.blob())
    .then(blob => {
        // Создаем объект URL для файла
        var url = URL.createObjectURL(blob);

        // Меняем расширение файла на xlsx
        var a = document.createElement('a');
        a.href = url;
        a.download = 'report.xlsx';
        a.click();

    })
    .catch(error => {
        // Выводим сообщение об ошибке, если что-то пошло не так
        displayErrorMessage('Произошла ошибка при получении файла.');
    });
}


function saveResult() {
    var salon_id = document.getElementById('salon').value;
    var login = document.getElementById('login').value;
    var password = document.getElementById('pass').value;
    var resultContainer = document.getElementById('result');

    const buttonElement = document.getElementById('savebtn');
    const spinnerElement = document.getElementById('spinner3');

    // Показываем спиннер и блокируем кнопку во время запроса
    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';


      return fetch('/saveClients', {
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
            resultContainer.innerHTML = "";
            // Скрываем спиннер и разблокируем кнопку после выполнения запроса
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';
            displayMessage(data.text, 'success')

        } else if (data.status === 'error') {
            displayMessage(data.text, 'error');
            // Скрываем спиннер и разблокируем кнопку после выполнения запроса
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';

        }
    })
}


// блокируем все кнопки пока не получат данные
document.querySelectorAll('.btn').forEach(function(btn) {
  if (btn.innerText !== "Выгрузить клиентов") {
    btn.disabled = true;
    btn.style.cursor = "not-allowed";
  }
});


var socket = io({ transports: ['websocket'] });

socket.on('parseclients', function (data) {
    displayMessage("1. Получение клиентов: " + data.counter.currentcount + ' / ' + data.counter.totalclients,"info");
});

socket.on('addedBD', function (data) {
    displayMessage("2. Добавляем дату рождения: " + data.counter.currentcount + ' / ' + data.counter.totalclients,"info");
});

socket.on('splitFIO', function (data) {
    displayMessage("3. Разбиваем ФИО: " + data.counter.currentcount + ' / ' + data.counter.totalclients,"info");
});

socket.on('saveResult', function (data) {
    displayMessage("4. Сохраняем изменения: " + data.counter.currentcount + ' / ' + data.counter.totalclients,"info");
});

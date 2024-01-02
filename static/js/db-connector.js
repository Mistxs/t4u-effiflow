function displayErrorMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.html(message);
    errorMessage.removeClass('alert-success').addClass('alert-danger').slideDown();
}

function displaySuccessMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.text(message);
    errorMessage.removeClass('alert-danger').addClass('alert-success').slideDown();
}


document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('extModal');
    const modalTitle = modal.querySelector('.modal-title');
    const modalBody = modal.querySelector('.modal-body');
    const actButton = document.getElementById('actButton');

    // Обработчик кликов на элементах списка
    document.getElementById('message-list').addEventListener('click', function (event) {
        const target = event.target;
        if (target.matches('span[data-bs-toggle="modal"][data-bs-target="#extModal"]')) {
            const listItem = target.closest('li');
            const flag = listItem.dataset.mpId;
            const title = listItem.querySelector('.chat-title').textContent;
            const salon_id = document.getElementById('salon').value;
            modalTitle.textContent = title;
            actButton.setAttribute('flag', flag);



        }
    });

    document.getElementById('actButton').addEventListener('click', function (event) {
        const salon_id = document.getElementById('salon').value;
        const flag = actButton.getAttribute('flag');
        sendQuery(flag,salon_id)
    });

    function displayResult(data) {
    var table = $('<table class="table table-hover table-striped table-responsive">');
    var thead = $('<thead>').append('<tr><th>Дата изменения</th><th>ID Юзера</th><th>Телефон юзера</th><th>Имя юзера</th><th>Название приложения</th><th>Предыдущий статус</th><th>Новый статус</th><th>Источник изменения</th></tr>');
    table.append(thead);

    var tbody = $('<tbody>');
    for (var i = 0; i < data.length; i++) {
        var record = data[i];
        var row = $('<tr>');
        row.append('<td>' + record.changed_at + '</td>');
        row.append('<td>' + record.user_id + '</td>');
        row.append('<td>' + record.phone + '</td>');
        row.append('<td>' + record.firstname + '</td>');
        row.append('<td>' + record.title + '</td>');
        row.append('<td>' + record.status_from + '</td>');
        row.append('<td>' + record.status_to + '</td>');
        row.append('<td>' + record.source + '</td>');





        tbody.append(row);
    }

    table.append(tbody);

    $('#result').empty().append(table);
    }

    // Загрузка данных через AJAX запрос при загрузке страницы
    function sendQuery(flag, salon) {
    const buttonElement = document.getElementById('actButton');
    const spinnerElement = document.getElementById('spinner');

    // Показываем спиннер и блокируем кнопку во время запроса
    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';

    fetch('https://b5898dc6e4bc-8806955829454616363.ngrok-free.app/dbconnect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "flag": flag,
            "salon_id": salon
        })
    })
    .then(response => response.json())
    .then(data => {
    buttonElement.disabled = false;
    spinnerElement.style.display = 'none';
    if (data.status === 'success') {

        if (flag === 'bulk_messages') {
            // Дополнительная проверка для flag === 'bulk_message'
            if (data.result === 'done') {
                displaySuccessMessage('Связь с типами для массовых рассылок подключена');
            } else if (data.result === 'empty') {
                // Передаем текст ошибки и SQL-запрос в displayErrorMessage
                const errorMessageHTML = "Связь отсутствует. Запрос для включения:<br><pre><code class='sql'>" + data.query + "</code></pre> <br> Ответ от БД: <pre>" + data.sqlresponse + "</pre>";
                displayErrorMessage(errorMessageHTML);
                hljs.highlightAll()
            }
        } else if (flag === 'fraud') {
            if (data.result === 'empty') {
                displaySuccessMessage('Подключенного антифрод модуля не обнаружено');
            } else if (data.result === 'done') {
                // Передаем текст ошибки и SQL-запрос в displayErrorMessage
                const errorMessageHTML = "Антифрод включен. Запрос для отключения:<br><pre><code class='sql'>" + data.query + "</code></pre>  <br> Ответ от БД: <pre>" + data.sqlresponse + "</pre>";
                displayErrorMessage(errorMessageHTML);
                hljs.highlightAll()
            }
        } else if (flag === 'mp_log') {
            if (data.result === 'empty') {
                displaySuccessMessage('Возвращено 0 строк. Может, неверный филиал? Или не было установок');
            } else {
                displayResult(data.result);
            }
        }
    } else if (data.status === 'error') {
        displayErrorMessage(data.text);
    }
});
}


});

 function performAction(actionFunction) {
    var loader = document.getElementById('loader');
    var buttons = document.getElementsByClassName('btn');

    // Показываем индикатор загрузки
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].disabled = true;
    }
    loader.style.display = 'block';

    // Выполняем действие
    actionFunction()
        .then(() => {
            // Скрываем индикатор загрузки и активируем кнопки
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].disabled = false;
            }
            loader.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);

            // Скрываем индикатор загрузки и активируем кнопки
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].disabled = false;
            }
            loader.style.display = 'none';
        });
}

// Функции действий
function unlock() {
    var record_link = document.getElementById('record_link').value;
    var resultContainer = document.getElementById('result');

    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    return fetch('/unlocker/action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'record_link': record_link
        })
    })
    .then(response => response.text())
    .then(data => {
        resultContainer.innerHTML = data;
    });
}

// Функции действий
function getinfo() {
    var record_link = document.getElementById('record_link').value;
    var resultContainer = document.getElementById('result');

    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    return fetch('/unlocker/getrecord', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'record_link': record_link
        })
    })
    .then(response => response.text())
    .then(data => {
        resultContainer.innerHTML = data;
    });
}
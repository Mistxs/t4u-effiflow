function displayErrorMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.text(message);
    errorMessage.removeClass('alert-success').addClass('alert-danger').slideDown();
}

function displaySuccessMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.text(message);
    errorMessage.removeClass('alert-danger').addClass('alert-success').slideDown();
}

function startCopy() {

     // Получение данных из формы
    var chain_id = document.getElementById("chain_id").value;

    return fetch('/exportgoods', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'chain_id': chain_id
        })
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            displaySuccessMessage("Функция по копированию завершилась");
//            drawTable(dataset)
        } else if (data.status === 'error') {
            displayErrorMessage(data.text);
        }
    })
}

var socket = io();

// Обработка события file-download от сервера
socket.on('file-download', (data) => {
    // data.file содержит base64-кодированный файл
    // Далее вы можете обработать файл, например, скачать его на клиенте
    // Создание элемента <a> для скачивания файла
    const a = document.createElement('a');
    a.href = 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + data.file;
    a.download = 'exported_file.xlsx';
    a.click();
});

socket.on('text', (data) => {
    console.log(data);
});

socket.on('file-ready', function(data) {
            // Обработка сообщения о готовности файла
            console.log('File ready:', data);
            document.getElementById('result').innerText = 'Файл готов. ' +
                'Ссылка для скачивания: ' + data.link;
        });
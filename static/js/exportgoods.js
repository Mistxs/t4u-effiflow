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

    const buttonElement = document.getElementById('actionButton');
    const spinnerElement = document.getElementById('spinner');

    // Показываем спиннер и блокируем кнопку во время запроса
    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';

    return fetch('/exportgoods', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'chain_id': chain_id
        })
    })

    .then(response => response.blob())
    .then(blob => {
        document.querySelectorAll('.btn').forEach(function(btn) {
                btn.disabled = false;
                btn.style.cursor = "pointer";
              });
             // Скрываем спиннер и разблокируем кнопку после выполнения запроса
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';

        // Создаем объект URL для файла
        var url = URL.createObjectURL(blob);

        // Меняем расширение файла на xlsx
        var a = document.createElement('a');
        a.href = url;
        a.download = 'report.xlsx';
        a.click();

    })
}

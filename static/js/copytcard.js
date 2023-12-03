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
    const tableWrap = document.querySelector('.resultTable');
    tableWrap.classList.remove('slide-in');
    tableWrap.style.display = 'none';
    tableWrap.style.display = 'block';
    tableWrap.classList.add('slide-in');

    var resultContainer = document.getElementById('result');

    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

     // Получение данных из формы
    var formData = {
                salon_from: document.getElementById("salon_from").value,
                salon_to: document.getElementById("salon_to").value,
            };

    return fetch('/copytcard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'dataset': formData
        })
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var dataset = data.dataset
            resultContainer.innerHTML = "";
            displaySuccessMessage("Функция по копированию завершилась");
//            drawTable(dataset)
        } else if (data.status === 'error') {
            resultContainer.innerHTML = "";
            displayErrorMessage(data.text);
        }
    })
}


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

    // Загрузка данных через AJAX запрос при загрузке страницы
    function sendQuery(flag,salon) {
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
                if (data.status === 'success') {
                    displaySuccessMessage(data.text);

                } else if (data.status === 'error') {
                    displayErrorMessage(data.text);
                }
            })
    };

});

function getstatus() {
    const inputElement = document.querySelector('.kkm_input');
    const url = inputElement.value;
    const buttonElement = document.getElementById('checkbtn');
    const spinnerElement = document.getElementById('spinner');

    // Показываем спиннер и блокируем кнопку во время запроса
    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';

    // Удаляем класс анимации, если он был добавлен
    const docStatusElement = document.querySelector('.docstatus');
    docStatusElement.classList.remove('slide-in');

    const badgeSuccess = docStatusElement.querySelector('.bg-success');
    const badgeDanger = docStatusElement.querySelector('.bg-danger');
    const cardTextElement = docStatusElement.querySelector('.card-text');

    badgeSuccess.style.display = 'none'; // Скрываем бейдж Success
    badgeDanger.style.display = 'none'; // Скрываем бейдж Failed
    cardTextElement.textContent = ''; // Очищаем текст

    fetch('/check_document', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ kkm_link: url }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                badgeSuccess.style.display = 'inline'; // Отображаем бейдж Success
                cardTextElement.textContent = `Успешно. Ответ: ${data.text}`;
            } else {
                badgeDanger.style.display = 'inline'; // Отображаем бейдж Failed
                cardTextElement.textContent = `Ошибка: ${data.text}`;
            }

            docStatusElement.style.display = 'block';
            docStatusElement.classList.add('slide-in'); // Добавляем класс для анимации

            // Скрываем спиннер и разблокируем кнопку после выполнения запроса
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';
        })
        .catch(error => {
            console.error(error);

            // Скрываем спиннер и разблокируем кнопку при ошибке
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';
        });
}



function runForce() {
    const inputElement = document.querySelector('.kkm_input');
    const url = inputElement.value;
    const buttonElement = document.getElementById('runbtn');
    const spinnerElement = document.getElementById('spinner2');

    // Показываем спиннер и блокируем кнопку во время запроса
    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';

    // Удаляем класс анимации, если он был добавлен
    const docStatusElement = document.querySelector('.pushstatus');
    docStatusElement.classList.remove('slide-in');

    const badgeSuccess = docStatusElement.querySelector('.bg-success');
    const badgeDanger = docStatusElement.querySelector('.bg-danger');
    const cardTextElement = docStatusElement.querySelector('.card-text');

    badgeSuccess.style.display = 'none'; // Скрываем бейдж Success
    badgeDanger.style.display = 'none'; // Скрываем бейдж Failed
    cardTextElement.textContent = ''; // Очищаем текст

    fetch('/run_force', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ kkm_link: url }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                badgeSuccess.style.display = 'inline'; // Отображаем бейдж Success
                cardTextElement.innerHTML = 'Успешно. Ответ от сервера YC - <a href="#" data-bs-toggle="modal" data-bs-target="#jsonModal">Подробнее</a>';
                const jsonResponseElement = document.getElementById('jsonResponse');
                jsonResponseElement.textContent = JSON.stringify(data.text, null, 2);
            } else {
                badgeDanger.style.display = 'inline'; // Отображаем бейдж Failed
                cardTextElement.textContent = `Ошибка: ${data.text}`;
            }

            docStatusElement.style.display = 'block';
            docStatusElement.classList.add('slide-in'); // Добавляем класс для анимации

            checkStatus();
            
            // Скрываем спиннер и разблокируем кнопку после выполнения запроса
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';
        })
        .catch(error => {
            console.error(error);

            // Скрываем спиннер и разблокируем кнопку при ошибке
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';
        });
}


function checkStatus() {
    const inputElement = document.querySelector('.kkm_input');
    const url = inputElement.value;
    const buttonElement = document.getElementById('checkbtn');
    const spinnerElement = document.getElementById('spinner');

    // Показываем спиннер и блокируем кнопку во время запроса
    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';

    // Удаляем класс анимации, если он был добавлен
    const docStatusElement = document.querySelector('.docstatus_after');
    docStatusElement.classList.remove('slide-in');

    const badgeSuccess = docStatusElement.querySelector('.bg-success');
    const badgeDanger = docStatusElement.querySelector('.bg-danger');
    const cardTextElement = docStatusElement.querySelector('.card-text');

    badgeSuccess.style.display = 'none'; // Скрываем бейдж Success
    badgeDanger.style.display = 'none'; // Скрываем бейдж Failed
    cardTextElement.textContent = ''; // Очищаем текст

    fetch('/check_document', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ kkm_link: url }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                badgeSuccess.style.display = 'inline'; // Отображаем бейдж Success
                cardTextElement.textContent = `Успешно. Ответ: ${data.text}`;
            } else {
                badgeDanger.style.display = 'inline'; // Отображаем бейдж Failed
                cardTextElement.textContent = `Ошибка: ${data.text}`;
            }

            docStatusElement.style.display = 'block';
            docStatusElement.classList.add('slide-in'); // Добавляем класс для анимации

            // Скрываем спиннер и разблокируем кнопку после выполнения запроса
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';
        })
        .catch(error => {
            console.error(error);

            // Скрываем спиннер и разблокируем кнопку при ошибке
            buttonElement.disabled = false;
            spinnerElement.style.display = 'none';
        });
}
function unlock() {
    const inputElement = document.querySelector('.kkm_input');
    const url = inputElement.value;
    const buttonElement = document.getElementById('runbtn');
    const spinnerElement = document.getElementById('spinner');

    // Показываем спиннер и блокируем кнопку во время запроса
    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';

     // Удаляем класс анимации, если он был добавлен
    const docStatusElement = document.querySelector('.unlockstatus');
    docStatusElement.classList.remove('slide-in');

    const badgeSuccess = docStatusElement.querySelector('.bg-success');
    const badgeDanger = docStatusElement.querySelector('.bg-danger');
    const cardTextElement = docStatusElement.querySelector('.card-text');

    badgeSuccess.style.display = 'none'; // Скрываем бейдж Success
    badgeDanger.style.display = 'none'; // Скрываем бейдж Failed
    cardTextElement.textContent = ''; // Очищаем текст


    fetch('/unlocker/action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'record_link': url })
    })
    .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                badgeSuccess.style.display = 'inline'; // Отображаем бейдж Success
                cardTextElement.innerHTML = data.text;
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

// Функции действий
function getinfo() {
    const inputElement = document.querySelector('.kkm_input');
    const url = inputElement.value;
    const buttonElement = document.getElementById('checkbtn');
    const spinnerElement = document.getElementById('spinner2');

    // Показываем спиннер и блокируем кнопку во время запроса
    buttonElement.disabled = true;
    spinnerElement.style.display = 'inline';

     // Удаляем класс анимации, если он был добавлен
    const docStatusElement = document.querySelector('.getinfostatus');
    docStatusElement.classList.remove('slide-in');

    const badgeSuccess = docStatusElement.querySelector('.bg-success');
    const badgeDanger = docStatusElement.querySelector('.bg-danger');
    const cardTextElement = docStatusElement.querySelector('.card-text');

    badgeSuccess.style.display = 'none'; // Скрываем бейдж Success
    badgeDanger.style.display = 'none'; // Скрываем бейдж Failed
    cardTextElement.textContent = ''; // Очищаем текст

    return fetch('/unlocker/getrecord', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'record_link': url
        })
    })
.then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                badgeSuccess.style.display = 'inline'; // Отображаем бейдж Success
                cardTextElement.innerHTML = data.text;
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
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('extModal');
    const modalTitle = modal.querySelector('.modal-title');
    const modalBody = modal.querySelector('.modal-body');
    const eddyLink = document.getElementById('eddyButton');
    const tgLink = document.getElementById('tgButton');

    const resultContainer = document.getElementById('result');
    const percentContainer = document.getElementById('percent');

    // Обработчик кликов на элементах списка
    document.getElementById('message-list').addEventListener('click', function (event) {
        const target = event.target;
        if (target.matches('span[data-bs-toggle="modal"][data-bs-target="#extModal"]')) {
            const listItem = target.closest('li');
            const mpId = listItem.dataset.mpId;
            const title = listItem.querySelector('.chat-title').textContent;

            eddyLink.href = `https://yclients.helpdeskeddy.com/ru/ticket/list/filter/id/search/ticket/${mpId}?search=${mpId}`;
            tgLink.setAttribute('tId',mpId);
            modalTitle.textContent = title;


            fetch('/marketplace/ticketinfo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "ticketid": mpId
                })
            })

            .then(response => response.json())

            .then(data => {
                console.log(data);
                if (data.status === "success" && data.dataset.length > 0) {
                const chatMessages = data.dataset.map(message => {
                    // Получаем имя из первого <p> и убираем его из текста
                    const name = message.text.match(/<p>(.*?)<\/p>/)[1];
                    const nameAndIdPattern = /<p>(.*?)<\/p>ID сообщения: \d+/;
                    const cleanedText = message.text.replace(nameAndIdPattern, '');
                    console.log(cleanedText);
                    return `
                        <div class="message">
                            <p class="chatTitle">
                                <span class="chatUser">${name}</span>
                                <span class="chatDate">${message.date_updated}</span>
                            </p>
                            <div class="chatText">${cleanedText}</div>
                        </div>
                        <hr class="m-3">
                    `;
                });

                const firstTenMessages = chatMessages.slice(0, 10);
                const chatHTML = firstTenMessages.join("");
                    modalBody.innerHTML = chatHTML;
                } else if (data.status === 'error') {
                    modalBody.innerHTML = data.text;
                }

            });

        } else if (target.matches('.star')) {
            // Обработчик кликов на звезде
            target.classList.toggle('fa-star');
            target.classList.toggle('fa-star-o');

            const listItem = target.closest('li');
            const mpId = listItem.dataset.mpId;
            const isFavourite = target.classList.contains('fa-star') ? 1 : 0;

            // Отправляем данные через веб-сокет
            socket.emit('update_favourite_status', { id: mpId, is_favourite: isFavourite });




        }
    });

    // Загрузка данных через AJAX запрос при загрузке страницы
    fetch('/marketplace/data')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            generateList(data.messages);
            generateListModeration(data.moderations);
        });

    document.getElementById('tgButton').addEventListener('click', function (event) {
        const ids = tgLink.getAttribute('tId');
        fetch('/marketplace/chathandler/read', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "ticket_ids": [ids]
                })
            })
    });

    function generateList(data) {
    const list = document.getElementById('message-list');
    // Очистка списка
    list.innerHTML = '';

    // Добавление элементов в список
    data.forEach(function (row) {
        const listItem = document.createElement('li');
        listItem.dataset.mpId = row[0];
        listItem.classList.add('list-group-item', 'list-group-item-action', 'd-flex', 'chat-list', 'justify-content-between', 'align-items-center');

        const titleSpan = document.createElement('span');
        titleSpan.classList.add('chat-title');
        titleSpan.dataset.bsToggle = 'modal';
        titleSpan.dataset.bsTarget = '#extModal';
        titleSpan.textContent = row[1];

        const badgeSpan = document.createElement('span');
        badgeSpan.classList.add('badge', 'bg-primary');
        badgeSpan.textContent = row[2];

        const star = document.createElement('span');
        star.classList.add('star', 'fa-solid', row[3] === 1 ? 'fa-star' : 'fa-star-o'); // Устанавливаем класс в зависимости от is_favourite

        listItem.appendChild(titleSpan);
        listItem.appendChild(badgeSpan);
        listItem.appendChild(star);

        list.appendChild(listItem);
        });
    }

    function generateListModeration(data) {
    const list = document.getElementById('moderationList');
    // Очистка списка
    list.innerHTML = '';

    // Добавление элементов в список
    data.forEach(function (row) {
        const listItem = document.createElement('a');
        listItem.href = row.link;  // Заменено на ссылку из данных
        listItem.target = '_blank';
        listItem.classList.add('list-group-item', 'list-group-item-action', 'd-flex', 'justify-content-between', 'align-items-center');

        const titleSpan = document.createElement('span');
        titleSpan.classList.add('mp-title');
        titleSpan.textContent = row.title;

        const badgeSpan = document.createElement('span');
        badgeSpan.classList.add('badge');  // Заменено на цвет из данных
                // Установка цвета в зависимости от статуса
        switch (row.status) {
            case 'Успешно':
                badgeSpan.classList.add('bg-success');
                break;
            case 'Повторная проверка':
                badgeSpan.classList.add('bg-warning');
                break;
            case 'Ожидание партнера':
                badgeSpan.classList.add('bg-dark');
                break;
            case 'В процессе':
                badgeSpan.classList.add('bg-primary');
                break;
            case 'Ручная проверка':
                badgeSpan.classList.add('bg-danger');
                break;
            case 'Автопроверка':
                badgeSpan.classList.add('bg-secondary');
                break;
            case 'Новый':
                badgeSpan.classList.add('bg-info');
                break;
            default:
                // Дефолтный цвет или обработка других статусов по вашему усмотрению
                badgeSpan.classList.add('bg-secondary');
                break;
        }

        badgeSpan.textContent = row.status;

        const externalLinkIcon = document.createElement('i');
        externalLinkIcon.classList.add('bx', 'bx-link-external');

        listItem.appendChild(titleSpan);
        listItem.appendChild(badgeSpan);
        listItem.appendChild(externalLinkIcon);

        list.appendChild(listItem);
    });
}






var socket = io({ transports: ['websocket'] });

    socket.on('task_completed', function (data) {
        console.log('Task completed:', data);
        resultContainer.innerHTML = data.data;
    });

    socket.on('processing', function (data) {
        percentContainer.innerHTML = data;
    });

    socket.on('update_table', function (data) {
            const newData = data.data;
            generateList(newData);
        });

    socket.on('update_moderation_table', function (data) {
            const newData = data.data;
            generateListModeration(newData);
        });


});

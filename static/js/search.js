function search(searchvalue) {
    var resultContainer = document.getElementById('result');

    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    return fetch('/search?text=' + encodeURIComponent(searchvalue), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    .then(response => {
        if (!response.ok) {
            throw new Error('Произошла ошибка. Статус: ' + response.status);
        }
        return response.json();
    })

    .then(data => {
        let table = document.getElementById('result');

        // Очистка содержимого таблицы
        while (table.firstChild) {
            table.removeChild(table.firstChild);
        }

        // Заполнение таблицы данными
        data.data.forEach(item => {
            let row = table.insertRow();
            let keyCell = row.insertCell();
            let descriptionCell = row.insertCell();
            let statusCell = row.insertCell();
            keyCell.innerHTML = item.key;  // Используйте innerHTML вместо textContent
            descriptionCell.innerHTML = item.summary;  // Используйте innerHTML вместо textContent
            statusCell.innerHTML = item.status;  // Используйте innerHTML вместо textContent

        });

        createStatusFilter(data.statuses);

        // Выводим значение count на страницу
        document.getElementById('count').innerHTML = data.count;
    })
    .catch(error => {
        // Очищаем контейнер от предыдущих данных
        resultContainer.innerHTML = '';

        // Вставляем сообщение об ошибке
        resultContainer.innerHTML = 'Произошла ошибка: ' + error.message;
    });
}


var searchvalue = sessionStorage.getItem('searchvalue');
const srcAW = document.getElementById("floatingInput");
if (searchvalue) {
    srcAW.value = searchvalue;
    search(searchvalue);

} else {
    // Если searchvalue не определено, выполняем другие действия (например, отображаем пустую таблицу)
}



function createStatusFilter(statuses) {
    let statusFiltersContainer = document.getElementById('statusFilters');

    // Очистка содержимого контейнера фильтров
    statusFiltersContainer.innerHTML = '';

    // Создание чекбоксов и меток для каждого статуса
    statuses.forEach((status, index) => {
        let formCheck = document.createElement('div');
        formCheck.classList.add('col-md-3', 'col-sm-12', 'form-check', 'form-switch', 'mb-2');

        let checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'status';
        checkbox.classList.add('form-check-input');
        checkbox.value = status;
        checkbox.id = 'flexSwitch' + index;
        checkbox.checked = true; // Установите значение true или false, в зависимости от вашего выбора.
        checkbox.addEventListener('change', applyFilters);

        let label = document.createElement('label');
        label.classList.add('form-check-label');
        label.setAttribute('for', 'flexSwitch' + index);
        label.textContent = status;

        formCheck.appendChild(checkbox);
        formCheck.appendChild(label);

        statusFiltersContainer.appendChild(formCheck);
    });
}



function applyFilters() {
    let table = document.getElementById('result');
    let countContainer = document.getElementById('count');

    let statusFilter = []; // Array to store selected status values
    // Get the selected status checkboxes and populate the statusFilter array
    let checkboxes = document.querySelectorAll('input[name="status"]:checked');
    checkboxes.forEach(checkbox => {
        statusFilter.push(checkbox.value);
    });

    let filteredCount = 0;

    // Iterate over table rows and apply filters
    for (let i = 0; i < table.rows.length; i++) {
        let row = table.rows[i];
        let statusCell = row.cells[2];
        let statusValue = statusCell.innerHTML.trim();

        // Check if the row matches the filter
        if (statusFilter.includes(statusValue)) {
            row.style.display = 'table-row';
            filteredCount++;
        } else {
            row.style.display = 'none';
        }
    }

    // Display the count of filtered rows
    countContainer.textContent = filteredCount;
}

// Добавьте обработчик события изменения состояния чекбоксов
document.querySelectorAll('#statusFilters input[name="status"]').forEach(checkbox => {
    checkbox.addEventListener('change', applyFilters);
});



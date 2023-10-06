
// Функции действий
function getdata() {

    const tableWrap = document.querySelector('.resultTable');
    tableWrap.classList.remove('slide-in');
    tableWrap.style.display = 'none';
    tableWrap.style.display = 'block';
    tableWrap.classList.add('slide-in');

    var cardlink = document.getElementById('cardlink').value;
    var resultContainer = document.getElementById('result');

    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    return fetch('/superloyal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'cardlink': cardlink
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Произошла ошибка. Статус: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        // Очищаем контейнер от предыдущих данных
        resultContainer.innerHTML = '';
        tableWrap.classList.remove('slide-in');
        tableWrap.classList.add('slide-in');


        var table1Data = data["table1"];
        var table2Data = data["table2"];
        var table3Data = data["table3"];
        var table4Data = data["table4"];

        console.log(table4Data);

        // Формирование HTML-кода для таблицы 1
        var table1HTML = '<table class="table table-sm mt-4 mb-4">';
        table1Data.forEach(function(item) {
            table1HTML += '<tr><td>' + item.name + '</td><td>' + item.data + '</td></tr>';
        });
        table1HTML += '</table>';

        // Формирование HTML-кода для таблицы 2
        table2HTML = "";
        if (table2Data && table2Data.length > 0) {
        var table2HTML = '<table class="table table-sm mt-4 mb-4">';
        table2HTML += '<tr><th>#</th><th>Акция</th><th>Тип</th><th>Накоплено</th><th>Значение</th></tr>';
        table2Data.forEach(function(item) {
            table2HTML += '<tr><td>' + item.number + '</td><td>' + item.name + '</td><td>' + item.type + '</td><td>' + item.collect + '</td><td>' + item.amount + '</td></tr>';
        });
        table2HTML += '</table>';
                  // Выводим таблицу 2
          console.log(table2HTML);
        }

        // Формирование HTML-кода для таблицы 3
        table3HTML = "";
        if (table3Data && table3Data.length > 0) {
        var table3HTML = '<table class="table table-sm mt-4 mb-4">';
        table3HTML += '<tr><th>#</th><th>Дата создания транзакции</th><th>Тип</th><th>Акция</th><th>Сумма</th><th>Номер визита</th><th>Номер записи</th><th>Дата визита</th></tr>';
        table3Data.forEach(function(item) {
            table3HTML += '<tr><td>' + item.transaction_id + '</td><td>' + item.create_date + '</td><td>' + item.type + '</td><td>' + item.actions + '</td><td>' + item.amount + '</td><td>' + item.visit_id + '</td><td>' + item.record_id + '</td><td>' + item.date + '</td></tr>';
        });
        table3HTML += '</table>';}

        // Формирование HTML-кода для таблицы 4
        table4HTML = "";
        if (table4Data && table4Data.length > 0) {
        var table4HTML = '<table class="table table-sm mt-4 mb-4">';
        table4HTML += '<tr><th>Пользователь</th><th>Дата начала</th><th>Дата окончания</th></tr>';
        table4Data.forEach(function(item) {
            table4HTML += '<tr><td>' + item.user + '</td><td>' + item.datefrom + '</td><td>' + item.dateto + '</td></tr>';
        });
        table4HTML += '</table>';}

        // Вставка HTML-кода таблиц в контейнер
        resultContainer.innerHTML = table1HTML + table2HTML + table3HTML + table4HTML;
    })
    .catch(error => {
        // Очищаем контейнер от предыдущих данных
        resultContainer.innerHTML = '';

        // Вставляем сообщение об ошибке
        resultContainer.innerHTML = 'Произошла ошибка: ' + error.message;
    });
}


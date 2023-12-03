function displayErrorMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.text(message);
    errorMessage.removeClass('alert-success').addClass('alert-danger').slideDown();
    setTimeout(function() {
        errorMessage.slideUp();
    }, 15000);
}

function displaySuccessMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.text(message);
    errorMessage.removeClass('alert-danger').addClass('alert-success').slideDown();
    setTimeout(function() {
        errorMessage.slideUp();
    }, 15000);
}

function getRecords() {
    var date = document.getElementById('date').value;
    var salonid = document.getElementById('salon').value;
    var resultContainer = document.getElementById('result');

    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    // Отправить запрос на сервер с выбранной датой
    $.ajax({
        url: '/daydetails',
        type: 'POST',
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            'date': date,
            'salon': salonid
        }),
        success: function(response) {
            // Отобразить полученные данные в таблице
            displayRecords(response["dataset"]);
        },
        error: function(error) {
            resultContainer.innerHTML = 'Произошла ошибка. Подробности в консоле'
            console.log(error);
        }
    });
}

function displayRecords(records) {
    var table = $('<table class="table table-striped programs table-responsive">');
    var thead = $('<thead>').append('<tr><th>Сотрудник</th><th>Услуга</th><th>Клиент</th><th>Дата визита</th><th>Статус визита</th><th>Статус оплаты</th><th>Статус печати чека</th></tr>');
    table.append(thead);

    var tbody = $('<tbody>');

    for (var i = 0; i < records.length; i++) {
        var record = records[i];
        var row = $('<tr>');
        row.append('<td>' + record.staff_name + '</td>');

        var services = [];
        for (var j = 0; j < record.services.length; j++) {
            services.push(record.services[j].title);
        }
        row.append('<td>' + services.join(", ") + '</td>');

        row.append('<td>' + record.client.name + '<br>' + record.client.phone + '</td>');
        row.append('<td>' + record.date + '</td>');
        row.append('<td>' + record.attendance + '</td>');
        row.append('<td class="' + getStatusClass(record.paid) + '">' + record.paid + '</td>');
        row.append('<td>' + record.bills + '</td>');

        // Создание кнопки "More" и скрытого блока с дополнительными полями
        var moreButton = $('<button class="btn morebutton">').text('More');
        var moreBlock = $('<div>').addClass('more-block').hide();

        // Обработчик события нажатия кнопки "More"
        moreButton.on('click', createMoreButtonClickHandler(record.more, moreBlock));

        // Добавление кнопки "More" в ячейку
        var moreCell = $('<td>').append(moreButton);
        row.append(moreCell);

        tbody.append(row);
        tbody.append($('<tr>').append($('<td>').attr('colspan', '7').append(moreBlock)));
    }

    function getStatusClass(status) {
        var classList = '';
        if (status.toLowerCase() === 'оплачена') {
            classList = 'status-paid';
        } else if (status.toLowerCase() === 'не оплачена') {
            classList = 'status-unpaid';
        } else if (status.toLowerCase() === 'переплата') {
            classList = 'status-overpaid';
        }
        return classList;
    }

    function createMoreButtonClickHandler(moreData, moreBlock) {
        return function() {
            moreBlock.empty();
            for (var i = 0; i < moreData.length; i++) {
                var data = moreData[i];
                var documents = data.documents;

                var documentsList = $('<ul>');
                for (var j = 0; j < documents.length; j++) {
                    var document = documents[j];
                    var listItem = $('<li>').text('Document ID: ' + document.id + ', Number: ' + document.number + ', Title: ' + document.title + ', Type: ' + document.type);
                    documentsList.append(listItem);
                }
                var document = $('<p>').text('Document ID: ' + documents[0].id);
                var recordId = $('<p>').text('Record ID: ' + data.record_id);
                var visitId = $('<p>').text('Visit ID: ' + data.visit_id);

                moreBlock.append(document);
                moreBlock.append(recordId);
                moreBlock.append(visitId);
                moreBlock.append($('<p>').text('Documents:').append(documentsList));
            }
            moreBlock.slideToggle();
        };
    }

    table.append(tbody);

    $('#result').empty().append(table);
}




$(function() {

  rome(date, {

	  monthsInCalendar: 3,
	  time: false,
      weekStart: 1,
      inputFormat: 'DD-MM-YYYY'
	});


});
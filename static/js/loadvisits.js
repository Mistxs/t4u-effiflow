document.getElementById('upload-form').addEventListener('submit', function(event) {
            event.preventDefault();

            var formData = new FormData(this);
            const tableWrap = document.querySelector('.resultTable');
            tableWrap.classList.remove('slide-in');

            fetch('/visits/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                var resultDiv = document.getElementById('result');
                var visit = data.data
//                resultDiv.innerHTML = '<h2>Результат:</h2><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                drawTable(visit)
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        });



function drawTable(visits) {
    const tableWrap = document.querySelector('.resultTable');

    tableWrap.style.display = 'block';
    tableWrap.classList.add('slide-in');

    var table = $('<table class="table">');
    var tbody = $('<tbody>');

    if (visits.length > 0) {
        var selectValue = '<option value="0">---</option><option value="date">Дата (обязательно)</option><option value="masterId">ID сотрудника (необязательно)</option><option value="masterName">Имя сотрудника (необязательно)</option><option value="length">Длительность (необязательно)</option><option value="serviceId">ID услуг (через ##) (необязательно)</option><option value="serviceTitle">Названия услуг (через ##) (необязательно)</option><option value="servicePrice">Цены услуг (через ##) (необязательно)</option><option value="serviceDiscount">Скидки на услуги (через ##) (необязательно)</option><option value="comment">Комментарий (необязательно)</option><option value="clientPhone">Номер телефона клиента (необязательно)</option><option value="clientName">Имя клиента (необязательно)</option><option value="attendance">Статус записи (число) (необязательно)</option><option value="attendanceTitle">Статус записи (строка) (необязательно)</option><option value="accountId">ID кассы (необязательно)</option><option value="paidAmount">Оплачено (необязательно)</option>';
        var thead = $('<thead>');
        var headerRow = $('<tr>');
        var columnCounter = 0;
        for (var key in visits[0]) {
            var thElement = $('<th>').html('<select class="form-select" name="column_' + columnCounter + '">' + selectValue + '</select>');
            headerRow.append(thElement);
            columnCounter = columnCounter + 1;
        }
        thead.append(headerRow);
        table.append(thead);
    }


    for (var i = 0; i < visits.length; i++) {
        var row = $('<tr>');
        for (var key in visits[i]) {
            row.append($('<td>').text(visits[i][key]));
        }
        tbody.append(row);
    }

    table.append(tbody);

    $('#result').empty().append(table);
}
function findoverpayed() {
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
                start_date: document.getElementById("start_date").value,
                end_date: document.getElementById("end_date").value,
                salon_id: document.getElementById("branch_number").value
            };

    return fetch('/findoverpayed', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'dataset': formData
        })
    })
    .then(function(response) {
                // Обработка ответа от сервера
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Ошибка при выполнении запроса");
                }
            })
    .then(data => {
            // Очищаем контейнер от предыдущих данных
            resultContainer.innerHTML = '';

            var table1Data = data["success"];
            var table2Data = data["dataset"];

            // Создаем разметку таблицы
            var tableHTML = '<table class="table table-sm mt-4 mb-4">';
            tableHTML += '<thead><tr><th>ID операции</th><th>Дата операции</th><th>Сумма</th><th>Запись</th></tr></thead>';
            tableHTML += '<tbody>';

            // Заполняем таблицу значениями из dataset
            for (var i = 0; i < table2Data.length; i++) {
                var row = table2Data[i];
                tableHTML += '<tr>';
                tableHTML += '<td>' + row.id + '</td>';
                tableHTML += '<td>' + row.date + '</td>';
                tableHTML += '<td>' + row.amount + '</td>';
                tableHTML += '<td>' + row.record_id + '</td>';
                tableHTML += '</tr>';
            }

            tableHTML += '</tbody></table>';

            // Вставляем HTML-код таблицы в контейнер
            resultContainer.innerHTML = tableHTML;
    })
}





$(function() {

  rome(start_date, {

	  monthsInCalendar: 3,
	  time: false,
      weekStart: 1,
      inputFormat: 'DD-MM-YYYY'
	});

	rome(end_date, {

	  monthsInCalendar: 3,
	  time: false,
      weekStart: 1,
      inputFormat: 'DD-MM-YYYY'
	});


});
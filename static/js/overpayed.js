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

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var dataset = data.dataset
            resultContainer.innerHTML = "";
            drawTable(dataset)
        } else if (data.status === 'error') {
            resultContainer.innerHTML = "";
            displayErrorMessage(data.text);
        }
    })
}



function drawTable(operations) {

const tableWrap = document.querySelector('.resultTable');

tableWrap.style.display = 'block';
tableWrap.classList.add('slide-in');

var table = $('<table class="table table-sm mt-4 mb-4">');
var tbody = $('<tbody>');

var table = '<table class="table table-sm mt-4 mb-4">';
table += '<thead><tr><th>ID операции</th><th>Дата операции</th><th>Сумма</th><th>Запись</th><th>Расхождение</th></tr></thead>';
operations.forEach(function(item) {
            table += '<tr><td>' + item.id + '</td><td>' + item.date + '</td><td>' + item.amount + '</td><td>' + item.record_id + '</td><td>' + item.overpay + '</td></tr>';
        });
table += '</table>';

$('#result').empty().append(table);

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
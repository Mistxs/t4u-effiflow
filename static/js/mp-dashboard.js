document.addEventListener('DOMContentLoaded', () => {


  const listItem = document.querySelectorAll('.chat-list');

  listItem.forEach((item) => {
    const star = document.createElement('span');
    star.classList.add('star', 'fa-solid', 'fa-star-o');
    item.appendChild(star);
  });


  const stars = document.querySelectorAll('.star');

  stars.forEach((star) => {
    star.addEventListener('click', () => {
      star.classList.toggle('fa-star');
      star.classList.toggle('fa-star-o');
    });
  });


    var modal = document.getElementById('extModal');
    var modalTitle = modal.querySelector('.modal-title');
    var modalBody = modal.querySelector('.modal-body');

    var spanElements = document.querySelectorAll('span[data-bs-toggle="modal"][data-bs-target="#extModal"]');
    spanElements.forEach(function(spanElement) {
        spanElement.addEventListener('click', function() {
            var listItem = this.closest('li');
            var mpId = listItem.getAttribute('data-mp-id');
            var title = listItem.querySelector('.chat-title').textContent;

            modalTitle.textContent = title;
            modalBody.textContent = mpId;
        });
    });


});




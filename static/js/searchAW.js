  const input = document.getElementById("floatingInput");
  const clearButton = document.getElementById("clearInput");
  const searchButton = document.getElementById("srchButton");

  clearButton.style.opacity = 0;
  clearButton.style.visibility = "hidden";
  searchButton.style.opacity = 0;
  searchButton.style.visibility = "hidden";

  input.addEventListener("input", function() {
    if (input.value.length > 0) {
      clearButton.style.opacity = 1;
      clearButton.style.visibility = "visible";
      searchButton.style.opacity = 1;
      searchButton.style.visibility = "visible";
    } else {
      clearButton.style.opacity = 0;
      clearButton.style.visibility = "hidden";
      searchButton.style.opacity = 0;
      searchButton.style.visibility = "hidden";
    }
  });

  clearButton.addEventListener("click", function() {
    input.value = "";
    sessionStorage.setItem('searchvalue', "");
    clearButton.style.opacity = 0;
    clearButton.style.visibility = "hidden";
    searchButton.style.opacity = 0;
    searchButton.style.visibility = "hidden";
  });


document.getElementById('floatingInput').addEventListener('keydown', function(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    searchAW()
  }
});

document.getElementById("srchButton").addEventListener("click", function() {
    searchAW()
});

function searchAW() {
    var searchvalue = document.getElementById('floatingInput').value;
    console.log(searchvalue);

    // Сохраняем значение в sessionStorage (или localStorage, если нужно сохранить его между сессиями)
    sessionStorage.setItem('searchvalue', searchvalue);

    // Переходим на страницу /2ndline/search
    window.location.href = '/2ndline/search';
}
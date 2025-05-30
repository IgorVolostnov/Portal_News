// Открытие и закрытие верхней зоны навигации
function openNav() {
const myNav = document.getElementById("myNav")
const screenHeight = window.screen.height;
let size = myNav.scrollHeight;
let sizePercent = String((size + (size * 0,70)) * 100 / screenHeight) + "%";
myNav.style.height = sizePercent;
this.style = "display: none;";
myNav.onmouseleave = function() {
 myNav.style.height = "0%";
 };
 }

function closeNav() {
const myNav = document.getElementById("myNav")
myNav.style.height = "0%";
 }
// Открытие и закрытие фильтров
function openFilter() {
const myFilter = document.getElementById("myFilter")
const myFilterButton = document.getElementById("myFilterButton")
myFilter.style.width = "30%";
myFilterButton.style.width = "30%";
this.style = "display: none;";
myFilter.onmouseleave = function() {
 myFilter.style.width = "0%";
 myFilterButton.style.width = "0%";
 };
}

function closeFilter() {
const myFilter = document.getElementById("myFilter")
const myFilterButton = document.getElementById("myFilterButton")
myFilter.style.width = "0%";
myFilterButton.style.width = "0%";
 }

 if( $(document).height() <= $(window).height() ){
  $(".page-footer").addClass("fixed-bottom");
}

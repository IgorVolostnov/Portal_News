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


// Карусель для картинок в постах
window.addEventListener('load', setUpSliders);


function setUpSliders() {
    var prevBtns = document.getElementsByClassName('prev-button');
    var nextBtns = document.getElementsByClassName('next-button');

    for (var i = 0; i < prevBtns.length; i++)
        prevBtns[i].addEventListener('click', function(e) {slide(e, 'prev')});

    for (var i = 0; i < nextBtns.length; i++)
        nextBtns[i].addEventListener('click', function(e) {slide(e, 'next')});
};


function qselectorall() {
    var x = document.querySelectorAll("video");
    for (var i = 0; i < x.length; i++) {
        x[i].pause();
        }
    }


function slide(e, to) {
    var sliderId = e.target.getAttribute('data-target');
    var sliderInner = document.querySelector('#' + sliderId + ' .slider-inner');
    var activeSlide = sliderInner.querySelector('.active');

    var toSlide;

    if (to === 'prev') {
        toSlide = activeSlide.previousElementSibling;
        if (!toSlide)
            toSlide = activeSlide.parentElement.lastElementChild;
    } else {
        toSlide = activeSlide.nextElementSibling;
        if (!toSlide)
            toSlide = activeSlide.parentElement.firstElementChild;
    }

    activeSlide.classList.remove('active');
    qselectorall();
    toSlide.classList.add('active');
};


// Прибиваем Footer к низу
document.addEventListener("DOMContentLoaded", function () {
    const myWrapper = document.getElementById('wrapper')
    var myFooter = document.getElementById('footer')
    if (myWrapper) {
        const wrapperHeight = document.getElementById("wrapper").offsetHeight;
        const windowHeight = window.innerHeight;
        if (wrapperHeight <= windowHeight) {
            myFooter.addClass("fixed-bottom");
        }
    }
})
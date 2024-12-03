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
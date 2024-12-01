function openNav() {
const myNav = document.getElementById("myNav")
myNav.style.height = "70%";
this.style = "display: none;";
myNav.onmouseleave = function() {
 myNav.style.height = "0%";
 };
 }

function closeNav() {
const myNav = document.getElementById("myNav")
myNav.style.height = "0%";
 }
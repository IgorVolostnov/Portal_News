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

function openFilter() {
const myFilter = document.getElementById("myFilter")
const buttonFilter = document.getElementById("buttonFilter")
myFilter.style.width = "30%";
buttonFilter.style = "display: grid;";
this.style = "display: none;";
myFilter.onmouseleave = function() {
 myFilter.style.width = "0%";
 buttonFilter.style = "display: none;";
 };
 }

function closeFilter() {
const myFilter = document.getElementById("myFilter")
const buttonFilter = document.getElementById("buttonFilter")
myFilter.style.width = "0%";
buttonFilter.style = "display: none;";
 }

function myFunctionHide() {
const buttonFilter = document.getElementById("buttonFilter")
buttonFilter.style = "display: none;";
 }

 if( $(document).height() <= $(window).height() ){
  $(".page-footer").addClass("fixed-bottom");
}
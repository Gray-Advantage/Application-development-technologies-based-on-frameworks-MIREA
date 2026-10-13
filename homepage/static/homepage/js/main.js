// Текущий год в подвале страницы подставляется на стороне браузера.
const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

const hamburger = document.getElementById("hamburger");
const sidebar = document.getElementById("sidebar");

hamburger.addEventListener("click", () => {
    sidebar.classList.toggle("open");

    // Toggle icon
    if (sidebar.classList.contains("open")) {
        hamburger.innerHTML = "&times;"; // ✖
    } else {
        hamburger.innerHTML = "&#9776;"; // ☰
    }
});
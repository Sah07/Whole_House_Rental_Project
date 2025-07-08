const menuBtn = document.querySelector('.menu-btn');
const navBar = document.querySelector('.nav-bar');
menuBtn.addEventListener('click', () => {
    navBar.classList.toggle('show');

    const isVisible = navBar.style.display === "flex";

    // Toggle menu visibility
    navBar.style.display = isVisible ? "none" : "flex";

    // Toggle arrow
    menuBtn.textContent = isVisible ? "Menu ▼" : "Menu ▲";
});
window.addEventListener("resize", () => {
    if (window.innerWidth > 600) {
        navBar.style.display = "flex";
        menuBtn.textContent = "Menu ▼"; // Reset arrow
    } else {
        navBar.style.display = "none"; // keep mobile clean
    }
});
document.addEventListener('DOMContentLoaded', () => {
    navBarToggle();
});

function navBarToggle() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.querySelector('.main-nav');

    if (!navToggle || !navMenu) return;

    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('open');
    });

    navMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => navMenu.classList.remove('open'));
    });
}
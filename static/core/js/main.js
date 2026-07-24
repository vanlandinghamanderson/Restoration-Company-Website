document.addEventListener('DOMContentLoaded', () => {
    heroCarousel();
    navBarToggle();
});

function heroCarousel() {
    const slides = Array.from(document.querySelectorAll('.hero-video-slide'));

    if (slides.length <= 1) return;

    const interval = 6000; // 6 seconds
    let currentSlide = 0;
    let timer = null;

    function goToSlide(index) {
        if (!slides.length) return;

        const previousSlide = slides[currentSlide];
        if (previousSlide) {
            previousSlide.classList.remove('active');
        }

        currentSlide = (index + slides.length) % slides.length;

        const nextSlide = slides[currentSlide];
        if (nextSlide) {
            nextSlide.classList.add('active');
        }

        if (nextSlide && nextSlide.tagName === 'VIDEO') {
            nextSlide.currentTime = 0;
            nextSlide.play().catch(() => {});
        }
    }

    function next() {
            goToSlide(currentSlide + 1);
    }
    
    function startAutoPlay() {
        clearInterval(timer);
        timer = setInterval(next, interval);
    }

    startAutoPlay();
}

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
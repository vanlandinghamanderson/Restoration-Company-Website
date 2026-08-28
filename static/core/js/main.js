document.addEventListener('DOMContentLoaded', () => {
    heroCarousel();
    navBarToggle();
    galleryFilter();
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

function galleryFilter() {
    
    /* Finds the navigation bar on the gallery page */
    const bar = document.querySelector(".filter-bar");
    /* Finds the items from the gallery */
    const items = Array.from(document.querySelectorAll(".gallery-item"));

    /* Bails out if the page has no pictures */
    if (!bar || !items.length ) return;

    /* Read the filter from the URL */
    function currentSlug() {
        return new URLSearchParams(window.location.search).get("service") || "all";
    }

    /* The function does the actual work */
    function applyFilter(slug) {

        /* Shows or hide each item */
        items.forEach(function (item) {
            item.hidden = slug !== "all" && item.dataset.service !== slug;
        });

        /* Update the button states */
        bar.querySelectorAll(".filter-button").forEach(function (btn) {
            const on = btn.dataset.service === slug;
            btn.classList.toggle("active", on);
            btn.setAttribute("aria-current", String(on));
        });
    }

    /* Listen for clicks on the navigation */
    bar.addEventListener("click", function(e) {

        /* Figures out which button was clicked */
        const btn = e.target.closet(".filter-button");
        if (!btn) return;

        /* Respect modifier clicks */
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;

        /* Stops the navigation */
        e.preventDefault();

        /* Apply the fiter */
        const slug = btn.dataset.service;
        applyFilter(slug);

        /* Build the new URL */
        const url = slug === "all"
            ? window.location.pathname
            : window.location.pathname + "?service=" + encodeURIComponent(slug);
        
        /* Update the address bar */
        history.pushState({ service : slug}, "", url);
    });

    /* Handle back and forward */
    window.addEventListener("popstate", function () {
        applyFilter(currentSlug());
    });

    /* Run once on load */
    applyFilter(currentSlug());

}
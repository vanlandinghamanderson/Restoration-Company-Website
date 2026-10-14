document.addEventListener('DOMContentLoaded', () => {
    heroCarousel();
    navBarToggle();
    galleryFilter();
    initContactForm();
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

function initContactForm() {
    const form = document.getElementById('contact-app');

    if (!form || !window.CONTACT_API_URL) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    const successAlert = form.querySelector('[data-contact-success]');
    const errorAlert = form.querySelector('[data-contact-error]');
    const fields = form.querySelector('[data-contact-fields]');

    if (successAlert) successAlert.hidden = true;
    if (errorAlert) {
        errorAlert.hidden = true;
        errorAlert.textContent = '';
    }

    form.querySelectorAll('[data-field-errors]').forEach((el) => {
        el.hidden = true;
        el.innerHTML = '';
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (!submitBtn) return;
        submitBtn.disabled = true;

        if (errorAlert) {
            errorAlert.hidden = true;
            errorAlert.textContent = '';
        }

        try {
            const response = await fetch(window.CONTACT_API_URL, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value,
                },
            });

            const data = await response.json();

            if (response.ok && data.ok) {
                if (successAlert) successAlert.hidden = false;
                if (fields) fields.hidden = true;
                form.reset();
                return;
            }

            const errors = data.errors || {};
            Object.keys(errors).forEach((name) => {
                if (name === '__all__') {
                    if (errorAlert) {
                        errorAlert.textContent = errors.__all__[0];
                        errorAlert.hidden = false;
                    }
                    return;
                }

                const list = form.querySelector(`[data-field-errors="${name}"]`);
                if (list) {
                    list.innerHTML = errors[name].map((msg) => `<li>${msg}</li>`).join('');
                    list.hidden = false;
                }
            });
        } catch (err) {
            if (errorAlert) {
                errorAlert.textContent = 'Something went wrong. Please try again or call us directly.';
                errorAlert.hidden = false;
            }
        } finally {
            submitBtn.disabled = false;
        }
    });
}
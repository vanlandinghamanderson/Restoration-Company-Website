document.addEventListener('DOMContentLoaded', () => {
    navigation();
    heroCarousel();
    galleryFilter();
    initContactForm();
});

function navigation() {
    /**
     * Retrieves the elements for the navigation
     */
    const nav = document.getElementById('mainNav');
    const navToggle = document.getElementById('navToggle');
    const serviceDropdowns = document.querySelectorAll('.site-header__service-dropdown');

    /**
     * Helper Function
     */

    function isMobile() {
        return window.matchMedia('(hover: none), (max-width: 938px)').matches;
    }

    function closeDropdowns() {
        serviceDropdowns.forEach(function (dropdown) {
            dropdown.classList.remove('open');
            dropdown.querySelector('.nav-link').setAttribute('aria-expanded', 'false');
        });
    }

    function closeNav() {
        nav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        closeDropdowns();
    }

    /**
     * Hamburger: Show/Hide the Whole Menu
     */
    navToggle.addEventListener('click', function() {
        const isOpen = nav.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', String(isOpen));
        if (!isOpen) closeDropdowns();
    });

    /**
     * Services: First tap ones, Second tap goes to the page
     */
    serviceDropdowns.forEach(function (dropdown) {
        const link = dropdown.querySelector('.nav-link');
        link.setAttribute('aria-haspopup', 'true');
        link.setAttribute('aria-expanded', 'false');

        link.addEventListener('click', function (event) {
            if (!isMobile()) return;

            if (!dropdown.classList.contains('open')) {
                event.preventDefault();
                closeDropdowns();
                dropdown.classList.add('open');
                link.setAttribute('aria-expanded', 'true');
            }
        });
    });

    /**
     * Taps outside of the header closes everything
     */
    document.addEventListener('click', function(event) {
        if (!event.target.closet('.site-header')) {
            closeNav();
        }
    });

    /**
     * Escape Key closes everything
     */
    document.addEventListener('keydown', function (event) {
        if (event.key !== 'Escape') return;

        if (nav.classList.contains('open')) {
            closeNav();
            navToggle.focus();
        } else {
            closeDropdowns();
            if (document.activeElement) document.activeElement.blur();
        }
    });

    /**
     * Reset when resized back to desktop
     */
    window.addEventListener('resize', function () {
        if (!window.matchMedia('(max-width: 1050px').matches) {
            closeNav();
        }
    });
}

function heroCarousel() {

    // Retrieves the slides by its ID
    const slides = document.querySelectorAll('#heroCarousel .hero__carousel-slide');

    // Checks to see if the length is 0, then it retunrs
    if (slides.length === 0) return;

    /**
     * 
     */
    const IMAGE_TIME = 6000;
    let current = 0;
    let timer = null;

    function showSlide(index) {

        // Hides the old slide and stops it video
        slides[current].classList.remove('active');
        const oldVideo = slides[current].querySelector('video');
        if (oldVideo) {
            oldVideo.pause();
            oldVideo.onended = null;
        }

        // Shows the next slide
        current = index;
        const slide = slides[current];
        slide.classList.add('active');

        clearTimeout(timer);

        const video = slide.querySelector('video');

        if (video) {
            // VIDEO: play it, go the next slide when it end
            video.loop = slides.length === 1; // loop only if it is the only slide
            video.currentTime = 0;
            video.play().catch(() => {
                // If the browser blocks playback, falls back to timing stage
                timer = setTimeout(nextSlide, IMAGE_TIME);
            });
            video.onended = nextSlide;
        } else {
            // PICTURE: It waits 6 seconds, then goes to the next picture
            if (slides.length > 1) {
                timer = setTimeout(nextSlide, IMAGE_TIME);
            }
        }
    }

    function nextSlide() {
        showSlide((current + 1) % slides.length);
    }

    // Starts with the first slide
    slides[0].classList.remove('active');
    current = 0;
    showSlide(0);
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
        const btn = e.target.closest(".filter-button");
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
/**
 * Initializes the contact form functionality.
 * @returns {void}
 */
function initContactForm() {

    // Retrieve the contact form element by its ID
    const form = document.getElementById('contact-app');
    // If the form doesn't exist or the CONTACT_API_URL is not defined, exit the function
    if (!form || !window.CONTACT_API_URL) return;

    /**
     * successAlert: It retrieves the element that displays a success message after the form is submitted successfully.
     * errorAlert: It retrieves the element that displays an error message if the form submission fails.
     * fields: It retrieves the container that holds the form fields.
     * submitButton: It retrieves the submit button of the form.
     */
    const successAlert = form.querySelector('[data-contact-success]');
    const errorAlert = form.querySelector('[data-contact-error]');
    const fields = form.querySelector('[data-contact-fields]');
    const submitButton = form.querySelector('button[type="submit"]');


    // Add an event listener for the form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // This handles the error messages and resets the form state before validation
        if (errorAlert) { errorAlert.hidden = true; errorAlert.textContent = ''; }
        form.querySelectorAll('[data-field-errors]').forEach(el => {
            el.hidden = true;
            el.innerHTML = '';
        });
        
        /**
         * requiredFields: It collects all the form fields that are marked as required.
         * selectedService: It retrieves the select element for the requested service.
         * selectedServiceOption: It retrieves the currently selected option in the requested service select element.
         * emptyFields: It filters out the required fields that are empty or not filled in by the user.
         */
        const requiredFields = Array.from(form.querySelectorAll('[required]'));
        const selectedService = form.querySelector('[name="requested_service"]');
        const selectedServiceOption = selectedService && selectedService.selectedOptions[0];
        const emptyFields = requiredFields.filter((field) => {
            if (field === selectedService) return !selectedServiceOption || !selectedServiceOption.value;
            return !field.value.trim();
        });

        // If there are empty required fields, display error messages and focus on the first empty field
        if (emptyFields.length) {
            const formFields = Array.from(form.querySelectorAll('input:not([type="hidden"]), select, textarea'));
            const allFieldsBlank = formFields.every(field => !field.value.trim());
            if (allFieldsBlank) {
                if (errorAlert) {
                    errorAlert.textContent = 'Please fill in all fields.';
                    errorAlert.hidden = false;
                }
                emptyFields[0].focus();
                return;
            }

            // Scans through the empty fields and displays error messages for each one
            emptyFields.forEach((field) => {
                const errorList = Array.from(form.querySelectorAll('[data-field-errors]')).find(list =>
                    list.dataset.fieldErrors === field.name);
                if (!errorList) return;

                const label = field.labels && field.labels[0];
                const fieldName = label
                    ? label.textContent.replace('*', '').trim()
                    : field.name;

                const error = document.createElement('li');
                error.textContent = field === selectedService
                    ? `${fieldName} must be selected.`
                    : `${fieldName} is required.`;
                errorList.appendChild(error);
                errorList.hidden = false;
            });
            emptyFields[0].focus();
            return;
        }

        // If the form is not valid according to HTML5 validation, report the validity and exit
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        submitButton.disabled = true;

        /**
         * Attempts to submit the form data to the server using the Fetch API. If the submission is successful, 
         * it displays a success message and hides the form fields. If there are validation errors returned from the server, 
         * it displays those errors next to the corresponding fields. If an unexpected error occurs during submission, 
         * it displays a generic error message.
         */
        try {
            const response = await fetch(window.CONTACT_API_URL, {
                method: 'POST',
                body: new FormData(form)
            });
            const data = await response.json();
            if (data.ok) {
                if (successAlert) successAlert.hidden = false;
                if (fields) fields.hidden = true;
                form.reset();
            } else {
                const errors = data.errors || {};
                Object.entries(errors).forEach(([name]) => {
                    if (name === '__all__') {
                        if (errorAlert) {
                            errorAlert.textContent = errors.__all__[0];
                            errorAlert.hidden = false;
                        }
                        return;
                    }

                    const list = form.querySelector(`[data-field-errors="${name}"]`);
                    if (list) {
                        list.innerHTML = errors[name].map(msg => `<li>${msg}</li>`).join('');
                        list.hidden = false;
                    }
                });
                submitButton.disabled = false;
            }
        } catch (error) {
            if (errorAlert) {
                errorAlert.textContent = 'An unexpected error occurred. Please try again later.';
                errorAlert.hidden = false;
            }
            submitButton.disabled = false;
        }
    });
}
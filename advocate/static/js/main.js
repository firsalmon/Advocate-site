(function() {
    'use strict';

    /* === Mobile Menu === */
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const burgerIcon = document.getElementById('burger-icon');
    const closeIcon = document.getElementById('close-icon');
    const mobileLinks = document.querySelectorAll('.mobile-nav-link');
    let isMenuOpen = false;

    function toggleMenu() {
        if (!menuBtn || !mobileMenu) return;
        isMenuOpen = !isMenuOpen;
        mobileMenu.classList.toggle('hidden', !isMenuOpen);
        burgerIcon.classList.toggle('hidden', isMenuOpen);
        closeIcon.classList.toggle('hidden', !isMenuOpen);
        menuBtn.setAttribute('aria-expanded', isMenuOpen);
        menuBtn.setAttribute('aria-label', isMenuOpen ? 'Закрыть меню' : 'Открыть меню');
        if (isMenuOpen) {
            const firstLink = mobileMenu.querySelector('a, button');
            if (firstLink) firstLink.focus();
        } else {
            menuBtn.focus();
        }
    }

    if (menuBtn) menuBtn.addEventListener('click', (e) => { e.stopPropagation(); toggleMenu(); });
    mobileLinks.forEach(link => link.addEventListener('click', () => { if (isMenuOpen) toggleMenu(); }));
    document.addEventListener('click', (e) => {
        if (isMenuOpen && !mobileMenu.contains(e.target) && e.target !== menuBtn && !menuBtn.contains(e.target)) toggleMenu();
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && isMenuOpen) toggleMenu(); });

    /* === Modal === */
    const modal = document.getElementById('booking-modal');
    const modalClose = document.getElementById('modal-close');
    const overlay = document.getElementById('modal-overlay');
    const triggerBtns = [
        document.getElementById('modal-trigger'),
        document.querySelector('.modal-trigger-mobile'),
        document.querySelector('.modal-trigger-main'),
        document.querySelector('.modal-trigger-footer')
    ].filter(Boolean);
    let previousFocus = null;
    let isModalOpen = false;

    function trapFocus() {
        if (!modal) return;
        const focusable = modal.querySelectorAll('input, textarea, select, button, [href], [tabindex]:not([tabindex="-1"])');
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        modal.addEventListener('keydown', (e) => {
            if (e.key !== 'Tab' || !isModalOpen) return;
            if (e.shiftKey) {
                if (document.activeElement === first) { e.preventDefault(); last.focus(); }
            } else {
                if (document.activeElement === last) { e.preventDefault(); first.focus(); }
            }
        });
    }

    function openModal(triggerElement) {
        if (isModalOpen || !modal) return;
        isModalOpen = true;
        previousFocus = triggerElement || document.activeElement;
        modal.classList.remove('hidden');
        document.body.classList.add('modal-open');
        modal.setAttribute('aria-hidden', 'false');
        const firstInput = modal.querySelector('input, textarea, button[type="submit"]');
        if (firstInput) setTimeout(() => firstInput.focus(), 50);
        trapFocus();
    }

    function closeModal() {
        if (!isModalOpen || !modal) return;
        isModalOpen = false;
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
        modal.setAttribute('aria-hidden', 'true');
        if (previousFocus) { previousFocus.focus(); previousFocus = null; }
    }

    triggerBtns.forEach(btn => btn.addEventListener('click', () => {
        openModal(btn);
        if (isMenuOpen) toggleMenu();
    }));

    if (modalClose) modalClose.addEventListener('click', closeModal);
    if (overlay) overlay.addEventListener('click', (e) => { if (e.target === overlay) closeModal(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && isModalOpen) closeModal(); });

    // Автооткрытие при success или ошибках валидации
    const successState = document.getElementById('success-state');
    const successCloseBtn = document.getElementById('close-success-btn');

    if (successState && !successState.classList.contains('hidden')) {
        openModal();
        if (successCloseBtn) {
            successCloseBtn.addEventListener('click', closeModal);
            setTimeout(closeModal, 4000);
        }
    } else if (modal && !modal.classList.contains('hidden')) {
        openModal();
        const firstInvalid = modal.querySelector('.text-red-500')?.previousElementSibling?.querySelector('input, textarea');
        const target = firstInvalid || modal.querySelector('input, button[type="submit"]');
        if (target) setTimeout(() => target.focus(), 50);
    }

    // Блокировка кнопки при отправке
    const form = document.getElementById('modal-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');

    if (form && submitBtn) {
        form.addEventListener('submit', () => {
            submitBtn.disabled = true;
            if (btnText) btnText.textContent = 'Отправка...';
            if (btnSpinner) btnSpinner.classList.remove('hidden');
        });
    }

    /* === Carousel === */
    const sliderTrack = document.getElementById('slider-track');
    if (sliderTrack) {
        const prevBtn = document.getElementById('slider-prev');
        const nextBtn = document.getElementById('slider-next');
        const dots = document.querySelectorAll('.slider-dot');
        let currentSlide = 0;
        const totalSlides = dots.length;

        function goToSlide(index) {
            if (index < 0) index = totalSlides - 1;
            if (index >= totalSlides) index = 0;
            currentSlide = index;
            const slides = sliderTrack.querySelectorAll('.slider-slide');
            if (slides[currentSlide]) {
                slides[currentSlide].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
            }
            dots.forEach((dot, i) => {
                dot.setAttribute('aria-selected', i === currentSlide ? 'true' : 'false');
                dot.classList.toggle('bg-emerald-500', i === currentSlide);
                dot.classList.toggle('bg-slate-300', i !== currentSlide);
            });
        }

        if (prevBtn) prevBtn.addEventListener('click', () => goToSlide(currentSlide - 1));
        if (nextBtn) nextBtn.addEventListener('click', () => goToSlide(currentSlide + 1));
        dots.forEach(dot => {
            dot.addEventListener('click', () => {
                goToSlide(parseInt(dot.getAttribute('data-index'), 10));
            });
        });
    }
})();
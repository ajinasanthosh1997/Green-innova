/**
 * Green Innova - Main JavaScript
 * Handles Header behavior, Mobile Menu, and Global Animations
 */

document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initMobileMenu();
    initTabs();
    initCalculator();
    initScrollAnimations();
    initHeroCarousel();
    initGlobalFeatures();
});

/**
 * Basic Scroll-triggered Animations
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all sections and cards for entrance animations
    document.querySelectorAll('section, .tab-content, .grid > div').forEach(el => {
        // observer.observe(el); 
    });
}

/**
 * Link Handling & Global Animations
 */
function initGlobalFeatures() {
    // Smooth scroll for all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || !targetId.startsWith('#')) return;
            
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form submission feedback (Global)
    document.querySelectorAll('form').forEach(form => {
        if (form.id === 'enquiry-form' || form.id === 'contact-form') return; 
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Thank you for your message! Our team will contact you soon.');
            form.reset();
        });
    });
}

/**
 * Tab Switching Logic
 */
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-tab');

            // Update buttons
            tabButtons.forEach(b => {
                b.classList.remove('active');
                b.classList.add('text-gray-400');
                b.classList.remove('text-charcoal');
            });
            btn.classList.add('active');
            btn.classList.remove('text-gray-400');
            btn.classList.add('text-charcoal');

            // Update content with fade transition
            tabContents.forEach(content => {
                content.classList.add('hidden');
                content.classList.remove('block', 'animate-fade-in-up');
            });
            const activeContent = document.getElementById(`tab-${target}`);
            if (activeContent) {
                activeContent.classList.remove('hidden');
                activeContent.classList.add('block', 'animate-fade-in-up');
            }
        });
    });
}

/**
 * Solar Savings Calculator Logic & Modal Flow
 */
function initCalculator() {
    const homeCalcCta = document.getElementById('home-calc-cta');
    const homeName = document.getElementById('home-lead-name');
    const homePhone = document.getElementById('home-lead-phone');

    const bizCalcCta = document.getElementById('biz-calc-cta');
    const bizName = document.getElementById('biz-lead-name');
    const bizPhone = document.getElementById('biz-lead-phone');

    const heroGetStarted = document.getElementById('hero-get-started');

    const enquiryModal = document.getElementById('enquiry-modal');
    const closeModal = document.getElementById('close-modal');

    // New Step Containers
    const modalStepLocation = document.getElementById('modal-step-location');
    const modalStepType = document.getElementById('modal-step-type');
    const modalStepResSubsidy = document.getElementById('modal-step-res-subsidy');
    const modalStepSelection = document.getElementById('modal-step-selection');
    const modalStepData = document.getElementById('modal-step-data');
    const modalStepSuccess = document.getElementById('modal-step-success');

    // Inputs & Buttons
    const modalLocationInput = document.getElementById('modal-location-input');
    const nextToTypeBtn = document.getElementById('next-to-type');
    const typeBtns = document.querySelectorAll('.type-btn');
    const subsidyBtns = document.querySelectorAll('.subsidy-btn');
    const comOptBtns = document.querySelectorAll('.com-opt-btn');
    const modalDataInput = document.getElementById('modal-data-input');
    const submitDataBtn = document.getElementById('submit-data');

    let currentEnquiryData = {
        name: '',
        phone: '',
        place: '',
        type: '',
        subsidy: 'false',
        commercialOption: '',
        units: '',
        bill: ''
    };

    function resetModalSteps() {
        // Reset Internal Data
        currentEnquiryData = {
            name: currentEnquiryData.name || '',
            phone: currentEnquiryData.phone || '',
            place: '',
            type: '',
            subsidy: 'false',
            commercialOption: '',
            units: '',
            bill: ''
        };

        // Reset DOM Inputs
        if (modalLocationInput) modalLocationInput.value = '';
        if (modalDataInput) {
            modalDataInput.value = '';
            modalDataInput.placeholder = 'Enter value';
        }

        // Reset Buttons
        if (nextToTypeBtn) {
            nextToTypeBtn.classList.remove('bg-primary');
            nextToTypeBtn.classList.add('bg-gray-400');
        }
        if (submitDataBtn) {
            submitDataBtn.classList.remove('bg-primary');
            submitDataBtn.classList.add('bg-gray-400');
        }

        // Reset Step Visibility
        const steps = [modalStepLocation, modalStepType, modalStepResSubsidy, modalStepSelection, modalStepData, modalStepSuccess];
        steps.forEach(step => step && step.classList.add('hidden'));
        if (modalStepLocation) modalStepLocation.classList.remove('hidden');
    }

    function openEnquiryModal(name, phone) {
        // Set basic info from trigger
        currentEnquiryData.name = name;
        currentEnquiryData.phone = phone;
        
        // Reset steps and other data
        resetModalSteps();
        
        if (enquiryModal) enquiryModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    function closeEnquiryModal() {
        if (enquiryModal) enquiryModal.classList.add('hidden');
        document.body.style.overflow = '';
    }

    function goToResults() {
        const params = new URLSearchParams({
            name: currentEnquiryData.name,
            phone: currentEnquiryData.phone,
            place: currentEnquiryData.place,
            type: currentEnquiryData.type,
            subsidy: currentEnquiryData.subsidy,
            comOpt: currentEnquiryData.commercialOption,
            units: currentEnquiryData.units,
            bill: currentEnquiryData.bill
        });
        window.location.href = '/calculator-results/?' + params.toString();
    }

    // Home/Biz Card Triggers
    [homeCalcCta, bizCalcCta].forEach((btn, idx) => {
        if (btn) {
            btn.addEventListener('click', () => {
                const nameInput = idx === 0 ? homeName : bizName;
                const phoneInput = idx === 0 ? homePhone : bizPhone;
                const name = nameInput ? nameInput.value.trim() : '';
                const phone = phoneInput ? phoneInput.value.trim() : '';
                if (!name || !phone) { alert('Please enter your Company/Name and Phone Number.'); return; }
                openEnquiryModal(name, phone);
            });
        }
    });

    if (heroGetStarted) {
        heroGetStarted.addEventListener('click', () => {
            openEnquiryModal('', '');
        });
    }

    // Step 1 -> Step 2
    if (modalLocationInput && nextToTypeBtn) {
        modalLocationInput.addEventListener('input', () => {
            if (modalLocationInput.value.trim().length > 0) {
                nextToTypeBtn.classList.remove('bg-gray-400');
                nextToTypeBtn.classList.add('bg-primary');
            } else {
                nextToTypeBtn.classList.remove('bg-primary');
                nextToTypeBtn.classList.add('bg-gray-400');
            }
        });

        nextToTypeBtn.addEventListener('click', () => {
            const place = modalLocationInput.value.trim();
            if (!place) { alert('Please enter a location.'); return; }
            currentEnquiryData.place = place;
            modalStepLocation.classList.add('hidden');
            modalStepType.classList.remove('hidden');
        });
    }

    // Step 2 -> Step 3
    typeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentEnquiryData.type = btn.getAttribute('data-type');
            modalStepType.classList.add('hidden');
            if (currentEnquiryData.type === 'Residential') {
                modalStepResSubsidy.classList.remove('hidden');
            } else {
                const label = document.getElementById('selection-step-label');
                if (label) label.textContent = 'Step 3';
                modalStepSelection.classList.remove('hidden');
            }
        });
    });

    // Step 3 Residential -> Selection step
    subsidyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentEnquiryData.subsidy = btn.getAttribute('data-subsidy');
            modalStepResSubsidy.classList.add('hidden');
            const label = document.getElementById('selection-step-label');
            if (label) label.textContent = 'Step 4';
            modalStepSelection.classList.remove('hidden');
        });
    });

    // Step Selection (Shared) -> Data Input Step
    comOptBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentEnquiryData.commercialOption = btn.getAttribute('data-opt');
            modalStepSelection.classList.add('hidden');
            modalStepData.classList.remove('hidden');
            
            // Update input UI based on choice
            const title = document.getElementById('data-title');
            const label = document.getElementById('data-label');
            const input = document.getElementById('modal-data-input');
            
            if (currentEnquiryData.commercialOption === 'Bill') {
                if (title) title.textContent = 'Enter Monthly Bill';
                if (label) label.textContent = 'Bill Amount (BHD)';
                if (input) input.placeholder = 'e.g. 150';
            } else {
                if (title) title.textContent = 'Enter Monthly Units';
                if (label) label.textContent = 'Total Units (Monthly)';
                if (input) input.placeholder = 'e.g. 1500';
            }
            if (input) input.focus();
        });
    });

    // Final Data Step -> Results
    if (modalDataInput && submitDataBtn) {
        modalDataInput.addEventListener('input', () => {
            if (modalDataInput.value.trim().length > 0) {
                submitDataBtn.classList.remove('bg-gray-400');
                submitDataBtn.classList.add('bg-primary');
            } else {
                submitDataBtn.classList.remove('bg-primary');
                submitDataBtn.classList.add('bg-gray-400');
            }
        });

        submitDataBtn.addEventListener('click', () => {
            const val = modalDataInput.value.trim();
            if (!val) { alert('Please enter a value.'); return; }
            
            if (currentEnquiryData.commercialOption === 'Bill') {
                currentEnquiryData.bill = val;
            } else {
                currentEnquiryData.units = val;
            }
            goToResults();
        });
    }

    if (closeModal) closeModal.addEventListener('click', closeEnquiryModal);
    window.addEventListener('click', (e) => {
        if (e.target === enquiryModal) closeEnquiryModal();
    });

    // Auto-popup logic for Home Page
    if (document.body.classList.contains('home-page')) {
        setTimeout(() => {
            if (enquiryModal && enquiryModal.classList.contains('hidden')) {
                openEnquiryModal('', '');
            }
        }, 5000); // Increased delay for a smoother landing
    }
}

/**
 * Sticky Header behavior 
 */
function initHeader() {
    const header = document.getElementById('main-header');
    if (!header) return;

    const topBar = header.querySelector('.bg-charcoal'); 
    const nav = header.querySelector('nav');
    const navLinks = document.getElementById('nav-links');
    const isHomePage = document.body.classList.contains('home-page');

    function updateHeader() {
        const scrollY = window.scrollY;
        const isScrolled = scrollY > 50; 

        if (isScrolled) {
            header.classList.add('glass-dark', 'shadow-md');
            header.classList.remove('glass-semi');
        } else {
            header.classList.add('glass-semi');
            header.classList.remove('glass-dark', 'shadow-md');
        }

        if (navLinks) {
            navLinks.classList.add('text-white');
        }

        if (nav) {
            nav.classList.toggle('py-2', isScrolled);
            nav.classList.toggle('py-4', !isScrolled);
        }
            
        if (topBar) {
            topBar.classList.toggle('hidden', isScrolled);
        }
    }

    window.addEventListener('scroll', updateHeader);
    updateHeader();
}

/**
 * Mobile Menu toggle logic
 */
function initMobileMenu() {
    const menuToggle = document.getElementById('menu-toggle');
    const menuClose = document.getElementById('menu-close');
    const mobileMenu = document.getElementById('mobile-menu');
    const servicesToggle = document.getElementById('mobile-services-toggle');
    const servicesContent = document.getElementById('mobile-services-content');
    const servicesIcon = document.getElementById('mobile-services-icon');

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', () => {
            mobileMenu.classList.remove('translate-x-full');
            document.body.style.overflow = 'hidden';
        });

        menuClose.addEventListener('click', () => {
            mobileMenu.classList.add('translate-x-full');
            document.body.style.overflow = '';
        });

        if (servicesToggle && servicesContent) {
            servicesToggle.addEventListener('click', () => {
                const isHidden = servicesContent.classList.contains('hidden');
                servicesContent.classList.toggle('hidden');
                if (servicesIcon) {
                    servicesIcon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
                }
            });
        }
    }
}

/**
 * Hero Carousel Logic
 */
function initHeroCarousel() {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    if (!slides.length) return;

    let currentSlide = 0;
    const slideCount = slides.length;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove('opacity-100', 'z-10');
            slide.classList.add('opacity-0', 'z-0');
            if (dots[i]) {
                dots[i].classList.remove('bg-primary');
                dots[i].classList.add('bg-white/30');
            }
        });

        slides[index].classList.add('opacity-100', 'z-10');
        slides[index].classList.remove('opacity-0', 'z-0');
        if (dots[index]) {
            dots[index].classList.add('bg-primary');
            dots[index].classList.remove('bg-white/30');
        }
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slideCount;
        showSlide(currentSlide);
    }

    let interval = setInterval(nextSlide, 5000);

    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            clearInterval(interval);
            currentSlide = i;
            showSlide(currentSlide);
            interval = setInterval(nextSlide, 5000);
        });
    });
}

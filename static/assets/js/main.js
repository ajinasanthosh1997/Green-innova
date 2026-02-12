/**
 * Green Innova - Main JavaScript
 * Handles Header behavior, Mobile Menu, and Global Animations
 */

document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initMobileMenu();
    initTabs();
    initCalculator();
    initChatbot();
    initScrollAnimations();
    initHeroCarousel();
});

/**
 * Chatbot UI Toggle
 */
function initChatbot() {
    const toggle = document.getElementById('chatbot-toggle');
    const close = document.getElementById('chat-close');
    const window = document.getElementById('chat-window');

    if (toggle && window) {
        toggle.addEventListener('click', () => {
            window.classList.toggle('opacity-0');
            window.classList.toggle('invisible');
            window.classList.toggle('translate-y-10');
        });

        close.addEventListener('click', () => {
            window.classList.add('opacity-0', 'invisible', 'translate-y-10');
        });
    }
}

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
        // observer.observe(el); // Disabled for now to keep implementation simple, can be enabled later
    });
}

/**
 * FINAL POLISH: Link Handling & Global Animations
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
        if (form.id === 'enquiry-form' || form.id === 'contact-form') return; // Handled locally on pages if present
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Thank you for your message! Our team will contact you soon.');
            form.reset();
        });
    });
}

/**
 * Initialize all features on load
 */
window.addEventListener('load', () => {
    initGlobalFeatures();
});

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
                if (!b.classList.contains('active')) {
                    b.classList.add('text-gray-400');
                    b.classList.remove('text-charcoal');
                }
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
 * Solar Savings Calculator Logic
 */
function initCalculator() {
    // 1. Home Calculator
    const billRange = document.getElementById('home-bill-range');
    const billValue = document.getElementById('home-bill-value');
    const savingsPerc = document.getElementById('home-savings-perc');
    const calcCta = document.getElementById('home-calc-cta');

    function updateHomeCalc() {
        if (!billRange || !window.SolarCalculator) return;
        const value = parseInt(billRange.value);
        billValue.textContent = `${value.toLocaleString()} AED`;
        
        // Match user's example: 700 AED = 2%
        // Using a linear mapping for the "Save Up To" percentage as requested
        const percentage = (value / 700) * 2;
        if (savingsPerc) {
            savingsPerc.textContent = `${Math.round(percentage)}%`;
        }
        
        // Update CTA link with bill amount
        if (calcCta) {
            calcCta.href = `calculator-results.html?bill=${value}`;
        }
    }

    if (billRange) {
        billRange.addEventListener('input', updateHomeCalc);
        updateHomeCalc(); // Initialize on load
    }

    // 2. Business Calculator
    const bizRange = document.getElementById('biz-bill-range');
    const bizValue = document.getElementById('biz-bill-value');
    const bizSavingsPerc = document.getElementById('biz-savings-perc');
    const bizCalcCta = document.getElementById('biz-calc-cta');

    function updateBizCalc() {
        if (!bizRange || !window.SolarCalculator) return;
        const value = parseInt(bizRange.value);
        bizValue.textContent = `${value.toLocaleString()} AED`;
        
        // Match home mapping: 700 AED = 2%
        const percentage = (value / 700) * 2;
        if (bizSavingsPerc) {
            bizSavingsPerc.textContent = `${Math.round(percentage)}%`;
        }
        
        // Update CTA link with bill amount
        if (bizCalcCta) {
            bizCalcCta.href = `calculator-results.html?bill=${value}`;
        }
    }

    if (bizRange) {
        bizRange.addEventListener('input', updateBizCalc);
        updateBizCalc(); // Initialize on load
    }
}

/**
 * Sticky Header behavior with glassmorphism transition
 */
function initHeader() {
    const header = document.getElementById('main-header');
    if (!header) return;

    const topBar = header.querySelector('.bg-charcoal'); // More reliable selector for the top bar
    const nav = header.querySelector('nav');
    const subNav = document.getElementById('service-subnav');
    const navLinks = document.getElementById('nav-links');
    const mainLogo = document.getElementById('main-logo');
    const isHomePage = document.body.classList.contains('home-page');
    const menuToggle = document.getElementById('menu-toggle');

    function updateHeader() {
        const scrollY = window.scrollY;

        // Semi-transparent (50%) initially, dark glass (90%) after scroll
        const isScrolled = scrollY > 50; 

        if (isScrolled) {
            header.classList.add('glass-dark', 'shadow-md');
            header.classList.remove('glass-semi', 'glass-effect');
        } else {
            header.classList.add('glass-semi');
            header.classList.remove('glass-dark', 'shadow-md', 'glass-effect');
        }

        // Always keep text white for the white logo theme
        if (navLinks) {
            navLinks.classList.remove('text-charcoal');
            navLinks.classList.add('text-white');
        }
        if (menuToggle) {
            menuToggle.classList.remove('text-charcoal');
            menuToggle.classList.add('text-white');
        }

        if (nav) {
            if (isHomePage) {
                nav.classList.toggle('py-2', scrollY > 50);
                nav.classList.toggle('py-4', scrollY <= 50);
            } else {
                nav.classList.remove('py-4');
                nav.classList.add('py-2');
            }
        }
            
        // Handle top bar visibility
        if (topBar) {
            if (scrollY > 50) {
                topBar.classList.add('hidden');
            } else {
                topBar.classList.remove('hidden');
            }
        }

        // Service Sub-nav visibility logic
        if (subNav) {
            if (scrollY > 400) subNav.classList.add('show');
            else subNav.classList.remove('show');
        }
    }

    // Mute all videos specifically for the "gilt" request
    document.querySelectorAll('video').forEach(video => {
        video.muted = true;
        video.setAttribute('muted', '');
    });

    window.addEventListener('scroll', updateHeader);
    updateHeader(); // Run on load
}

/**
 * Mobile Menut toggle logic
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
            document.body.style.overflow = 'hidden'; // Prevent background scroll
        });

        menuClose.addEventListener('click', () => {
            mobileMenu.classList.add('translate-x-full');
            document.body.style.overflow = '';
        });

        // Services Collapse Logic
        if (servicesToggle && servicesContent) {
            servicesToggle.addEventListener('click', () => {
                const isHidden = servicesContent.classList.contains('hidden');
                servicesContent.classList.toggle('hidden');
                if (servicesIcon) {
                    servicesIcon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
                }
            });
        }

        // Close menu on link click
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('translate-x-full');
                document.body.style.overflow = '';
            });
        });
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
            dots[i].classList.remove('bg-primary');
            dots[i].classList.add('bg-white/30');
        });

        slides[index].classList.add('opacity-100', 'z-10');
        slides[index].classList.remove('opacity-0', 'z-0');
        dots[index].classList.add('bg-primary');
        dots[index].classList.remove('bg-white/30');
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slideCount;
        showSlide(currentSlide);
    }

    // Auto-play
    let interval = setInterval(nextSlide, 5000);

    // Manual Nav
    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            clearInterval(interval);
            currentSlide = i;
            showSlide(currentSlide);
            interval = setInterval(nextSlide, 5000);
        });
    });
}

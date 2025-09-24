// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 70; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add active class to navigation links based on scroll position
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPos = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                // Remove active class from all links
                navLinks.forEach(link => link.classList.remove('active'));
                
                // Add active class to current section's link
                const activeLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    });
    
    // Add fade-in animation for elements as they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections for animation
    const animatedElements = document.querySelectorAll('.analysis-card, .insight-category, .stat-card, .mission, .methodology, .impact');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Initialize all carousels
    function initializeCarousel(carousel) {
        const track = carousel.querySelector('.carousel-track');
        const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
        const btnPrev = carousel.querySelector('.carousel-btn.prev');
        const btnNext = carousel.querySelector('.carousel-btn.next');
        const captionIndex = carousel.querySelector('.carousel-index');
        const captionText = carousel.querySelector('.carousel-text');
        const dotsContainer = carousel.querySelector('.carousel-dots');

        if (!track || !slides.length || !btnPrev || !btnNext) return;

        let current = 0;

        // Build dots
        slides.forEach((_, idx) => {
            const dot = document.createElement('button');
            dot.className = 'carousel-dot';
            dot.setAttribute('aria-label', `Go to slide ${idx + 1}`);
            dot.addEventListener('click', () => goTo(idx));
            dotsContainer.appendChild(dot);
        });

        function update() {
            const offset = -current * 100;
            track.style.transform = `translateX(${offset}%)`;
            if (captionIndex) captionIndex.textContent = `${current + 1} / ${slides.length}`;
            if (captionText) captionText.textContent = slides[current].dataset.caption || '';
            Array.from(dotsContainer.children).forEach((d, i) => {
                d.classList.toggle('active', i === current);
            });
        }

        function goTo(idx) {
            current = (idx + slides.length) % slides.length;
            update();
        }

        btnPrev.addEventListener('click', (e) => {
            e.preventDefault();
            goTo(current - 1);
        });
        btnNext.addEventListener('click', (e) => {
            e.preventDefault();
            goTo(current + 1);
        });

        // Keyboard navigation
        carousel.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') goTo(current - 1);
            if (e.key === 'ArrowRight') goTo(current + 1);
        });

        // Swipe support (basic)
        let startX = 0;
        track.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; });
        track.addEventListener('touchend', (e) => {
            const dx = e.changedTouches[0].clientX - startX;
            if (dx > 40) goTo(current - 1);
            if (dx < -40) goTo(current + 1);
        });

        // Initialize
        update();
        carousel.setAttribute('tabindex', '0');
    }

    // Initialize all carousels
    const allCarousels = document.querySelectorAll('.map-carousel');
    allCarousels.forEach(initializeCarousel);

});


// DOM Elements
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const hamburger = document.querySelector('.hamburger');
const sidebar = document.querySelector('.sidebar');
const overlay = document.querySelector('.overlay');
const sidebarItems = document.querySelectorAll('.sidebar-item');

// Utility function to check if device is mobile
const isMobile = () => window.innerWidth <= 768;

// Toggle sidebar collapsed state for desktop
function toggleSidebarCollapsed(collapsed) {
    if (!isMobile()) {
        sidebar.classList.toggle('sidebar-collapsed', collapsed);
        document.querySelector('main').style.marginLeft = collapsed ? 
            `${getComputedStyle(document.documentElement).getPropertyValue('--sidebar-collapsed-width')}` : 
            `${getComputedStyle(document.documentElement).getPropertyValue('--sidebar-width')}`;
    }
}

// Toggle mobile menu
function toggleMobileMenu() {
    if (isMobile()) {
        sidebar.classList.toggle('active');
        hamburger.classList.toggle('open');
        overlay.classList.toggle('active');
        document.body.style.overflow = sidebar.classList.contains('active') ? 'hidden' : '';
    }
}

// Initialize sidebar state
function initializeSidebar() {
    if (!isMobile()) {
        // Desktop: Start with collapsed sidebar
        toggleSidebarCollapsed(true);
        
        // Add hover listeners for desktop
        sidebar.addEventListener('mouseenter', () => toggleSidebarCollapsed(false));
        sidebar.addEventListener('mouseleave', () => toggleSidebarCollapsed(true));
    } else {
        // Mobile: Remove any desktop-specific classes
        sidebar.classList.remove('sidebar-collapsed');
        document.querySelector('main').style.marginLeft = '0';
    }
}

// Event Listeners
mobileMenuBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleMobileMenu();
});

overlay.addEventListener('click', toggleMobileMenu);

sidebarItems.forEach(item => {
    item.addEventListener('click', () => {
        if (isMobile() && sidebar.classList.contains('active')) {
            toggleMobileMenu();
        }
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (isMobile()) {
        const isClickInsideSidebar = sidebar.contains(e.target);
        const isClickInsideButton = mobileMenuBtn.contains(e.target);
        
        if (!isClickInsideSidebar && !isClickInsideButton && sidebar.classList.contains('active')) {
            toggleMobileMenu();
        }
    }
});

// Handle window resize
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        if (isMobile()) {
            // Switch to mobile layout
            sidebar.classList.remove('sidebar-collapsed');
            document.querySelector('main').style.marginLeft = '0';
            if (sidebar.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            }
        } else {
            // Switch to desktop layout
            sidebar.classList.remove('active');
            hamburger.classList.remove('open');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
            toggleSidebarCollapsed(true);
        }
    }, 250);
});

// Touch swipe functionality for mobile
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

document.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    if (isMobile()) {
        handleSwipe();
    }
}, { passive: true });

function handleSwipe() {
    const swipeThreshold = 50;
    const difference = touchEndX - touchStartX;
    
    if (Math.abs(difference) > swipeThreshold) {
        if (difference > 0 && !sidebar.classList.contains('active')) {
            // Swipe right to open
            toggleMobileMenu();
        } else if (difference < 0 && sidebar.classList.contains('active')) {
            // Swipe left to close
            toggleMobileMenu();
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeSidebar);
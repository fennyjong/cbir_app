 // Mobile menu functionality
 const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
 const hamburger = document.querySelector('.hamburger');
 const sidebar = document.querySelector('.sidebar');
 const overlay = document.querySelector('.overlay');
 const scrollToTop = document.querySelector('.scroll-to-top');

 // Toggle mobile menu
 function toggleMobileMenu() {
     sidebar.classList.toggle('active');
     hamburger.classList.toggle('open');
     overlay.classList.toggle('active');
     document.body.style.overflow = sidebar.classList.contains('active') ? 'hidden' : '';
 }

 mobileMenuBtn.addEventListener('click', toggleMobileMenu);
 overlay.addEventListener('click', toggleMobileMenu);

 // Close mobile menu on link click
 const sidebarLinks = document.querySelectorAll('.sidebar-item');
 sidebarLinks.forEach(link => {
     link.addEventListener('click', () => {
         if (sidebar.classList.contains('active')) {
             toggleMobileMenu();
         }
     });
 });

 // Scroll to top button functionality
 window.addEventListener('scroll', () => {
     if (window.pageYOffset > 300) {
         scrollToTop.classList.add('visible');
     } else {
         scrollToTop.classList.remove('visible');
     }
 });

 scrollToTop.addEventListener('click', () => {
     window.scrollTo({
         top: 0,
         behavior: 'smooth'
     });
 });

 // Close sidebar when clicking outside on mobile
 document.addEventListener('click', (e) => {
     if (window.innerWidth <= 768) {
         const isClickInsideSidebar = sidebar.contains(e.target);
         const isClickInsideButton = mobileMenuBtn.contains(e.target);
         
         if (!isClickInsideSidebar && !isClickInsideButton && sidebar.classList.contains('active')) {
             toggleMobileMenu();
         }
     }
 });

 // Handle window resize
 window.addEventListener('resize', () => {
     if (window.innerWidth > 768 && sidebar.classList.contains('active')) {
         toggleMobileMenu();
     }
 });
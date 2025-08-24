(function() {
    // Toggle sidebar on mobile
    const sidebarToggleBtn = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const mobileCloseBtn = document.getElementById('mobile-close-btn');
    
    sidebarToggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('hidden');
    });
    
    mobileCloseBtn.addEventListener('click', function() {
        sidebar.classList.add('hidden');
    });
    
    // Toggle user dropdown
    const userDropdownToggle = document.getElementById('user-dropdown-toggle');
    const userDropdown = document.getElementById('user-dropdown');
    
    userDropdownToggle.addEventListener('click', function() {
        userDropdown.classList.toggle('show');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        const container = document.getElementById('user-dropdown-container');
        if (container && !container.contains(event.target)) {
            userDropdown.classList.remove('show');
        }
    });
    
    // Navigation / Page switching
    const navItems = document.querySelectorAll('.nav-item');
    const pageContents = document.querySelectorAll('.page-content');
    const pageTitle = document.getElementById('page-title');
    
    // Save active page to localStorage
    function saveActivePage(pageId) {
        localStorage.setItem('activeEbookPage', pageId);
    }
    
    // Load active page from localStorage
    function loadActivePage() {
        return localStorage.getItem('activeEbookPage') || 'dashboard';
    }
    
    // Set the active page on initial load
    function setActivePage(pageId) {
        // Remove active class from all nav items
        navItems.forEach(nav => {
            nav.classList.remove('active');
        });
        
        // Add active class to the matching nav item
        const activeNavItem = document.querySelector(`.nav-item[href="#${pageId}"]`);
        if (activeNavItem) {
            activeNavItem.classList.add('active');
        }
        
        // Hide all pages
        pageContents.forEach(page => {
            page.classList.add('hidden');
        });
        
        // Show the target page
        const targetPage = document.getElementById(pageId + '-page');
        if (targetPage) {
            targetPage.classList.remove('hidden');
            // Update page title
            pageTitle.textContent = pageId.charAt(0).toUpperCase() + pageId.slice(1);
            
            // Apply fade-in animation
            targetPage.classList.add('fade-in');
        }
    }
    
    // Set initial active page
    const initialPage = loadActivePage();
    setActivePage(initialPage);
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the page ID from the href
            const targetId = this.getAttribute('href').substring(1);
            
            // Save and set the active page
            saveActivePage(targetId);
            setActivePage(targetId);
            
            // Close sidebar on mobile after navigation
            if (window.innerWidth < 768) {
                sidebar.classList.add('hidden');
            }
        });
    });
    
    // Animate stat cards on dashboard page load
    function animateStatCards() {
        const dashboard = document.getElementById('dashboard-page');
        if (!dashboard.classList.contains('hidden')) {
            const statCards = document.querySelectorAll('.stat-card');
            statCards.forEach((card, index) => {
                setTimeout(() => {
                    card.style.transform = 'translateY(-5px)';
                    setTimeout(() => {
                        card.style.transform = 'translateY(0)';
                    }, 300);
                }, index * 100);
            });
        }
    }
    
    // Run animation on page load and whenever dashboard becomes visible
    animateStatCards();
    
    // Check for dark mode preference
    function setThemePreference() {
        const isDarkMode = localStorage.getItem('ebookDarkMode') === 'true';
        document.documentElement.classList.toggle('dark', isDarkMode);
    }
    
    // Set theme on initial load
    setThemePreference();
    
    // Theme toggle buttons (find them in settings page)
    const themeButtons = document.querySelectorAll('.settings-page .theme-button');
    themeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const theme = this.dataset.theme;
            if (theme === 'dark') {
                localStorage.setItem('ebookDarkMode', 'true');
            } else if (theme === 'light') {
                localStorage.setItem('ebookDarkMode', 'false');
            }
            setThemePreference();
        });
    });
})();

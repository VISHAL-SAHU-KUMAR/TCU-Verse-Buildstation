// ==================== MAIN.JS - Landing Page Logic ====================

// Global state
let currentUser = null;

// DOM Elements
const loginModal = document.getElementById('loginModal');
const signupModal = document.getElementById('signupModal');
const loginBtn = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signupBtn');
const closeLogin = document.getElementById('closeLogin');
const closeSignup = document.getElementById('closeSignup');
const switchToSignup = document.getElementById('switchToSignup');
const switchToLogin = document.getElementById('switchToLogin');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const getStartedBtn = document.getElementById('getStartedBtn');
const ctaBtn = document.getElementById('ctaBtn');
const mobileToggle = document.getElementById('mobileToggle');

// ==================== MODAL FUNCTIONS ====================

function openModal(modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(modal) {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Event Listeners for Modal Open/Close
if (loginBtn) {
    loginBtn.addEventListener('click', () => openModal(loginModal));
}

if (signupBtn) {
    signupBtn.addEventListener('click', () => openModal(signupModal));
}

if (getStartedBtn) {
    getStartedBtn.addEventListener('click', () => openModal(signupModal));
}

if (ctaBtn) {
    ctaBtn.addEventListener('click', () => openModal(signupModal));
}

if (closeLogin) {
    closeLogin.addEventListener('click', () => closeModal(loginModal));
}

if (closeSignup) {
    closeSignup.addEventListener('click', () => closeModal(signupModal));
}

// Switch between modals
if (switchToSignup) {
    switchToSignup.addEventListener('click', (e) => {
        e.preventDefault();
        closeModal(loginModal);
        openModal(signupModal);
    });
}

if (switchToLogin) {
    switchToLogin.addEventListener('click', (e) => {
        e.preventDefault();
        closeModal(signupModal);
        openModal(loginModal);
    });
}

// Close modal on outside click
window.addEventListener('click', (e) => {
    if (e.target === loginModal) {
        closeModal(loginModal);
    }
    if (e.target === signupModal) {
        closeModal(signupModal);
    }
});

// ==================== AUTHENTICATION ====================

// Check if user is already logged in
async function checkAuth() {
    try {
        const response = await fetch('/api/check-auth', {
            credentials: 'include'
        });
        const data = await response.json();

        if (data.authenticated) {
            currentUser = data.user;
            // Redirect to dashboard if on landing page
            window.location.href = '/dashboard.html';
        }
    } catch (error) {
        console.error('Auth check error:', error);
    }
}

// Login Handler
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        const submitBtn = loginForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                showToast('Login successful! Redirecting...', 'success');
                currentUser = data.user;
                setTimeout(() => {
                    window.location.href = '/dashboard.html';
                }, 1000);
            } else {
                showToast(data.error || 'Login failed', 'error');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        } catch (error) {
            console.error('Login error:', error);
            showToast('Network error. Please try again.', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    });
}

// Signup Handler
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const fullName = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;

        // Basic validation
        if (password.length < 6) {
            showToast('Password must be at least 6 characters', 'error');
            return;
        }

        const submitBtn = signupForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating account...';
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ full_name: fullName, email, password })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                showToast('Account created successfully! Redirecting...', 'success');
                currentUser = data.user;
                setTimeout(() => {
                    window.location.href = '/dashboard.html';
                }, 1000);
            } else {
                showToast(data.error || 'Registration failed', 'error');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        } catch (error) {
            console.error('Signup error:', error);
            showToast('Network error. Please try again.', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    });
}

// ==================== TOAST NOTIFICATIONS ====================

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icon = type === 'success' ? 'fa-check-circle' :
                 type === 'error' ? 'fa-exclamation-circle' :
                 'fa-info-circle';

    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span class="toast-message">${message}</span>
    `;

    document.body.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease';
    }, 10);

    // Remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 4000);
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10000;
        min-width: 300px;
    }
    .toast.success {
        border-left: 4px solid #10b981;
    }
    .toast.error {
        border-left: 4px solid #ef4444;
    }
    .toast i {
        font-size: 20px;
    }
    .toast.success i {
        color: #10b981;
    }
    .toast.error i {
        color: #ef4444;
    }
    .toast-message {
        color: #1f2937;
        font-size: 14px;
    }
`;
document.head.appendChild(style);

// ==================== SMOOTH SCROLLING ====================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });

            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            this.classList.add('active');
        }
    });
});

// ==================== NAVBAR SCROLL EFFECT ====================

let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 50) {
        navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
    }

    lastScroll = currentScroll;
});

// ==================== MOBILE MENU ====================

if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
        const navMenu = document.querySelector('.nav-menu');
        navMenu.classList.toggle('active');

        // Toggle icon
        const icon = mobileToggle.querySelector('i');
        if (icon.classList.contains('fa-bars')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });
}

// Add mobile menu styles
const mobileStyle = document.createElement('style');
mobileStyle.textContent = `
    @media (max-width: 768px) {
        .nav-menu {
            position: fixed;
            top: 70px;
            right: -100%;
            background: white;
            width: 250px;
            height: calc(100vh - 70px);
            flex-direction: column;
            align-items: flex-start;
            padding: 30px;
            box-shadow: -2px 0 10px rgba(0,0,0,0.1);
            transition: right 0.3s ease;
            gap: 20px;
        }

        .nav-menu.active {
            right: 0;
        }

        .nav-menu .btn {
            width: 100%;
            justify-content: center;
        }
    }
`;
document.head.appendChild(mobileStyle);

// ==================== INTERSECTION OBSERVER (Fade-in animations) ====================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards
document.querySelectorAll('.feature-card, .step, .role-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ==================== INITIALIZE ====================

// Check authentication on page load
checkAuth();

// Add loading state
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

console.log('%c🧠 SkillLens AI', 'color: #667eea; font-size: 24px; font-weight: bold;');
console.log('%cCareer Intelligence Platform', 'color: #764ba2; font-size: 14px;');

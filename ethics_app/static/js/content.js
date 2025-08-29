// Consent Management JavaScript
// File: static/js/consent.js

class ConsentManager {
    constructor() {
        this.consentTypes = ['functional', 'analytics', 'marketing'];
        this.consentData = this.loadConsentData();
        this.cookieBanner = document.getElementById('cookie-banner');
        this.init();
    }

    init() {
        // Show banner if no consent given
        if (!this.hasEssentialConsent()) {
            this.showCookieBanner();
        }

        // Load analytics/marketing scripts based on consent
        this.loadConsentBasedScripts();

        // Set up event listeners
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Language switching
        document.addEventListener('DOMContentLoaded', () => {
            this.updateRTLSupport();
        });

        // Form submissions with loading states
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitButton = form.querySelector('button[type="submit"]');
                if (submitButton) {
                    this.showLoadingState(submitButton);
                }
            });
        });

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    // Cookie Banner Management
    showCookieBanner() {
        if (this.cookieBanner) {
            this.cookieBanner.style.display = 'block';
            // Add fade in animation
            setTimeout(() => {
                this.cookieBanner.style.opacity = '1';
            }, 100);
        }
    }

    hideCookieBanner() {
        if (this.cookieBanner) {
            this.cookieBanner.style.opacity = '0';
            setTimeout(() => {
                this.cookieBanner.style.display = 'none';
            }, 300);
        }
    }

    // Consent Data Management
    loadConsentData() {
        try {
            const data = localStorage.getItem('consentData');
            return data ? JSON.parse(data) : {};
        } catch (e) {
            console.warn('Failed to load consent data:', e);
            return {};
        }
    }

    saveConsentData(data) {
        try {
            const consentData = {
                ...this.consentData,
                ...data,
                timestamp: new Date().toISOString(),
                version: '1.0'
            };
            localStorage.setItem('consentData', JSON.stringify(consentData));
            this.consentData = consentData;
            
            // Send to server
            this.sendConsentToServer(data);
        } catch (e) {
            console.warn('Failed to save consent data:', e);
        }
    }

    async sendConsentToServer(consentData) {
        try {
            const response = await fetch('/api/cookie-consent/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(consentData)
            });

            if (!response.ok) {
                throw new Error('Failed to send consent to server');
            }
        } catch (e) {
            console.warn('Failed to send consent to server:', e);
        }
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    hasEssentialConsent() {
        return this.consentData.functional === true;
    }

    hasConsent(type) {
        return this.consentData[type] === true;
    }

    // Script Loading Based on Consent
    loadConsentBasedScripts() {
        // Analytics Scripts
        if (this.hasConsent('analytics')) {
            this.loadGoogleAnalytics();
        }

        // Marketing Scripts
        if (this.hasConsent('marketing')) {
            this.loadMarketingScripts();
        }
    }

    loadGoogleAnalytics() {
        // Example Google Analytics loading
        if (typeof gtag === 'undefined') {
            const script1 = document.createElement('script');
            script1.async = true;
            script1.src = 'https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID';
            document.head.appendChild(script1);

            const script2 = document.createElement('script');
            script2.innerHTML = `
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', 'GA_MEASUREMENT_ID', {
                    anonymize_ip: true,
                    cookie_flags: 'max-age=7200;secure;samesite=none'
                });
            `;
            document.head.appendChild(script2);
        }
    }

    loadMarketingScripts() {
        // Load marketing/advertising scripts here
        console.log('Loading marketing scripts...');
    }

    // RTL Language Support
    updateRTLSupport() {
        const htmlElement = document.documentElement;
        const currentLang = htmlElement.getAttribute('lang');
        
        if (currentLang === 'ar') {
            htmlElement.setAttribute('dir', 'rtl');
            document.body.classList.add('rtl');
        } else {
            htmlElement.setAttribute('dir', 'ltr');
            document.body.classList.remove('rtl');
        }
    }

    // Loading States
    showLoadingState(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<span class="loading me-2"></span>Processing...';
        button.disabled = true;
        
        // Reset after 5 seconds (fallback)
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 5000);
    }

    // Utility Methods
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Privacy-focused event tracking
    trackEvent(eventName, properties = {}) {
        if (this.hasConsent('analytics')) {
            // Only track if user consented to analytics
            if (typeof gtag !== 'undefined') {
                gtag('event', eventName, {
                    ...properties,
                    anonymize_ip: true
                });
            }
        }
    }
}

// Global functions for cookie banner
function acceptAllCookies() {
    const consent = {
        functional: true,
        analytics: true,
        marketing: true
    };
    
    consentManager.saveConsentData(consent);
    consentManager.hideCookieBanner();
    consentManager.loadConsentBasedScripts();
    
    // Show success message
    showNotification('Cookie preferences saved successfully!', 'success');
    
    // Track event (will only fire if analytics consent given)
    consentManager.trackEvent('consent_all_accepted');
}

function acceptEssentialCookies() {
    const consent = {
        functional: true,
        analytics: false,
        marketing: false
    };
    
    consentManager.saveConsentData(consent);
    consentManager.hideCookieBanner();
    
    showNotification('Essential cookies accepted', 'info');
    consentManager.trackEvent('consent_essential_only');
}

function showCookieSettings() {
    // Redirect to consent management page
    window.location.href = '/consent/';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 1060;
        min-width: 300px;
        max-width: 400px;
    `;
    
    notification.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Cookie utility functions
const CookieUtils = {
    set(name, value, days = 365) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;secure;samesite=strict`;
    },

    get(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    },

    delete(name) {
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/`;
    },

    // GDPR compliant cookie cleaning
    cleanNonEssentialCookies() {
        const essentialCookies = ['csrftoken', 'sessionid', 'consentData'];
        const cookies = document.cookie.split(';');
        
        cookies.forEach(cookie => {
            const [name] = cookie.trim().split('=');
            if (!essentialCookies.includes(name)) {
                this.delete(name);
            }
        });
    }
};

// Form validation utilities
const FormUtils = {
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    validateRequired(value) {
        return value && value.trim().length > 0;
    },

    showFieldError(field, message) {
        // Remove existing error
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }

        // Add new error
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error text-danger mt-1';
        errorDiv.innerHTML = `<small><i class="fas fa-exclamation-triangle me-1"></i>${message}</small>`;
        field.parentNode.appendChild(errorDiv);
        
        // Add error styling to field
        field.classList.add('is-invalid');
    },

    clearFieldError(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        field.classList.remove('is-invalid');
    }
};

// Accessibility utilities
const A11yUtils = {
    announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    },

    trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];
        
        element.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey && document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
            }
        });
    }
};

// Performance monitoring
const PerformanceUtils = {
    measurePageLoad() {
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData && consentManager.hasConsent('analytics')) {
                consentManager.trackEvent('page_load_time', {
                    load_time: Math.round(perfData.loadEventEnd - perfData.loadEventStart),
                    dom_ready: Math.round(perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart)
                });
            }
        });
    },

    measureUserEngagement() {
        let startTime = Date.now();
        let isVisible = true;
        
        // Track page visibility
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                isVisible = false;
                const timeSpent = Date.now() - startTime;
                if (consentManager.hasConsent('analytics') && timeSpent > 5000) {
                    consentManager.trackEvent('page_engagement', {
                        time_spent: Math.round(timeSpent / 1000)
                    });
                }
            } else {
                isVisible = true;
                startTime = Date.now();
            }
        });

        // Track scroll depth
        let maxScroll = 0;
        window.addEventListener('scroll', consentManager.debounce(() => {
            const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            if (scrollPercent > maxScroll) {
                maxScroll = scrollPercent;
            }
        }, 500));

        // Send scroll data on page unload
        window.addEventListener('beforeunload', () => {
            if (consentManager.hasConsent('analytics') && maxScroll > 25) {
                consentManager.trackEvent('scroll_depth', {
                    max_scroll: maxScroll
                });
            }
        });
    }
};

// Security utilities
const SecurityUtils = {
    sanitizeInput(input) {
        const temp = document.createElement('div');
        temp.textContent = input;
        return temp.innerHTML;
    },

    validateCSRF() {
        const token = consentManager.getCSRFToken();
        if (!token) {
            console.warn('CSRF token not found');
            return false;
        }
        return true;
    },

    // Content Security Policy helper
    loadScriptSecurely(src, integrity = null) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.async = true;
            
            if (integrity) {
                script.integrity = integrity;
                script.crossOrigin = 'anonymous';
            }
            
            script.onload = resolve;
            script.onerror = reject;
            
            document.head.appendChild(script);
        });
    }
};

// Data minimization utilities
const DataMinimizationUtils = {
    // Remove PII from tracking data
    sanitizeTrackingData(data) {
        const sensitiveFields = ['email', 'phone', 'name', 'address', 'ssn', 'id'];
        const cleaned = { ...data };
        
        sensitiveFields.forEach(field => {
            if (cleaned[field]) {
                delete cleaned[field];
            }
        });
        
        return cleaned;
    },

    // Hash sensitive data for analytics
    hashSensitiveData(data) {
        if (typeof data === 'string' && data.length > 0) {
            // Simple hash function (use proper crypto in production)
            let hash = 0;
            for (let i = 0; i < data.length; i++) {
                const char = data.charCodeAt(i);
                hash = ((hash << 5) - hash) + char;
                hash = hash & hash; // Convert to 32-bit integer
            }
            return hash.toString(16);
        }
        return null;
    }
};

// Initialize consent manager when DOM is ready
let consentManager;

document.addEventListener('DOMContentLoaded', () => {
    consentManager = new ConsentManager();
    
    // Initialize performance monitoring if analytics consent given
    if (consentManager.hasConsent('analytics')) {
        PerformanceUtils.measurePageLoad();
        PerformanceUtils.measureUserEngagement();
    }
    
    // Add fade-in animation to main content
    document.querySelector('main')?.classList.add('fade-in');
    
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
    
    // Enhanced form validation
    const forms = document.querySelectorAll('form[data-validate="true"]');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
});

// Enhanced form validation
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        FormUtils.clearFieldError(field);
        
        if (!FormUtils.validateRequired(field.value)) {
            FormUtils.showFieldError(field, 'This field is required');
            isValid = false;
        } else if (field.type === 'email' && !FormUtils.validateEmail(field.value)) {
            FormUtils.showFieldError(field, 'Please enter a valid email address');
            isValid = false;
        }
    });
    
    if (!isValid) {
        A11yUtils.announceToScreenReader('Form contains errors. Please check the highlighted fields.');
    }
    
    return isValid;
}

// Export utilities for use in other scripts
window.ConsentManager = ConsentManager;
window.CookieUtils = CookieUtils;
window.FormUtils = FormUtils;
window.A11yUtils = A11yUtils;
window.SecurityUtils = SecurityUtils;
window.DataMinimizationUtils = DataMinimizationUtils;

// Error handling
window.addEventListener('error', (e) => {
    console.error('JavaScript error:', e.error);
    
    // Only report errors if analytics consent given
    if (consentManager && consentManager.hasConsent('analytics')) {
        consentManager.trackEvent('javascript_error', {
            message: e.message,
            filename: e.filename,
            line: e.lineno
        });
    }
});

// Unhandled promise rejection handling
window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    
    if (consentManager && consentManager.hasConsent('analytics')) {
        consentManager.trackEvent('promise_rejection', {
            reason: e.reason?.toString() || 'Unknown'
        });
    }
});

// Service Worker registration for offline functionality
if ('serviceWorker' in navigator && consentManager.hasConsent('functional')) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

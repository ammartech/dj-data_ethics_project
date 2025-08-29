// consent.js - Cookie Consent Management

function acceptAll() {
    // Enable all optional cookie toggles
    document.querySelectorAll('input[type="checkbox"]:not([disabled])').forEach(checkbox => {
        checkbox.checked = true;
    });

    // Show confirmation
    showNotification("All cookies enabled", "success");

    // Submit form
    document.querySelector(".consent-form").submit();
}

function rejectAll() {
    // Disable all optional cookie toggles
    document.querySelectorAll('input[type="checkbox"]:not([disabled])').forEach(checkbox => {
        checkbox.checked = false;
    });

    // Show confirmation
    showNotification("Only essential cookies will be used", "info");

    // Submit form
    document.querySelector(".consent-form").submit();
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement("div");
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

    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Initialize extra behaviors
document.addEventListener("DOMContentLoaded", function() {
    // Smooth scroll to action buttons
    const actions = document.querySelector(".consent-actions");
    if (actions) {
        actions.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    }
});


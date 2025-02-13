
if (document.getElementById('otp-form')) {

    if (document.getElementById('error-message'))
        errorDiv = document.getElementById('error-message')
    document.getElementById('otp-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting normally
        form = document.getElementById('otp-form');
        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                to_unspecified_page(data.redirect_url);
            } else {
                if (errorDiv) {
                    errorDiv.innerHTML = `<p>${data.error}</p>`; // Display error message
                }
            }
        })
        .catch(error => console.error('Error:', error));
    })
}

if (document.getElementById('checker')) {

    if (document.getElementById('error-message'))
        errorDiv = document.getElementById('error-message')
    document.getElementById('checker').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting normally
        form = document.getElementById('checker');
        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                to_unspecified_page(data.redirect_url);
            } else {
                if (errorDiv) {
                    errorDiv.innerHTML = `<p>${data.error}</p>`; // Display error message
                }
            }
        })
        .catch(error => console.error('Error:', error));
    })
}

if (document.getElementById('login-form')) {

    const form = document.getElementById('login-form');
    const errorMessageDiv = document.getElementById('error-message');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        errorMessageDiv.textContent = '';
        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            const result = await response.json();

            if (result.success) {
                to_unspecified_page(result.redirect_url);
            } else {
                errorMessageDiv.textContent = result.error || 'Login failed. Please try again.';
            }
        } catch (error) {
            console.error('Error:', error);
            errorMessageDiv.textContent = 'An unexpected error occurred. Please try again.';
        }
    });
}

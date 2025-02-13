(function() {
    function startOAuth2Flow() {
        window.location.href = '/oauth/start/';
    }

    function handleOAuthCallback() {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');

        if (code) {
            fetch('/oauth/callback/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ code: code })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        console.log('Error response data:', data);
                        throw new Error(`Failed to register: ${data.error || 'Unknown error'}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                to_unspecified_page('/game');
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }

    const authButton = document.getElementById("42_auth_button");
    if (authButton) {
        authButton.addEventListener('click', startOAuth2Flow);
    }

    handleOAuthCallback();
})();

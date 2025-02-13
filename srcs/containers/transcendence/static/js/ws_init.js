
function getWebSocket() {
    if (!socket || socket.readyState === WebSocket.CLOSED) {

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const websocketUrl = `${protocol}//${window.location.host}/ws/authentication/social/`;

        socket = new WebSocket(websocketUrl);

        socket.onopen = function (e) {
        };

        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (data.type === 'redirect') {
                to_unspecified_page(data.url);
            }
        };

        socket.onclose = function (event) {
            if (event.wasClean === false && event.code === 1006) {
                to_unspecified_page = '/';
            }
            if (event.wasClean) {
            } else {
                reload_scripts(window.location.pathname);
            }
        };
    
        socket.onerror = function (error) {
            console.log(`[error] ${error.message}`);
        };
    }
    return socket;

}

getWebSocket();
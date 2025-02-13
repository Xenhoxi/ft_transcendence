
function open_match_socket(game_data) {
    if (game_socket)
        if (game_socket.readyState === WebSocket.OPEN) {
            game_socket.close();
            game_socket.onclose = function (event) {
                pong_websocket(game_data, '/ws/game/match/');
            };
        }
        else if (game_socket.readyState === WebSocket.CONNECTING)
            timeoutID = setTimeout(open_match_socket, 100);
}

function open_match_ai_socket(game_data) {
    if (game_socket)
        if (game_socket.readyState === WebSocket.OPEN) {
            game_socket.close();
            game_socket.onclose = function (event) {
                pong_websocket(game_data, '/ws/game/match_ai/');
            };
        }
        else if (game_socket.readyState === WebSocket.CONNECTING)
            timeoutID = setTimeout(open_match_ai_socket, 100);
}

pong_websocket(game_data, '/ws/game/game/');

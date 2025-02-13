function PongSocketStatus() {
    if (!game_socket) {
        console.error("Socket is not initialized.");
        return false;
    }

    switch (game_socket.readyState) {
        case WebSocket.CONNECTING:
            break;
        case WebSocket.OPEN:
            break;
        case WebSocket.CLOSING:
            break;
        case WebSocket.CLOSED:
            break;
        default:
            break;
    }
    return true
}

function ready(game_mode) {

    if (game_mode === 'matchmaking_1v1')
        game_mode = 'match_1v1'
    const message = JSON.stringify({mode: game_mode, action: 'player_ready'});
    game_socket.send(message);
}

function launch_game(data){
    if (data.mode === 'match_ai')
        open_match_ai_socket(game_data);
    else if (data.mode === 'matchmaking_1v1')
        open_match_socket(game_data)
    document.getElementById('lobby_css').remove();
    document.getElementById('lobby_div').remove();
    main_game(data);
}

function responsePong() {
    if (PongSocketStatus())
    {
        game_socket.onmessage = function(event)
        {
            try
            {
                let data = JSON.parse(event.data);
                if (data.action === 'searching') {
                    display_cancel_btn();
                    display_loading();
                }
                else if (data.action === 'cancel') {
                    display_research_btn("SEARCH OPPONENT");
                    stop_loading();
                }
                else if (data.action === 'find_opponent')
                {
                    change_opponent(data.opponent);
                    timeoutID = setTimeout(ready, 3000, data.mode);
                }
                else if (data.action === 'opponent_change')
                    tournament_opponent(data.players);
                else if (data.action === 'lobby_full')
                {
                    display_graph();
                    timeoutID = setTimeout(ready, 5000, 'match_tournament');
                }
                else if (data.action === 'second_match')
                    display_graph();
                else if (data.action === 'launch_second_match')
                    timeoutID = setTimeout(ready, 5000, 'match_tournament');
                else if (data.action === 'no_tournament')
                    return ;
                else if (data.action === 'cancel_lobby')
                    to_unspecified_page('game/');
                else if (data.action === 'start_game')
                    launch_game(data);
                else if (data.action === 'game_data')
                    update_racket_state(data);
                else if (data.action === 'game_end') {
                    update_racket_state(data);
                    game_ended(data);
                }
                else {
                    console.error("Unknown action received from server.");
                }
            }
            catch (e) {
                console.error("Failed to parse message data: ", e);
            }
        };
    }
}


display_research_btn("SEARCH OPPONENT");

function choose_message(str_action)
{
    let mode_name = document.getElementById("mode_name");
    let game_mode = undefined;
    if (mode_name.className === 'match_tournament')
        game_mode = "match_tournament";
    else if (mode_name.className === 'match_ai')
        game_mode = "match_ai";
    else
        game_mode = "match_1v1";
    let message = {mode: game_mode, action: str_action}
    return JSON.stringify(message);
}

function display_research_btn(content)
{
    let fuck_btn = document.getElementById("cancel_research");
    if (fuck_btn)
        fuck_btn.remove();
    let btn_play = document.createElement("button");
    btn_play.innerHTML = content;
    btn_play.className = "button"
    btn_play.id = "start_research"
    btn_play.onclick = () => {
        game_socket.send(choose_message('searching'));
    }
    if (!document.getElementById('start_research'))
        if (document.getElementById("lobby_div"))
            document.getElementById("lobby_div").appendChild(btn_play);
    change_opponent(undefined);
    if (document.getElementById("option_div"))
        if (document.getElementById("option_div").style.display === 'none')
            document.getElementById("option_div").style.display = 'flex';
}

function display_cancel_btn()
{
    let btn = document.getElementById("start_research");
    if (btn)
        btn.remove();
    let cancel_btn = document.createElement("button");
    cancel_btn.innerHTML = "CANCEL RESEARCH";
    cancel_btn.id = "cancel_research";
    cancel_btn.className = 'button';
    cancel_btn.onclick = () => {
        game_socket.send(choose_message('cancel'));
    }
    if (!document.getElementById('cancel_research'))
        document.getElementById("lobby_div").appendChild(cancel_btn);
    change_opponent(undefined);
    document.getElementById("option_div").style.display = 'none';
}

if (document.getElementById("btn_matchmaking_1v1")) {
    document.getElementById("btn_matchmaking_1v1").onclick = () => {
        let mode_name = document.getElementById("mode_name");
        mode_name.innerHTML = "MatchMaking 1v1";
        mode_name.className = "match_1v1";
        if (document.getElementById('start_research'))
            document.getElementById('start_research').remove()
        display_research_btn("SEARCH OPPONENT");
        let lobby_content = document.getElementById('lobby_content');
        fetching_html("/game/match_1v1", lobby_content);
    }
}

if (document.getElementById("btn_tournament")) {
    document.getElementById("btn_tournament").onclick = () => {
        let mode_name = document.getElementById("mode_name");
        mode_name.innerHTML = "Tournament";
        mode_name.className = "match_tournament";
        if (document.getElementById('start_research'))
            document.getElementById('start_research').remove()
        display_research_btn("SEARCH TOURNAMENT");
        let lobby_content = document.getElementById('lobby_content');
        fetching_html("/game/tournament", lobby_content);
    }
}

function display_start_local_btn()
{
    let start_local_btn = document.createElement("button");
    start_local_btn.innerHTML = "START MATCH";
    start_local_btn.id = "start_research";
    start_local_btn.className = 'button';
    start_local_btn.onclick = async () => {
            document.getElementById('lobby_div').remove();
            document.getElementById('lobby_css').remove();
            await load_script_form_fetch(local_game_script_cache);
        }
    document.getElementById("lobby_div").appendChild(start_local_btn);
}

if (document.getElementById("btn_match_local")) {
    document.getElementById("btn_match_local").onclick = () => {
        let mode_name = document.getElementById("mode_name");
        mode_name.innerHTML = "Match 1v1 local";
        mode_name.className = "match_local";
        if (document.getElementById('start_research'))
            document.getElementById('start_research').remove()
        display_start_local_btn("START MATCH");
        let lobby_content = document.getElementById('lobby_content');
        fetching_html("/game/local_match", lobby_content);
    }
}

if (document.getElementById("btn_match_ai")) {
    document.getElementById("btn_match_ai").onclick = () => {
        let mode_name = document.getElementById("mode_name");
        mode_name.innerHTML = "Match vs AI";
        mode_name.className = "match_ai";
        if (document.getElementById('start_research'))
            document.getElementById('start_research').remove()
        display_research_btn("LAUNCH GAME");
        let lobby_content = document.getElementById('lobby_content');
        fetching_html("/game/match_1v1", lobby_content);
    }
}

function match_found(opponent)
{
    if (document.getElementById("opponent_name").className === "loader")
        document.getElementById("opponent_name").className = "";
    document.getElementById("opponent_name").innerHTML = opponent;
    document.getElementById('option_div').remove();
    document.getElementById('cancel_research').remove();
    document.getElementById('mode_name').remove();
    let text = document.createElement("h3");
    text.innerHTML = "Match found !"
    let loading = document.createElement("p");
    loading.id = "loading";
    loading.className = 'loader'
    document.getElementById('lobby_div').appendChild(text);
    document.getElementById('lobby_div').appendChild(loading);
}

function change_opponent(opponent) {
    if (opponent === undefined) {
        if (document.getElementById("opponent_name")) {
            let text_opponent = document.getElementById("opponent_name");
            if (document.getElementById("start_research")) {
                text_opponent.className = "";
                text_opponent.innerHTML = "...";
            } else if (document.getElementById("cancel_research")) {
                text_opponent.className = "loader";
                text_opponent.innerHTML = "";
            }
        }
    }
    else
        match_found(opponent);
}

function tournament_opponent(players)
{
    let class_loader = document.getElementsByClassName("loader");
    let class_players = document.getElementsByClassName("player");
    let i = 0;
    while (i < class_players.length)
    {
        if (players['p' + i.toString()]) {
            class_players[i].innerHTML = players['p' + i.toString()];
            players['p' + i.toString()] = null;
        }
        else {
            class_players[i].innerHTML = '';
        }
        i++;
    }
    let u = 0;
    while (u < class_loader.length)
    {
        if (players['p' + i.toString()] !== null) {
            class_loader[u].innerHTML = players['p' + i.toString()];
        }
        i++;
        u++;
    }
    i = 0;
    while (i < class_loader.length)
    {
        if (class_loader[i].innerHTML !== '')
        {
            class_loader[i].className = 'player';
            i = -1;
        }
        i++;
    }
    i = 0;
    while (i < class_players.length)
    {
        if (class_players[i].innerHTML === '')
        {
            class_players[i].className = 'loader';
            i = -1;
        }
        i++;
    }
}

function display_loading()
{
    let class_players = document.getElementsByClassName("player");
    if (class_players.length === 0)
        return
    let i = 0;
    while (i < class_players.length)
    {
        if (class_players[i].innerHTML === '...') {
            class_players[i].innerHTML = '';
            class_players[i].className = 'loader';
            i = 0;
        }
        i++;
    }
}

function stop_loading(){
    let lobby_content = document.getElementById('lobby_content');

    let mode = document.getElementById('mode_name');
    if (mode.innerHTML === "Tournament")
        fetching_html('/game/tournament', lobby_content);
    else
        fetching_html('/game/match_1v1', lobby_content);
}

function display_graph()
{
    let lobby_div = document.getElementById('lobby_div');

    fetching_html('/game/tournament/bracket_graph',lobby_div)
}
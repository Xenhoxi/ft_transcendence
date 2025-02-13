function navigate(link, replace = false) {
    if (link[0] !== '/') link = '/' + link;
    const pageState = { page: link };

    console.log(pageState, replace)
    if (replace) {
        history.replaceState(pageState, null, link);
    } else {
        history.pushState(pageState, null, link);
    }
}


function change_page_name(page) {
    if (page === 'game/canvas/')
        return 'game';
    else if (page === 'logout_btn/')
        return '';
    else
        return page.replace(/^\/+/, '');  // remove leading slashes if any
}


async function back_to_unspecified_page(page) {
    let div_content = document.getElementById('content');

    let error = await fetching_html_post(page, div_content)
    if (error === 410)
    {
        history.replaceState(page, null, '/game');
        page = '/game';
    }
    else if (error === 401 || error === 403)
    {
        history.replaceState(page, null, '/');
        page = '/'
    }
    reset_script(page);
    await reload_scripts(page, 0);
}


window.onpopstate = (function(event) {

    if (event.state && event.state.page) {
        back_to_unspecified_page(event.state.page);
    } else {
        back_to_unspecified_page(window.location.pathname);
    }
});

function open_lobby_socket(game_data)
{
    if (game_socket)
        if (game_socket.readyState === WebSocket.OPEN) {
            game_socket.close();
            game_socket.onclose = function (event){
                if (game_data.interid !== undefined)
                    clearInterval(game_data.interid);
                pong_websocket(game_data, '/ws/game/game/');
            }
        }
        else if (game_socket.readyState === WebSocket.CONNECTING)
            timeoutID = setTimeout(open_lobby_socket, 100);
    else
    {
        if (game_data.interid !== undefined)
            clearInterval(game_data.interid);
        pong_websocket(game_data, '/ws/game/game/');
    }
    game_data.my_racket = undefined;
    game_data.opponent_racket = undefined;
}

async function to_unspecified_page(page) {
	let div_content = document.getElementById('content');	
	await fetching_html(page, div_content);
	page = change_page_name(page);

	reset_script('/' + page);
    await reload_scripts('/' + page, 0);
	if (page.match('game')) {
		open_lobby_socket(game_data);
	} else {
        if (game_socket) game_socket.close();
	}
    navigate('/' + page);
}


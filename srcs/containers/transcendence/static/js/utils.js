
let game_socket;
let socket;
let timeoutID;
let moveback = window.location.pathname

if (window.location.pathname !== '/')
{
    navigate_utils('/');
}

let game_script_cache = fetch_scripts('game/scripts/', 'game_script');
let local_game_script_cache = fetch_scripts('game/scripts/', 'local_game_script');
let local_game_class_script_cache = fetch_scripts('game/scripts/', 'local_game_class_script');
let game_class_script_cache = fetch_scripts('game/scripts/', 'game_class_script');
let authentication_script_cache = fetch_scripts('game/scripts/', 'auth_script');
let navbar_script_cache = fetch_scripts('game/scripts/', 'navbar_script');
let navigation_script_cache = fetch_scripts('game/scripts/', 'navigation_script');
let profile_script_cache = fetch_scripts('game/scripts/', 'profile_script');
let ws_script_cache = fetch_scripts('game/scripts', 'ws_script');
let social_script_cache = fetch_scripts('game/scripts', 'social_script');
let twofa_script_cache = fetch_scripts('game/scripts', '2fa_script');

let game_data = {
	my_racket: undefined,
	opponent_racket: undefined,
}

let tournament_data = {
	racket_left: undefined,
	racket_right: undefined,
	ballon: undefined,
}

if (moveback !== '/')
{
    navigate_utils(moveback);
}
async function fetch_scripts(url, class_name)
{
    let script_div = document.createElement('div');
    await fetching_html(url, script_div);
    let script_list = script_div.getElementsByClassName(class_name);
    return (script_list);
}

async function reload_scripts(page)
{
    if (page !== '/' && page !== '/account/redirect/checker' && page !== '/account/redirect/login')
    {
        await always_on_script();
        if (page.match('/social'))
            await load_script_form_fetch(social_script_cache);
        else if (page.match('/profile'))
            await load_script_form_fetch(profile_script_cache);
        else if (page.match('/game'))
            await load_script_form_fetch(game_script_cache);
		else if (page.match('/account'))
			await load_script_form_fetch(twofa_script_cache);
    }
    else {
        await load_script_form_fetch(authentication_script_cache);
		await load_script_form_fetch(navigation_script_cache);
        await load_script_form_fetch(twofa_script_cache);
    }
}

function reset_script(page)
{
    let script_list = ['game_script', 'social_script', 'navbar_script', 'profile_script', 'auth_script', 'local_game_script']

    for(let a = 0; a <= script_list.length; a++)
    {
        if (document.getElementsByClassName(script_list[a]))
            delete_script_by_class_name(script_list[a]);
    }
    if (page === '/')
           delete_script_by_class_name('ws_script');
}


async function always_on_script()
{
    let script_list = ['navigation_script', 'game_class_script', 'ws_script', '2fa_script', 'local_game_class_script']
    let script_list_cache = [navigation_script_cache, game_class_script_cache, ws_script_cache, twofa_script_cache, local_game_class_script_cache]

    for (let a = 0; a <= 4; a++)
    {
        if (document.getElementsByClassName(script_list[a]).length === 0)
                await  load_script_form_fetch(script_list_cache[a]);

    }
    if (document.getElementsByClassName('navbar').length > 0)
        await load_script_form_fetch(navbar_script_cache);
}


async function load_script_form_fetch(cache)
{
    let list_script = await cache;
    for (let i = 0; i < list_script.length; i++)
    {
        const newScript = document.createElement('script');
        if(list_script[i].className)
            newScript.className = list_script[i].className;
        if (list_script[i].src)
            newScript.src = list_script[i].src;
        else
            newScript.innerHTML = list_script[i].innerHTML;
        document.body.appendChild(newScript);

    }
}

async function fetching_html_add(link, element)
{
    try
    {
        const response = await fetch(link)
        if (!response.ok)
            throw new TypeError("HTML fetch failed");
        let bidule = await response.text();
        element.innerHTML += bidule;
    }
    catch (error)
    {
        console.log(error);
    }
}

async function fetching_html(link, element)
{
    try
    {
        const response = await fetch(link);
        if (!response.ok)
            throw new TypeError("HTML fetch failed");
        element.innerHTML = await response.text();
    }
    catch (error)
    {
        console.log(error);
    }
}

async function fetching_html_post(link, element)
{
    if (!link.endsWith('/'))
        link += '/';
    console.log(link);
    try
    {
        const response = await fetch(link,{
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({navigation: 'backward_forward'})
        });
        if (!response.ok)
        {
            if (response.status === 401)
                return 401;
            else if (response.status === 410)
                return 410;
            else if (response.status === 403)
                return 403
            throw new TypeError("HTML fetch failed");
        }
        element.innerHTML = await response.text();
    }
    catch (error)
    {
        console.log(error);
    }
}



function delete_script_by_class_name(name)
{
    const list_script = document.getElementsByClassName(name);
    for (let i = list_script.length - 1; i >= 0; i--) {
        list_script[i].remove();
    }
}

function navigate_utils(link, replace = false) {
    if (link[0] !== '/') link = '/' + link;
    const pageState = { page: link };

    if (replace) {
        history.replaceState(pageState, null, link);
    } else {
        history.pushState(pageState, null, link);
    }
}

function pong_websocket(game_data, url) {
    if (!game_socket || game_socket.readyState === WebSocket.CLOSED) {

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const websocketUrl = `${protocol}//${window.location.host}${url}`;
        game_socket = new WebSocket(websocketUrl);

        game_socket.onopen = function (e) {
            responsePong();
            const message = JSON.stringify({mode: "match_tournament", action: 'is_tournament'});
            game_socket.send(message);
        };

        game_socket.onclose = function (event) {
        };

        game_socket.onerror = function (error) {
            console.log(`[error] ${error.message}`);
        };
    }
    return game_socket;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

reload_scripts(window.location.pathname);

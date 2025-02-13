
document.getElementById('social-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('searchbar').value;
    const message = JSON.stringify({ action: "friend_request", "username": username });
    socket.send(message);
    display_popup_green('Friend request sent !');
});

document.getElementById('friends').addEventListener('click', function(event) {
    event.preventDefault();
        let list = document.getElementById('ListContainer');
    list.className = "FriendListContainer";
    const message = JSON.stringify({action: "friend_list"});
    socket.send(message);
});

document.getElementById('request').addEventListener('click', function(event) {
    event.preventDefault();
        let list = document.getElementById('ListContainer');
        list.className = "RequestListContainer";
    const message = JSON.stringify({action: "request_list"});
    socket.send(message);
});

document.getElementById('pending').addEventListener('click', function(event) {
    event.preventDefault();
    let list = document.getElementById('ListContainer');
    list.className = "PendingListContainer";
    const message = JSON.stringify({action: "pending_list"});
    socket.send(message);
});

function request_friend_list() {
    if (window.location.pathname === '/social') {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ 'action': 'friend_list' }));
        } else {
            console.error("WebSocket is not open. Unable to send request.");
        }
    } else {
        console.log("Pathname is not '/social/', request not sent.");
    }
}

function checkSocketStatus() {
    if (!socket) {
        console.error("Socket is not initialized.");
        return;
    }

    switch (socket.readyState) {
        case WebSocket.CONNECTING:
            break;
        case WebSocket.OPEN:
            request_friend_list();
            break;
        case WebSocket.CLOSING:
            break;
        case WebSocket.CLOSED:
            break;
        default:
            console.error("Unknown WebSocket state.");
            break;
    }
}

async function friend_profile_request(data)
{
    navigate('/');
    let div_content = document.getElementById('profile_popup_content');
    await fetching_html_add(`profile/?target_name=${encodeURIComponent(data.target)}`, div_content)
    document.getElementById("profile_popup").classList.add('on')


    if (document.getElementById('normal_games_btn'))
    {
        document.getElementById('normal_games_btn').addEventListener('click', () =>{
            navigate('/')
            fetching_html(`profile/normal_games?target_name=${encodeURIComponent(data.target)}`, document.getElementById('full_history'))
            navigate('social/', true);
        })
    }

    if (document.getElementById('tournament_games_btn'))
    {
        document.getElementById('tournament_games_btn').addEventListener('click', () =>{
            navigate('/')
            fetching_html(`profile/tournament_games?target_name=${encodeURIComponent(data.target)}`, document.getElementById('full_history'))
            navigate('social/', true);
        })
    }
    await navigate('social/', true);
}



document.getElementById('profile_popup').addEventListener('click', function(e){
    if (!document.getElementById('profile_popup_content').contains(e.target)
        || document.getElementById('close-friend-profile').contains(e.target)){
        document.getElementById('profile_page').remove();
        document.getElementById('profile_popup').classList.remove('on');
    }
})

window.addEventListener('keydown', function (e){
    if (e.key === 'Escape')
    {
        if (document.getElementsByClassName('profile_popup.on'))
        {
            document.getElementById('profile_page').remove();
            document.getElementById('profile_popup').classList.remove('on');
        }
    }
})

function response_choice(data)
{
    let action_list = ['friend_list', 'request_list', 'pending_list', 'remove_friend',
        'accept_friend_request', 'cancel_deny_request', 'create_request', 'view_profile', 'error'];

    let action_list_function = [parse_friend_list, parse_request_list, parse_pending_list, remove_friend_request,
        accept_friend_request, cancel_deny_request, create_request, friend_profile_request, display_popup];

    for (let a = 0; a <= action_list.length; a++)
    {
        if (data.action === action_list[a])
        {
            action_list_function[a](data);
            return ;
        }
    }
    console.error("Unknown action received from server.");
}


function response() {
    checkSocketStatus();

    socket.onmessage = function(event)
    {
        try
        {
            let data = JSON.parse(event.data);
            response_choice(data);
        }
        catch (e)
        {
            console.error("Failed to parse message data: ", e);
        }
    };
}

response();

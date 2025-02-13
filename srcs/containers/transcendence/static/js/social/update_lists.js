
function remove_friend_request(data)
{
    if (document.getElementById(data.target))
        document.getElementById(data.target).remove();
}

function accept_friend_request(data) {
    if (document.getElementsByClassName("RequestListContainer"))
        if (document.getElementById(data.target))
            document.getElementById(data.target).remove();
    if (document.getElementsByClassName("FriendListContainer")[0]) {
        let listItem = createListItem(data.target, data.is_connected, data.is_playing);
        listItem.id = data.target;
        addButtons(listItem, data.target, "friend_list");
        document.getElementsByClassName('FriendListContainer')[0].appendChild(listItem);
    }
}

function cancel_deny_request(data) {
    if (document.getElementsByClassName("PendingListContainer"))
        if (document.getElementById(data.target))
            document.getElementById(data.target).remove();
    if (document.getElementsByClassName("RequestListContainer"))
        if (document.getElementById(data.target))
            document.getElementById(data.target).remove();
}

function create_request(data)
{
    if (data.who === 'requester')
    {
        if (document.getElementsByClassName("RequestListContainer")[0]) {
            let listItem = createListItem(data.target, data.is_connected, data.is_playing);
            listItem.id = data.target;
            addButtons(listItem, data.target, "request_list");
            document.getElementsByClassName('RequestListContainer')[0].appendChild(listItem);
        }
    }
    if (data.who === 'pending') {
        if (document.getElementsByClassName("PendingListContainer")[0]) {
            let PendingItem = createListItem(data.target, data.is_connected, data.is_playing);
            PendingItem.id = data.target;
            addButtons(PendingItem, data.target, "pending_list");
            document.getElementsByClassName('PendingListContainer')[0].appendChild(PendingItem);
        }
    }
}

function display_popup(data)
{
    if (document.getElementById("snackbar")) {
        let snackbar = document.getElementById("snackbar")
        snackbar.className = "snackbar_visibility_show";
        snackbar.innerHTML = data.error;
        snackbar.style.backgroundColor = 'red'
        setTimeout(function (){
            snackbar.className = "snackbar_visibility"
        }, 5000)
    }
}

function display_popup_green(str)
{
    if (document.getElementById("snackbar")) {
        let snackbar = document.getElementById("snackbar")
        snackbar.className = "snackbar_visibility_show";
        snackbar.innerHTML = str;
        snackbar.style.backgroundColor = 'green'
        setTimeout(function (){
            snackbar.className = "snackbar_visibility"
        }, 5000)
    }
}


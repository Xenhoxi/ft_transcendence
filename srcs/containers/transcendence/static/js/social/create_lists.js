
function clearAndCheckContainer(containerId) {
    let container = document.getElementById(containerId);
    if (!container) {
        console.error(`${containerId} not found.`);
        return null;
    }
    container.innerHTML = '';
    return container;
}

function createListItem(name, isConnected, isPlaying) {
    let listItem = document.createElement('li');
    listItem.className = 'item';

    let nameElement = document.createElement('span');
    nameElement.className = 'name';
    nameElement.textContent = name;

    let connectionStatus = document.createElement('span');
    connectionStatus.className = 'connection-status';
    if (isConnected && !isPlaying)
        connectionStatus.classList.add('connected');
    else {
        if (isPlaying)
            connectionStatus.classList.add('is_playing');
        else
            connectionStatus.classList.add('disconnected');
    }
    listItem.appendChild(connectionStatus);
    listItem.appendChild(nameElement);
    return listItem;
}

function addButtons(listItem, name, listType) {
    if (listType === 'friend_list') {
        let inviteButton = document.createElement('button');
        inviteButton.className = 'invite-button';
        inviteButton.textContent = 'Invite to game';
        inviteButton.addEventListener('click', function() {
            const message = JSON.stringify({ action: "invite_to_game", "target": name });
    		socket.send(message);
            display_popup_green('Friend invite to your game ! No jk it does not work');
        });

        let removeButton = document.createElement('button');
        removeButton.className = 'remove-button';
        removeButton.textContent = 'Remove friend';
        removeButton.addEventListener('click', function() {
            const message = JSON.stringify({ action: "remove_friend", "target": name });
    		socket.send(message);
            display_popup_green('Friend removed from your list !');
        });

        let view_profile_button = document.createElement('button');
        view_profile_button.className = 'view-button';
        view_profile_button.textContent = 'view profile';
        view_profile_button.addEventListener('click', function() {
            const message = JSON.stringify({ action: "view_profile", "target": name });
    		socket.send(message);
        });

        listItem.appendChild(inviteButton);
        listItem.appendChild(removeButton);
        listItem.appendChild(view_profile_button)
    } else if (listType === 'request_list') {
        let acceptButton = document.createElement('button');
        acceptButton.className = 'accept-button';
        acceptButton.textContent = 'Accept';
        acceptButton.addEventListener('click', function() {
            const message = JSON.stringify({ action: "accept_friend_request", "target": name });
    		socket.send(message);
            display_popup_green('Friend request accepted !');
        });

        let denyButton = document.createElement('button');
        denyButton.className = 'deny-button';
        denyButton.textContent = 'Deny';
        denyButton.addEventListener('click', function() {
			const message = JSON.stringify({ action: "cancel_deny_request", "target": name });
    		socket.send(message);
            display_popup_green('Friend request denied !');
        });

        listItem.appendChild(acceptButton);
        listItem.appendChild(denyButton);
    } else if (listType === 'pending_list') {
        let cancelButton = document.createElement('button');
        cancelButton.className = 'cancel-button';
        cancelButton.textContent = 'Cancel';
        cancelButton.addEventListener('click', function() {
            const message = JSON.stringify({ action: "cancel_deny_request", "target": name });
    		socket.send(message);
            display_popup_green('Friend request canceled !');
        });

        listItem.appendChild(cancelButton);
    }
}

function parseList(data, listType, containerId) {
    let items;
    if (listType === 'friend_list') {
        items = data.friend_list.friends;
    } else if (listType === 'request_list') {
        items = data.request_list.request;
    } else if (listType === 'pending_list') {
        items = data.pending_list.pending;
    }

    let container = clearAndCheckContainer(containerId);
    if (!container) return;

    for (let item in items) {
        if (items.hasOwnProperty(item)) {
            let listItem = createListItem(item, items[item].is_connected, items[item].is_playing);
            listItem.id = item;
            addButtons(listItem, item, listType);
            container.appendChild(listItem);
        }
    }
}

function parse_friend_list(data) {
    parseList(data, 'friend_list', 'ListContainer');
}

function parse_request_list(data) {
    parseList(data, 'request_list', 'ListContainer');
}

function parse_pending_list(data) {
    parseList(data, 'pending_list', 'ListContainer');
}


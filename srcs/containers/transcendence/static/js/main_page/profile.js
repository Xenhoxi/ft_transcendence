
if (document.getElementById('profile_form'))
{
    document.getElementById('profile_form').addEventListener('submit', function (event) {
        event.preventDefault();
        update_profile(this);
    })
    document.getElementById('imglabel').addEventListener('mouseenter',() =>{
        document.getElementById('imglabel').classList.add('hover_img')
    })

    document.getElementById('imglabel').addEventListener('mouseleave',() =>{
        document.getElementById('imglabel').classList.remove('hover_img');
    })
}

if (document.getElementById('normal_games_btn'))
{
    document.getElementById('normal_games_btn').addEventListener('click', () =>{
        fetching_html('/profile/normal_games/', document.getElementById('full_history'))
    })
}

if (document.getElementById('tournament_games_btn'))
{
    document.getElementById('tournament_games_btn').addEventListener('click', () =>{
        fetching_html('/profile/tournament_games/', document.getElementById('full_history'))
    })
}


async function update_profile(value)
{
    try
    {
        navigate('/')
        const formdata = new FormData(value);
        let response = await fetch('profile/modify/',{
            method: 'POST',
            body: formdata,
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            credentials: 'same-origin',
        });
        if (!response.ok)
            throw new TypeError(`Server error: ${errorText}`);
        let success_error = await response.json();
        if(success_error.success === 'Error')
            throw new TypeError('something went wrong');
        if (success_error.success === 'success' && success_error.password === 'yes')
        {
            socket.close();
            await to_unspecified_page('logout_btn/');
        }
        else if (success_error.success === 'success' && success_error.password === 'no')
        {
            socket.send(JSON.stringify({'action': 'update_name', 'username': success_error.username}));
            await to_unspecified_page('profile/');
        }
        else
            display_popup(success_error.error)
    }
    catch (error)
    {
        console.log(error);
    }
}

function display_popup(data)
{
    if (document.getElementById("snackbar")) {
        let snackbar = document.getElementById("snackbar")
        snackbar.className = "snackbar_visibility_show";
        snackbar.innerHTML = data;
        setTimeout(function (){
            snackbar.className = "snackbar_visibility"
        }, 5000)
    }
}

if (document.getElementById('player_username'))
{
    const username = document.getElementById('player_username').textContent;
    if (username.endsWith('_42')) {
        const editProfileButton = document.getElementById('edit_profile');
        if (editProfileButton) {
            editProfileButton.style.display = 'none';
        }
    } else {
        if (document.getElementById('edit_profile')) {
            document.getElementById('edit_profile').addEventListener('click', () => {
                to_unspecified_page('/profile/modify');
            });
        }
    }
}

if (document.getElementById('setup_2fa')) {
	document.getElementById('setup_2fa').addEventListener('click', function(event) {
	    to_unspecified_page('/account/redirect/setup')
    })
}

if (document.getElementById('delete_2fa')) {
    document.getElementById('delete_2fa').addEventListener('click', function(event) {
        event.preventDefault();

        if (confirm('Are you sure you want to delete Two-Factor Authentication?')) {
            fetch('/account/delete_2fa/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({}),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to delete Two-Factor Authentication.');
            });
        }
    });
}


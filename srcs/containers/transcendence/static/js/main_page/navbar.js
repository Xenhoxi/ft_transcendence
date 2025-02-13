if (document.getElementById("logout"))
    document.getElementById("logout").addEventListener('click', async function(event){
        event.preventDefault();
        socket.close();
        await to_unspecified_page('/logout_btn');
        to_unspecified_page('/');
    })

if (document.getElementById('game'))
    document.getElementById('game').addEventListener('click', function(event){
        event.preventDefault();
        if (timeoutID)
        {
            clearTimeout(timeoutID);
            timeoutID = undefined;
        }
        to_unspecified_page('/game');
    })

if (document.getElementById('profile'))
    document.getElementById('profile').addEventListener('click', function(event){
    event.preventDefault();
    to_unspecified_page('/profile');
    })

if (document.getElementById('social'))
    document.getElementById('social').addEventListener('click', async function(event){
    event.preventDefault();
    await to_unspecified_page('/social');
    })

// if (document.getElementById("register"))
// 	document.getElementById("register").addEventListener("click", async (e) => {
// 		document.getElementById("login_div").remove();
// 		await fetching_html_add("register_tentative/", document.getElementById('content'));
// 		await reload_scripts('/');
// })
//
// if (document.getElementById("login_button"))
// 	document.getElementById("login_button").addEventListener("click", async (e) => {
// 		document.getElementById("register_div").remove();
// 		await fetching_html_add("account/redirect/login", document.getElementById('content'));
// 		await reload_scripts('/');
// })
//
// if (document.getElementById("registration"))
// 	document.getElementById("registration").addEventListener("submit", async (e) => {
// 		e.preventDefault();
// 		await send_login_form(e.target, 'register_session/');
// })

async function load_sign_up()
{
    let fetch_div = document.getElementById('login_div');

    await fetching_html('register_session/', fetch_div);
    document.getElementById('register-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    await send_login_form(event.target, 'register_session/');
    })
}

async function load_sign_in()
{
    let fetch_div = document.getElementById('login_div');

    await fetching_html('login_session/', fetch_div);
}

async function send_login_form(value, url)
{
    const errorMessageDiv = document.getElementById('error-message');
    try
    {
        const formdata = new FormData(value);
        let response = await fetch(url, {
            method: 'POST',
            body: formdata,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
        })
        if (!response.ok)
                throw new TypeError("Login fail");
        let test = await response.json()
        if (!test.success)
              errorMessageDiv.textContent = test.error || 'Login failed. Please try again.';
        else
            await to_unspecified_page(test.redirect_url)
    }
    catch (error)
    {
        console.log(error);
    }

}
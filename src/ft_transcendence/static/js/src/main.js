let canevas = document.getElementById("canv");
let canvcont = canevas.getContext("2d");

let img1 = new twix(0, 300, "static/js/img/raquetteR.png", 1000);
let img2 = new twix(2040 - 74, 300, "static/js/img/raquetteL.png", 1000);
let ballon = new balle(1020, 540, "static/js/img/maltesers.png", 500);

let oldtime = Date.now();
let ms;
let game_begin = 0;


function main()
{
    document.addEventListener("keyup", lowkeyup);
    document.addEventListener("keydown", lowkeydown);
    const interid = setInterval(rien, 1000/60);
}

function drawwin(img1, img2)
{
    let text;
    canvcont.font = "48px serif";
    if (img1.score >= 10)
        text = "WINNER is player 1";
    else
        text = "WINNER is player 2";
    console.log(text);
    canvcont.fillStyle = "Black";
    canvcont.fillText(text, (canevas.clientWidth / 2.5), canevas.clientHeight / 2);
}

function drawscore()
{
    canvcont.font = "48px serif";
    let text = img1.score;
    let text2 = img2.score;
    canvcont.fillStyle = "Black";
    canvcont.fillText(text, 510, 50);
    canvcont.fillText(text2, 1530, 50);
}

function lowkeydown(key){

    console.log(key.code);
    if (key.code == "ArrowUp")
        img2.up = true;
    else if (key.code == "ArrowDown")
        img2.down = true;
    if (key.code == "KeyW")
        img1.up = true;
    else if (key.code == "KeyS")
        img1.down = true;
    if (key.code == "Space" && (img1.score == 3 || img2.score == 3 || game_begin == 0))
    {
        game_begin = 2;
        reseting();
    }
}

function lowkeyup(key){

    console.log(key.code);
    if (key.code == "ArrowUp")
        img2.up = false;
    else if (key.code == "ArrowDown")
        img2.down = false;
    if (key.code == "KeyW")
        img1.up = false;
    else if (key.code == "KeyS")
        img1.down = false;
}


function rien()
{
    let newtime = Date.now();
    ms = (newtime - oldtime) / 1000;
    if (game_begin == 2)
        countdown(ms, newtime);
    else if (game_begin == 1)
    {  
        oldtime = newtime;
        if (img1.score < 3 && img2.score < 3 && game_begin == 1)
        {
            
            img2.moving(ms);
            img1.moving(ms);
            ballon.move(ms);
            canvcont.clearRect(0, 0, canevas.clientWidth, canevas.clientHeight);
            ballon.drawing(canvcont);
            img2.drawing(canvcont);
            img1.drawing(canvcont);
        }
        else if (img1.score >= 3 || img2.score >= 3)
            drawwin(img1, img2);
        drawscore();
    }  
    if (game_begin == 0)
            oldtime = newtime;
}
        
function reseting()
{
    ballon.x = 1020;
    ballon.y = 540;
    img2.reset();
    ballon.resetballs();
    img1.reset();
}

function countdown(ms, newtime)
{
    let countdown;
    if (ms < 4)
    {
        countdown = 3 - Math.floor(ms);
        canvcont.font = "300px serif";
        canvcont.fillStyle = "Black";
        canvcont.clearRect(0, 0, canevas.clientWidth, canevas.clientHeight);
        ballon.drawing(canvcont);
        img2.drawing(canvcont);
        img1.drawing(canvcont);
        canvcont.fillText(countdown.toString(), (canevas.clientWidth / 2) - 100, (canevas.clientHeight / 2) + 150);
        console.log(countdown);
    }
    else
    {
        oldtime = newtime;
        game_begin = 1;
    }
}

main();


function local_main()
{
    let canevas = document.createElement("canvas");
    canevas.id = "canv";
    canevas.height = 1080;
    canevas.width = 2040;
    canevas.style = "border: 4px solid black";
    canevas.style.backgroundColor = 'white';
    document.getElementById("gamecanvas").appendChild(canevas);

    let local_utils = {
        canvcont: canevas.getContext("2d"),

        fontsize: 80 / canevas.width,
        oldtime: Date.now(),
        ms: 0,
        game_begin: 0,
    }
    let racket_left = new local_racket(0, canevas.height / 2 - 116, "../static/js/images/raquetteR.png", 1000, canevas);
    let racket_right = new local_racket(canevas.width - 74, canevas.height / 2 - 116, "../static/js/images/raquetteL.png", 1000, canevas);
    let ball = new local_ball(canevas.width / 2, canevas.height / 2, "../static/js/images/maltesers.png", 500, canevas);

    document.addEventListener("keyup",function (event){local_lowkeyup(event, racket_left, racket_right)});
    document.addEventListener("keydown", function (event){local_lowkeydown(event, racket_left, racket_right, ball, local_utils, canevas)});
    const interid = setInterval(local_infinite_game_loop, 1000/60, racket_left, racket_right, ball, canevas, local_utils);
}

function local_drawwin(racket_left, racket_right, canevas, utils)
{
    let text;
    let actualfontsize = utils.fontsize * canevas.width;
    utils.canvcont.font = (actualfontsize) + "px serif";
    if (racket_left.score >= 3)
        text = "WINNER is player 1";
    else
        text = "WINNER is player 2";
    utils.canvcont.fillStyle = "Black";
    utils.canvcont.fillText(text, (canevas.width / 3.2), canevas.height / 2);
}

function local_drawscore(racket_left, racket_right, canevas, utils)
{
    let actualfontsize = utils.fontsize * canevas.width;

    utils.canvcont.font = (actualfontsize) + "px serif";
    utils.canvcont.fillStyle = "Black";
    utils.canvcont.fillText(racket_left.score, canevas.width / 4, actualfontsize);
    utils.canvcont.fillText(racket_right.score, (canevas.width / 4) * 3, actualfontsize);
}

function local_lowkeydown(key, racket_left, racket_right, ballon, utils, canevas){

    if (key.code === "ArrowUp")
        racket_right.up = true;
    else if (key.code === "ArrowDown")
        racket_right.down = true;
    if (key.code === "KeyW")
        racket_left.up = true;
    else if (key.code === "KeyS")
        racket_left.down = true;
    if (key.code === "Space" && (racket_left.score === 3 || racket_right.score === 3 || utils.game_begin === 0))
    {
        utils.game_begin = 2;
        local_reseting(racket_left, racket_right, ballon, canevas);
    }
}

function local_lowkeyup(key, racket_left, racket_right){

    if (key.code === "ArrowUp")
        racket_right.up = false;
    else if (key.code === "ArrowDown")
        racket_right.down = false;
    if (key.code === "KeyW")
        racket_left.up = false;
    else if (key.code === "KeyS")
        racket_left.down = false;
}


function local_infinite_game_loop(racket_left, racket_right, ballon, canevas, utils)
{
    let newtime = Date.now();
    utils.ms = (newtime - utils.oldtime) / 1000;
    if (utils.game_begin === 2)
        local_countdown(newtime, racket_left, racket_right, ballon, utils, canevas);
    else if (utils.game_begin === 1)
    {
        utils.oldtime = newtime;
        if (racket_left.score < 3 && racket_right.score < 3 && utils.game_begin === 1)
        {

            racket_right.local_moving(utils.ms);
            racket_left.local_moving(utils.ms);
            ballon.local_move(utils.ms, racket_left, racket_right);
            utils.canvcont.clearRect(0, 0, canevas.width, canevas.height);
            ballon.local_drawing(utils.canvcont);
            racket_right.local_drawing(utils.canvcont);
            racket_left.local_drawing(utils.canvcont);
        }
        else if (racket_left.score >= 3 || racket_right.score >= 3)
            local_drawwin(racket_left, racket_right, canevas, utils);
        local_drawscore(racket_left, racket_right, canevas, utils);
    }
    if (utils.game_begin === 0)
            utils.oldtime = newtime;
}

function local_reseting(racket_left, racket_right, ballon, canevas)
{
    ballon.x = canevas.width / 2;
    ballon.y = canevas.height / 2;
    racket_right.local_reset();
    ballon.local_resetballs(racket_left, racket_right);
    racket_left.local_reset();
}

function local_countdown(newtime, racket_left, racket_right, ballon, utils, canevas)
{
    let countdown;
    let actualfontsize = utils.fontsize * canevas.width;
    if (utils.ms < 4)
    {
        countdown = 3 - Math.floor(utils.ms);
        utils.canvcont.font = (actualfontsize * 3) + "px serif";
        utils.canvcont.fillStyle = "Black";
        utils.canvcont.clearRect(0, 0, canevas.width, canevas.height);
        ballon.local_drawing(utils.canvcont);
        racket_right.local_drawing(utils.canvcont);
        racket_left.local_drawing(utils.canvcont);
        utils.canvcont.fillText(countdown.toString(),(canevas.width / 2) - 40, (canevas.height / 2) + 40);
    }
    else
    {
        utils.oldtime = newtime;
        utils.game_begin = 1;
    }
}

local_main();
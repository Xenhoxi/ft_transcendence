/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.js                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ljerinec <ljerinec@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/05/21 11:45:05 by ljerinec          #+#    #+#             */
/*   Updated: 2024/05/27 13:34:14 by ljerinec         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

let canvas = document.getElementById("game");
let ctx = canvas.getContext("2d");
let previous = Date.now();
let interval;

let padLeft;
let padRight;
let ball;

function main()
{
	load();
	console.log("Loaded !");
	interval = setInterval(run, 1000/60);
}

function run()
{
	let now = Date.now();
	let dt = (now - previous) / 1000;
	previous = now;
	update(dt);
	ctx.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
	draw(ctx);
}

function load()
{
	document.addEventListener("keydown", keyPressed, false);
	document.addEventListener("keyup", keyReleased, false);
	padLeft = new Pad("./img/pad.png", 0, (canvas.clientHeight / 2) - (120 / 2));
	padRight = new Pad("./img/pad.png", canvas.clientWidth - 20, (canvas.clientHeight / 2) - (120 / 2));
	ball = new Ball("./img/ball.png", canvas.clientWidth / 2 - 7, canvas.clientHeight / 2 - 7);
}

function update(dt)
{
	if (keyW)
		padLeft.goUp(dt);
	if (KeyS)
		padLeft.goDown(dt);
	if (KeyO)
		padRight.goUp(dt);
	if (KeyL)
		padRight.goDown(dt);
	ball.update(dt);
}

function draw(ctx)
{
	padLeft.draw(ctx);
	padRight.draw(ctx);
	ball.draw(ctx);
}

main();
/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ball.js                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ljerinec <ljerinec@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/05/23 10:13:48 by ljerinec          #+#    #+#             */
/*   Updated: 2024/05/27 10:43:12 by ljerinec         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

class Ball
{
	constructor(src, x, y)
	{
		this.img = new Image();
		this.img.src = src;
		this.x = x;
		this.y = y;
		this.vx = -200;
		this.vy = 50;
		this.vector = 1;
	}

	update(dt)
	{
		this.x += this.vx * dt;
		this.y += this.vy * dt;
		// console.log(canvas.clientWidth);
		if (this.x > canvas.clientWidth || this.x + this.img.width < 0)
			this.reset();
		if (this.y + this.img.height > canvas.height || this.y < 0)
			this.vy *= -1;
		if (padLeft.gotHit(this.x, this.y) === true || padRight.gotHit(this.x, this.y) === true)
			this.vx *= -1;
	}

	draw(ctx)
	{
		ctx.drawImage(this.img, this.x, this.y);
	}

	reset()
	{
		this.x = canvas.clientWidth / 2 - this.img.width / 2;
		this.y = canvas.clientHeight / 2 - this.img.height / 2;
	}
}
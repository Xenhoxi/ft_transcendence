/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ball.js                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ljerinec <ljerinec@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/05/23 10:13:48 by ljerinec          #+#    #+#             */
/*   Updated: 2024/05/27 13:46:52 by ljerinec         ###   ########.fr       */
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
		this.vx = -400;
		this.vy = 50;
	}

	update(dt)
	{
		this.x += this.vx * dt;
		this.y += this.vy * dt;
		if (this.x > canvas.clientWidth || this.x + this.img.width < 0)
			this.reset();
		if (this.y + this.img.height > canvas.height || this.y < 0)
			this.vy *= -1;
		if (padLeft.gotHit(this.x, this.y, this.img.width, this.img.height) === true)
		{
			let angle = padLeft.getImpactPoint(this.y) * (Math.PI / 4);
			let speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
			this.vx = speed * Math.cos(angle);
			this.vy = speed * Math.sin(angle);
		}
		if (padRight.gotHit(this.x, this.y, this.img.width, this.img.height) === true)
		{
			let angle = padLeft.getImpactPoint(this.y) * (Math.PI / 4);
			let speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
			this.vx = speed * Math.cos(angle);
			this.vy = speed * Math.sin(angle);
		}
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
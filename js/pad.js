/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pad.js                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ljerinec <ljerinec@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/05/23 09:34:04 by ljerinec          #+#    #+#             */
/*   Updated: 2024/05/23 10:17:56 by ljerinec         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

class Pad
{
	constructor(src, x , y)
	{
		this.x = x;
		this.y = y;
		this.img = new Image();
		this.img.src = src;
		this.speed = 350
	}

	draw(ctx) {
		ctx.drawImage(this.img, this.x, this.y);
	}

	goUp(dt) {
		if (this.y - (this.speed * dt) >= 0)
			this.y -= (this.speed * dt);
	}

	goDown(dt) {
		if (this.y + (this.speed * dt) <= canvas.clientHeight - 120)
			this.y += (this.speed * dt);
	}
}
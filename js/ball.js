/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ball.js                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ljerinec <ljerinec@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/05/23 10:13:48 by ljerinec          #+#    #+#             */
/*   Updated: 2024/05/23 11:49:08 by ljerinec         ###   ########.fr       */
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
	}

	update(dt)
	{
	}

	draw(ctx)
	{
		ctx.drawImage(this.img, this.x, this.y);
	}
}
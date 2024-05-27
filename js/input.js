/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input.js                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ljerinec <ljerinec@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/05/22 15:17:56 by ljerinec          #+#    #+#             */
/*   Updated: 2024/05/27 13:31:55 by ljerinec         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

let keyW = false;
let KeyS = false;
let KeyO = false;
let KeyL = false;

function keyPressed(t)
{
	console.log(t.code);
	if (t.code == "KeyW")
		keyW = true;
	if (t.code == "KeyS")
		KeyS = true;
	if (t.code == "KeyO")
		KeyO = true;
	if (t.code == "KeyL")
		KeyL = true;
}

function keyReleased(t)
{
	if (t.code == "KeyW")
		keyW = false;
	if (t.code == "KeyS")
		KeyS = false;
	if (t.code == "KeyO")
		KeyO = false;
	if (t.code == "KeyL")
		KeyL = false;
}
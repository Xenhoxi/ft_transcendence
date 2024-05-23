/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input.js                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ljerinec <ljerinec@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/05/22 15:17:56 by ljerinec          #+#    #+#             */
/*   Updated: 2024/05/23 10:02:56 by ljerinec         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

let keyW = false;
let KeyS = false;
let KeyO = false;
let KeyL = false;

function keyPressed(t)
{
	if (t.code == "KeyW")
		keyW = true;
	if (t.code == "KeyS")
		KeyS = true;
	if (t.code == "KeyO")
		KeyO = true;
	if (t.code == "KeyL")
		KeyL = true;
	// console.log(t.code);
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
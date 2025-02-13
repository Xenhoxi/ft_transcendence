class balle
{
	constructor(canevas){
		this.x = undefined;
		this.y = undefined;
		this.img = new Image();
		this.img.src = "../static/js/images/maltesers.png";
		this.startspeed = 500;
		this.evospeed = undefined;
		this.dirx = undefined;
		this.diry = undefined;
		this.size = 30;
		this.canevas = canevas

	}

	drawing(canvcont)
	{
        canvcont.drawImage(this.img, this.x, this.y, this.size, this.size);
    }

	move(ms)
	{
		this.x += this.dirx * 0.01667;
		this.y += this.diry;
	}
}
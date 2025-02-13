class local_racket
{
    constructor(x, y, str, speed, canevas)
    {
        this.x = x;
        this.y = y;
        this.height = 223;
        this.speed = speed;
        this.img = new Image();
        this.img.src = str;
        this.up = false;
        this.down = false
        this.score = 0;
        this.canevas = canevas
    }

    local_reset(canvcont)
    {
        this.score = 0;
        this.y = this.canevas.height / 2;
        if (this.x !== 0)
            this.x = this.canevas.width - 74;
    }

    local_drawing(canvcont)
    {
        canvcont.drawImage(this.img, this.x, this.y);
    }

    local_impact(ball)
    {
        let impact = (ball.y - this.y) - (this.height / 2)
        let normal = (impact / (this.height /2));
        return (normal);
    }

    local_scored()
    {
        this.score++;
    }

    local_moving(ms)
    {
        if (this.up === true)
        {
            if (this.y - (this.speed * ms) >= 0)
                this.y -= this.speed * ms;
        }
        if (this.down === true)
        {
            if (this.canevas.height >= (this.y + this.height) + (this.speed * ms))
                this.y += this.speed * ms;
        }
    }
}
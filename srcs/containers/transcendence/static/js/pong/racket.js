class racket {
    constructor(canevas, canvcont) {
        this.name = undefined;
        this.x = 0;
        this.y = 0;
        this.height = 223;
        this.speed = 1000;
        this.img = new Image();
        this.up_pressed = false;
        this.down_pressed = false;
        this.up = false;
        this.down = false;
        this.score = 0;
        this.canevas = canevas;
        this.canvcont = canvcont;
        this.side = undefined;
    }

    drawing(canvcont) {
        canvcont.drawImage(this.img, this.x, this.y);
    }


    draw_name(canvas_ctx, actual_fontsize) {
        let text = canvas_ctx.measureText(this.name);
        if (document.getElementById("player1") && document.getElementById("player2")) {
            if (this.side === 'right' && document.getElementById("player1").innerText.length <= 0) {
                document.getElementById("player1").innerText = this.name;
            }
            else if (this.side === 'left' && document.getElementById("player2").innerText.length <= 0) {
            document.getElementById("player2").innerText = this.name;
            }
        }
    }

    moving(ms) {
        if (this.up && !this.down) {
            if (this.y > 0)
                this.y -= this.speed * 0.01667;
            else
                this.y = 0;
        }
        else if (this.down  && !this.up) {
            if (this.y < 1080 - 233)
                this.y += this.speed * 0.01667;
            else
                this.y = 1080 - 233;
        }
    }

}


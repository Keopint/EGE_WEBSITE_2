const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

canvas.width = 1000;
canvas.height = 1000;

const coin_image = new Image();
coin_image.src = '../static/coin.jpg';

const diamond_image = new Image();
diamond_image.src = '../static/diamond.png';

roll_text = document.getElementById('roll_text');
roll_button = document.getElementById('roll_button');


const centerX = canvas.width / 2;
const centerY = canvas.height / 2;
const radius = Math.min(canvas.width, canvas.height) * 0.45;

const FPS = 60;


function Rad(gr) {
    return gr * Math.PI / 180;
}


function drawRotatedImage(image, x, y, w, h, degrees){
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(Rad(degrees));
    ctx.drawImage(image, -w/2, -h/2, w, h);
    ctx.restore();
  }


function drawText(text, x, y, degrees) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(Rad(degrees));
    
    ctx.fillStyle = "black";
    ctx.font = '50px sans-serif';
    ctx.textBaseline = "center";
    ctx.textAlign = "center";
    ctx.fillText(text, 0, 0);

    ctx.restore();
}


function moveForwardX(x, angle, steps) {
    return x + Math.cos(Rad(angle)) * steps;
}


function moveForwardY(y, angle, steps) {
    return y + Math.sin(Rad(angle)) * steps;
}


function fillSector(x, y, radius, angle, color = 'white') {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(Rad(angle));

    ctx.beginPath();
    
    ctx.moveTo(0, 0);
    var x1 = moveForwardX(0, 0, radius);
    var y1 = moveForwardY(0, 0, radius);
    ctx.lineTo(x1, y1);
    var x2 = moveForwardX(0, 0 + sectorAngle, radius);
    var y2 = moveForwardY(0, 0 + sectorAngle, radius);
    ctx.lineTo(x2, y2);


    ctx.arc(0, 0, radius, 0, Rad(sectorAngle) * 1, false);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.lineWidth = 1;

    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Rad(sectorAngle) * 1, false);
    ctx.strokeStyle = 'black';
    ctx.stroke();

    ctx.restore();
}


function drawReward(centerX, centerY, radius, local_angle, reward) {
    var image;
    if (reward[0] == "diamonds") {
        image = diamond_image;
    } else if (reward[0] == "tokens") {
        image = coin_image;
    }

    ctx.beginPath();
    var rmod = 0.58;
    var image_x1 = moveForwardX(centerX, local_angle + sectorAngle / 2, radius * rmod);
    var image_y1 = moveForwardY(centerY, local_angle + sectorAngle / 2, radius * rmod);
    drawRotatedImage(image, image_x1, image_y1, 100, 100, local_angle + sectorAngle / 2 + 90);

    ctx.beginPath();
    var rmod = 0.83;
    var text_x1 = moveForwardX(centerX, local_angle + sectorAngle / 2, radius * rmod);
    var text_y1 = moveForwardY(centerY, local_angle + sectorAngle / 2, radius * rmod);
    drawText(reward[1], text_x1, text_y1, local_angle + sectorAngle / 2 + 90);
}


function identifySector(angle) {
    cell = sectorsArray[Math.ceil((360 - (angle + 90 + sectorAngle) % 360) / sectorAngle) % sectors];
    let t = cell[0];
    if (t === "diamonds") {
        t = "keys";
    } else if (t === "tokens") {
        t = "fumes";
    }
    roll_text.innerHTML = cell[1] + " " + t;
    roll_text.style.backgroundColor = cell[2];
}

// config
// startAngle = 10;
// AngleG = -0.05;
// startAngleM = 20;

// angleM = startAngleM;
// angle = startAngle;

// sectorsArray = [
//     ["diamond", 5, "#ED8AE9"],
//     ["tokens", 50, "#FFF55F"],
//     ["diamond", 10, "#ED8AE9"],
//     ["diamond", 8, "#FFF55F"],
//     ["tokens", 100, "#FF5F61"],
// ]

// sectors = sectorsArray.length;
// sectorAngle = 360 / sectors;

function drawWheel() {
    identifySector(angle);

    ctx.globalAlpha = "1";
    ctx.globalCompositeOperation = "source-over"; 

    ctx.beginPath();
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let local_angle = angle;

    for (let i = 0; i < sectors; i++) {
        color = sectorsArray[i][2];
        fillSector(centerX, centerY, radius, local_angle, color);

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        var x1 = moveForwardX(centerX, local_angle, radius);
        var y1 = moveForwardY(centerY, local_angle, radius);
        ctx.lineTo(x1, y1);
        ctx.strokeStyle = 'black';
        ctx.stroke();

        drawReward(centerX, centerY, radius, local_angle, sectorsArray[i]);

        local_angle += sectorAngle;
    }

    ctx.beginPath();
    ctx.beginPath();
    var dy = 30;
    var dx = 20;
    ctx.moveTo(centerX, centerY - radius + dy / 2);
    ctx.lineTo(centerX - dx, centerY - radius - dy / 2);
    ctx.lineTo(centerX + dx, centerY - radius - dy / 2);
    ctx.lineTo(centerX, centerY - radius + dy / 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
    ctx.stroke();
}


coin_image.onload = function() {
    drawWheel();
}

diamond_image.onload = function() {
    drawWheel();
}


function gameLoop(animation=true) {
    if (angleM < 0) {
        return;
    }

    if (animation) {
        drawWheel();   
    }

    angle += angleM;
    angleM += AngleG;
}


function sendResult() {
    return
    var link = "/api/get_reward" + '/' + new URL(document.URL).pathname.split('/').pop();

    console.log(link);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", link, false)
    xhr.onload = function() {
        console.log(`Загружено: ${xhr.status} ${xhr.response}`);
        console.log(JSON.parse(xhr.response));
    };
    xhr.onprogress = function() {
        console.log("Загрузка...");
    };
    xhr.onerror = function() {
        console.log("Error");
    };
    xhr.send(JSON.stringify({}));
}


function rollWheel() {
    roll_button.disabled = true;
    sendResult();
    setInterval(gameLoop, 1000 / FPS);
}


function rollFullWheel() {
    roll_button.disabled = true;
    while (angleM > 0) {
        gameLoop(animation=false);
    }
    drawWheel();
}
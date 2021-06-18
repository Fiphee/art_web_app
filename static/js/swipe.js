const artCard = document.getElementById('swipe-card');
var isDown = false,
position = {
    original_x: 0,
    original_y: 0,
    current_x: 0,
    current_y: 0,
    deg: 0,
    previous_x: 0,
};

var pullDeltaX = 0;
var likeUrl = document.getElementById('swipe-like-btn').href;
var dislikeUrl = document.getElementById('swipe-dislike-btn').href;


$('.swipe-card').draggable({axis:"x", revert:"invalid"});

artCard.addEventListener('mousedown', function(down) {
    down.preventDefault();
    isDown = true;
    position.original_x = down.clientX;
    position.original_y = down.clientY;
    position.previous_x = down.clientX;
}, true);


artCard.addEventListener('mouseup', function(up) {
    up.preventDefault();
    isDown = false;
    position.deg = 0;
    position.current_x = position.original_x - up.clientX;
    if (position.current_x > 200) {
        console.log("DISLIKE");
        window.location.href = dislikeUrl;
    } else if (position.current_x < -200) {
        console.log("LIKE");
        window.location.href = likeUrl;
    } else {
        console.log("nothing happened");
        $(artCard).css('transform', 'rotate(0deg)');
    }
}, true);

artCard.addEventListener('mousemove', function(event) {
    if (isDown) {
        if (event.clientX > position.previous_x) {
            position.deg += .777;
            $(artCard).css('transform', 'rotate(' + position.deg + 'deg)');
            console.log('right');

        } else {
            position.deg -= .777;
            $(artCard).css('transform', 'rotate(' + position.deg + 'deg)');
            console.log('left');
        }
        position.previous_x = event.clientX;

    };
}, true);


$('.swipe-card').mouseleave(function() {
    if (isDown) {
        isDown = false;
    }
});

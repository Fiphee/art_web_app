const artCard = document.getElementById('swipe-card');
var isDown = false,
position = {
    original_x: 0,
    original_y: 0,
    current_x: 0,
    current_y: 0
};

function getLikeUrl() {
    var myUrl = document.getElementById('art-view-link').href,
    splitUrl = myUrl.split("/"),
    lastElementIndex = splitUrl.length - 1,
    baseUrl = splitUrl[0] + "//" + splitUrl[2] + '/artworks/swipe-like/',
    artId = splitUrl[lastElementIndex],
    likeUrl = baseUrl + artId;
    return likeUrl;
};

$('.swipe-card').draggable({axis:"x", revert:"invalid"});

artCard.addEventListener('mousedown', function(down) {
    down.preventDefault();
    isDown = true;
    position.original_x = down.clientX;
    position.original_y = down.clientY;
}, true);


artCard.addEventListener('mouseup', function(up) {
    up.preventDefault();
    isDown = false;
    position.current_x = position.original_x - up.clientX;
    if (position.current_x > 200) {
        console.log("DISLIKE");
        window.location.reload(false);
    } else if (position.current_x < -200) {
        console.log("LIKE");
        window.location.href = getLikeUrl();
    } else {
        console.log("nothing happened");
    }
}, true);


artCard.addEventListener('mousemove', function(event) {
    if (isDown) {
        console.log(position.original_x, position.original_y);
    };
}, true);


$('.swipe-card').mouseleave(function() {
    if (isDown) {
        console.log('Somamsd');
        isDown = false;
    }
});

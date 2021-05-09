$(function() {
    $('.fa-ellipsis-v').on('click', function() {
        var galleryList = $(this).siblings().first();
        $(galleryList).css('display', 'block')
    }),
    
    $('.gallery-list').mouseleave(function(){
        $(this).css('display','none');
    });

});

const likeBtn = document.getElementsByClassName('btn-like');
let likes = document.getElementsByClassName('likes-counter');


$(likeBtn).on('click', function(event) {
    event.preventDefault();
    let heart = $(this).children()
    
    $.ajax({
        type: 'GET',
        url: $(this).attr('href'),
        success: function(response) {
            $(likes).text(response.art_likes + ' Likes')

            if (response.liked) {
                heart.attr('id', 'liked-heart')
                heart.addClass('fas fa-heart btn-edit')
            } else {
                heart.attr('id', 'non-liked-heart')
                heart.addClass('far fa-heart btn-edit')
            }
        }
    });
})
    
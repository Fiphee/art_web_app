$(function() {
    $('.profile-card-container').hover(function() {
        $(this).find('.save-icon').css('color','black');
        $(this).find('#non-liked-heart').css('color','black');
        $(this).find('#edit-cog').css('color', 'black');
    }),
    $('.profile-card-container').mouseleave(function() {
        $(this).find('.save-icon').css('color','white')
        $(this).find('#non-liked-heart').css('color','white');
        $(this).find('#edit-cog').css('color', 'white');
    }),

    $('.save-icon').on('click', function() {
        var my_list = $(this).siblings().first(); 
        my_list.css('display', 'block');
        my_list.on('mouseleave', function() {
            my_list.css('display', 'none');
        });
    });

    var my_settings = document.getElementById('gallery-settings-form');
    $('.fa-edit').on('click', function(){
        $(my_settings).css('display', 'block')
    });

    $(my_settings).mouseleave(function() {
        $(this).css('display','none');
    });


const likeBtn = document.getElementsByClassName('heart-btn');


$(likeBtn).on('click', function(event) {
    event.preventDefault();
    let heart = $(this).children()
    let likes = $(this).siblings('.likes-counter')
    $.ajax({
        type: 'GET',
        url: $(this).attr('href'),
        success: function(response) {
            $(likes).text(response.art_likes + ' Likes')

            if (response.liked) {
                heart.attr('id', 'liked-heart')
                heart.addClass('fas fa-heart btn-edit')
                $(heart).css('color','#53d358')
            } else {
                heart.attr('id', 'non-liked-heart')
                heart.addClass('far fa-heart btn-edit')
                $(heart).css('color','white')
            }
        }
    });
});

const followBtn = document.getElementById('follow-btn')

$(followBtn).on('click', function(event) {
    event.preventDefault();
    $.ajax({
        type:'GET',
        url: $(this).attr('href'),
        success: function(response) {
            let follows_nr = document.getElementById('followers-nr');
            $(follows_nr).text(response.followers_nr);
            if (response.followed) {
                $(followBtn).text('Unfollow');
            } else {
                $(followBtn).text('Follow');
            };
        }

    });
});

});

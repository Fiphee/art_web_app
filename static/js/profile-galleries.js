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

    const makeComment = document.getElementById('make-comment');
    let cancelExists = false;

    function cloneForm(selector) {
        let comment = $(selector).parent().parent();
        
        let oldForm = document.getElementById('make-reply');
        $(oldForm).remove();
 
        let newForm = $(makeComment).clone(true);
        $(newForm).attr('class', 'make-reply');
        $(newForm).attr('id', "make-reply");
        let newFormTextArea = $(newForm).find('.textarea')
        $(newFormTextArea).val('@' + $(comment).find('.author').html() + ' ')
        let cancelBtn = jQuery('<span></span>', {
            id:'cancel-btn',
            class:'comment-btn',
            html:'Cancel',          
        });

        $(cancelBtn).click(function () {
            if (cancelExists) {
                $(newForm).remove();
            };
        });
        cancelExists = true;

        $(newForm).append(cancelBtn);
        $(comment).append(newForm)
        
};


    $('.reply-btn').on('click', function() {
        cloneForm(this)
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

<<<<<<< HEAD
$(document).on('DOMNodeInserted', function(e) {
    if ( $(e.target).hasClass('make-reply') ) {
        let replyBox = document.getElementById('make-reply');
        let replyCommentBtn = $(replyBox).find('.comment-btn').first();
        $(replyCommentBtn).on('click', function (e) {
            e.preventDefault();
            let comment = $(this).parent().parent().parent();
            let csrf = $('input[name=csrfmiddlewaretoken]').val();
            let replyUrl = 'http://127.0.0.1:8000' + $(comment).find('.reply-btn').children().attr('class')
            let body = $(this).siblings('.textarea').val();
            $.ajax({
                url: replyUrl,
                type:"post",
                data: {
                    body: body,
                    csrfmiddlewaretoken: csrf
                },
                success: function(response) {
                    location.reload()   


                },
            });
        })
    }
=======
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

>>>>>>> cbc03f8e28a6cf7863fea89dfa77b0d80b7ad63c
});

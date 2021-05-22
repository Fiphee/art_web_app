$(function() {
    $('.fa-ellipsis-v').on('click', function() {
        var galleryList = $(this).siblings().first();
        $(galleryList).css('display', 'block')
    }),
    
    $('.gallery-list').mouseleave(function(){
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

});

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
    

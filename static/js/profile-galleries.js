$(function() {
    $('.profile-card-container').hover(function() {
        $(this).find('.save-icon').css('color','black');
    }),
    $('.profile-card-container').mouseleave(function() {
        $(this).find('.save-icon').css('color','#53d358')
    }),

    $('.save-icon').on('click', function() {
        var my_list = $(this).siblings().first(); 
        my_list.css('display', 'block');
        my_list.on('mouseleave', function() {
            my_list.css('display', 'none');
        });
    }),

    $('.fa-times').on('click', function() {
        $(this).parent().parent().css('display', 'none');
    });


});



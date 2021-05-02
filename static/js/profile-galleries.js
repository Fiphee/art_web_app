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
});



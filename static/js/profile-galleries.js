$(function() {
    $('.profile-card-container').hover(function() {
        $(this).find('.save-icon').css('color','black');
    }),
    $('.profile-card-container').mouseleave(function() {
        $(this).find('.save-icon').css('color','white')
    }),

    $('.save-icon').on('click', function() {
        var myList = $(this).siblings().first(); 
        myList.css('display', 'block');
        myList.on('mouseleave', function() {
            myList.css('display', 'none');
        });
    });

    var mySettings = document.getElementById('gallery-settings-form');
    $('.fa-edit').on('click', function(){
        $(my_settings).css('display', 'block')
    });

    $(mySettings).mouseleave(function() {
        $(this).css('display','none');
    });
});



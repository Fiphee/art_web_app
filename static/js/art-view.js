$(function() {
    $('.fa-ellipsis-v').on('click', function() {
        var galleryList = $(this).siblings().first();
        $(galleryList).css('display', 'block')
    }),
    
    $('.gallery-list').mouseleave(function(){
        $(this).css('display','none');
    });

});


function sticky_relocate() {
    var window_top = $(window).scrollTop();
    var div_top = $('#sticky-anchor').offset().top;
    var stop_top = $('#stop-anchor').offset().top;
    if (window_top > div_top && window_top < stop_top) {
        $('#sticky').addClass('stick');
    }
    else {
        $('#sticky').removeClass('stick');
    }
}

$(document).ready(function () {
    $(window).scroll(sticky_relocate);
});
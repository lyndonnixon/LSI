$(function() {
    if ( $('.nav-tabs li').length > 0 ) {
        $('.nav-tabs li').click(function() {
            $(this).addClass('active');
            $(this).siblings().removeClass('active');
            $(".tab-content").hide();
            var tabId = $(this).attr("data-tab");
            $("#" + tabId).show();
            return false;
        });
    }
});

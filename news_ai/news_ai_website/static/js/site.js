var LOAD = 0;
var pageRef = window.location.pathname;

$(document).ready(function($) {
    updatePgRef();

    $("header").find('.logo').click(function() {
        window.location.href = "/";
    });
    
    if (pageRef != "/") { getData(); }
});

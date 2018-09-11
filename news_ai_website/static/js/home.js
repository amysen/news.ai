$(document).ready(function() {
    $("#content").parent().find("div").find(".url-btn").click(function() {

        url_input = $("#content").parent().find("div").find(".url-input")[1].value

        $.cookie("requested_url", url_input, { expires: 1 });

        window.location.href = "/analytics";        

    });
});
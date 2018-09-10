$(document).ready(function() {
    $("#content").parent().find("div").find(".url-btn").click(function() {

        url_input = $("#content").parent().find("div").find(".url-input")[1].value
        console.log(url_input)

        $.ajax({
            type: "POST",
            url: window.location,
            data: JSON.stringify({
               'url': url_input
            }),
            contentType: 'application/json',
        }).done(function(data){
            console.log(data)
            window.location.href = "/analytics";
        });

    });
});
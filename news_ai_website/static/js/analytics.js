$(document).ready(function() {

});

function getData() {


    var x = $.cookie("requested_url");

    $.ajax({
        type: "POST",
        url: window.location,
        data: JSON.stringify({
           'url': x
        }),
        contentType: 'application/json',
        
    }).done(function (data) {
        
        fillAnalyticsPage(data);
    });

}

function fillAnalyticsPage(data){
    
    var articleData = JSON.parse(data);
    console.log(articleData);
    $("#analytic-text").text('Summary: ' + articleData['summary']);
}
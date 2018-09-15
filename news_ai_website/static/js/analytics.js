$(document).ready(function() {

    $('.popover-dismiss').popover({
      trigger: 'focus'
    })

    $('[data-toggle="popover"]').popover()

    $('#domain-bias').hide();

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
    console.log('HERE');
    // console.log(data)
    data = JSON.parse(data);

    var articleData = data['articleData'];
    var biasData = data['biasData'];
    var biasDesc = data['biasDesc'];
    console.log(articleData);
    console.log(biasData);
    console.log(biasDesc);
    console.log(articleData['top_image']);


    $('#container').append('<span>' + articleData['title'] + '</span>');
    $('#container').find('span').css('background-color', 'white'); 
    $('#container').find('span').css('font-size', '40px'); 
    $('#container').find('span').css('font-weight', '500');


    $('#container').append('<p id="article-summary">' + articleData['summary'] + '</p>');


    console.log(articleData['authors'])
    console.log(articleData['authors'].length)
    if (articleData['authors'] != ''){
        if (articleData['authors'].length == 1) {
            $('#container').append('<p id="article-title">Author: ' + articleData['authors'] + '</p>');
        } else {
            $('#container').append('<p id="article-title">Authors: ' + articleData['authors'] + '</p>');
        }

    } 
    console.log(articleData['full_url'])
    $('#container').append('<a id="source-link" href=' + articleData['full_url'] + '></a>');
    $('#source-link').text('Original Article');

    $('#container').append('</br></br>');

    if (articleData['top_image'] != ''){
        $('#bg').css('background-image', 'url(' + articleData['top_image'] + ')'); 
        $('#bg').css('height', '50%'); 
        $('#chk').append('<button type="button" class="btn btn-lg btn-danger check-btn" data-toggle="modal" data-target="#exampleModalCenter">Check ' + biasData['name'] + '</button>');
    } else {
        $('#container').append('<button type="button" class="btn btn-lg btn-danger check-btn" data-toggle="modal" data-target="#exampleModalCenter">Check ' + biasData['name'] + '</button>');
    }

    
    
    // POPOVER BUTTON
    // $('#domain-bias').text('Check ' + biasData['name']);
    // $('#domain-bias').attr('data-original-title', biasDesc['name']);
    // $('#domain-bias').attr('data-content', biasDesc['description']);
    // $('#domain-bias').show();

    $('.modal-body').text(biasDesc['description'])
    $('.modal-title').text(biasDesc['name'])
    

    

    
}
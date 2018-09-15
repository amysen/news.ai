$(document).ready(function() {

    console.log('hello');

});


function getData() {
	console.log('inside trending');
    $.ajax({
        type: "POST",
        url: window.location,
        contentType: 'application/json'
        
    }).done(function (data) {

        fillTrendingPage(data);
        
    });


  function fillTrendingPage(data){
  	console.log('HERE');
    
    data = JSON.parse(data);

    // console.log(data)
    var divCount = 1;
    for (i = 0; i < 10; i++) { 
	    console.log(data['articles'][i])
	    $('#container').append("<div id='trending-"+divCount+"' class='list-group-item trending-story'></div>");
	    $('#trending-'+divCount+'').append('<h5>'+ data['articles'][i]['title'] +'</h5>');
	    $('#trending-'+divCount+'').append('<p>'+ data['articles'][i]['content'] +'</p>');
	    // '+ data['articles'][i]['title'] +'
	    // $('#container').find('li').append('<p id="trending-story" class="list-group-item">'+ data['articles'][i]['content'] +'</p>');
	    divCount ++;
	}

  }


 // var x = $.cookie("requested_url");

 //    $.ajax({
 //        type: "POST",
 //        url: window.location,
 //        data: JSON.stringify({
 //           'url': x
 //        }),
 //        contentType: 'application/json',
        
 //    }).done(function (data) {
        
 //        fillAnalyticsPage(data);
 //    });

}
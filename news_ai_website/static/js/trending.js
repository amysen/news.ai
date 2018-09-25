$(document).ready(function() {

    $(document).on("submit", "#viewBias", function(e){
        e.preventDefault();
        $form = $(this);
        url = $form.attr('action');

        $.cookie("requested_url", url, { expires: 365 });

        window.location.href = "/analytics";  
    });

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


function fillTrendingPage(data){
    console.log('HERE');
    
    data = JSON.parse(data);

    // console.log(data)
    var divCount = 1;
    for (i = 0; i < 10; i++) { 
        // console.log(data['articles'][i]['url'])
        // $('#grid-table').append('<tbody></tbody>');
        $('#container').append("<div id='trending-"+divCount+"' class='list-group-item trending-story'></div>");
        $('#trending-'+divCount+'').append('<h5>'+ data['articles'][i]['title'] +'</h5>');
        $('#trending-'+divCount+'').append('<p>'+ data['articles'][i]['source']['name'] +'</p>');
        $('#trending-'+divCount+'').append('<p>'+ data['articles'][i]['content'] +'</p>');
        // $('#trending-'+divCount+'').append('<a href='+ data['articles'][i]['url'] +'>Link to article</a>');
        $('#trending-'+divCount+'').append('<form id="viewBias" action="'+ data['articles'][i]['url'] +'"><input type="submit" class="btn btn-lg btn-danger check-btn" value="Bias Prediction" /></form>');
        $('#trending-'+divCount+'').append('<form id="viewArticle" action="'+ data['articles'][i]['url'] +'"><input type="submit" class="btn btn-lg btn-danger check-btn" value="Original Article" /></form>');
        
        // '+ data['articles'][i]['title'] +'
        // $('#container').find('li').append('<p id="trending-story" class="list-group-item">'+ data['articles'][i]['content'] +'</p>');
        divCount ++;
    }
}







$(document).ready(function() {

});

function getData() {
    $.ajax({
        type: "POST",
        url: window.location,
        data: JSON.stringify({
           // 'oldPass': oldPass,
           // 'newPass': secondPass,
           // 'process': 1, 
        }),
        contentType: 'application/json',
        
    }).done(function (data) {
        // try {
        //     data = JSON.parse(data);
        // } catch (e) {
        //     data = data;
        // }
        console.log(data);
        
    });

}
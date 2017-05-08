/**
 * Created by f3n1xx on 20/04/17.
 */
function showFlashMessage(message)
{
    var template= "<div class ='container-alert-flash'>"+
    "<div>"+
        "<div class='alert alert-success alert-dismissible' role='alert'>"+
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>"+
                "<span aria-hidden='true'>&times;</span>"+
            "</button>"+
            "<strong>"
            +message+
            "</strong>..."+
        "</div>"+
    "</div>"+
"</div>"

    $("body").append(template)
    $('.container-alert-flash').fadeIn();
    setTimeout(function(){
        $('.container-alert-flash').fadeOut();
    }, 1800);
}
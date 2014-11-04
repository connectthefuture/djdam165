$(function () {
    $.datepicker.setDefaults(
        $.extend($.datepicker.regional[""])
    );
    $("#datepicker").datepicker();
});


$(function () {
    $("input#datepicker").datepicker({
        changeMonth: true,
        changeYear: true,
        altFormat: "yy-mm-dd"
    });
});


$(function () {
    $("form#tweak_date").submit(function () {
        $search_key = $(this).children("input[type=date]").val();
        $new_action_path = "/searcher/find/" + $search_key + "/";
        location.href = $new_action_path;
        return false;
    });
});

$(function () {
    $("form#tweak_search").submit(function () {
        $search_key = $(this).children("input[type=text]").val();
        $new_action_path = "/searcher/find/" + $search_key + "/";
        location.href = $new_action_path;
        return false;
    });
});



/* Friendly URL rewrite */
$("form#tweak_searchdate").submit(function() {
    /* Remove unwanted characters, only accept alphanumeric and space */
    var keyword_start   = $('#startdate').val().replace(/[^A-Za-z0-9 ]/g,'');
    var keyword_end     = $('#enddate').val().replace(/[^A-Za-z0-9 ]/g,'');
    /* Replace multi spaces with a single space */
    keyword_start       = keyword_start.replace(/\s{2,}/g,' ');
    keyword_end         = keyword_end.replace(/\s{2,}/g,' ');

    /* Replace space with a '-' symbol */
    keyword_start       = keyword_start.replace(/\s/g, "-");
    keyword_end         = keyword_end.replace(/\s/g, "-");

    var cleanUrl        = 'searcher/find/' + keyword_start.toLowerCase() + '/' + keyword_end.toLowerCase + '/';
    window.location     = cleanUrl;
    return false;  // Prevent default button behaviour
});


// prepare the form when the DOM is ready
$(document).ready(function() {
    // bind form using ajaxForm
    $('#htmlForm').ajaxForm({
        // target identifies the element(s) to update with the server response
        target: '#htmlExampleTarget',

        // success identifies the function to invoke when the server response
        // has been received; here we apply a fade-in effect to the new content
        success: function() {
            $('#htmlExampleTarget').fadeIn('slow');
        }
    });
});




// Ajax Form Functions SUBMIT FORM
// prepare the form when the DOM is ready
$(document).ready(function() {
    var options = {
        target:        '#output2',   // target element(s) to be updated with server response
        beforeSubmit:  showRequest,  // pre-submit callback
        success:       showResponse, // post-submit callback

        // other available options:
        url:           'searcher/find/'         // override for form's 'action' attribute
        //type:      type        // 'get' or 'post', override for form's 'method' attribute
        //dataType:  null        // 'xml', 'script', or 'json' (expected server response type)
        //clearForm: true        // clear all form fields after successful submit
        //resetForm: true        // reset the form after successful submit

        // $.ajax options can be used here too, for example:
        //timeout:   3000
    };

    // bind to the form's submit event
    $('#myForm1').submit(function() {
        // inside event callbacks 'this' is the DOM element so we first
        // wrap it in a jQuery object and then invoke ajaxSubmit
        $(this).ajaxSubmit(options);

        // !!! Important !!!
        // always return false to prevent standard browser submit and page navigation
        return false;
    });
});

// pre-submit callback
function showRequest(formData, jqForm, options) {
    // formData is an array; here we use $.param to convert it to a string to display it
    // but the form plugin does this for you automatically when it submits the data
    var queryString = $.param(formData);

    // jqForm is a jQuery object encapsulating the form element.  To access the
    // DOM element for the form do this:
    // var formElement = jqForm[0];

    alert('About to submit: \n\n' + queryString);

    // here we could return false to prevent the form from being submitted;
    // returning anything other than false will allow the form submit to continue
    return true;
}

// post-submit callback
function showResponse(responseText, statusText, xhr, $form)  {
    // for normal html responses, the first argument to the success callback
    // is the XMLHttpRequest object's responseText property

    // if the ajaxSubmit method was passed an Options Object with the dataType
    // property set to 'xml' then the first argument to the success callback
    // is the XMLHttpRequest object's responseXML property

    // if the ajaxSubmit method was passed an Options Object with the dataType
    // property set to 'json' then the first argument to the success callback
    // is the json data object returned by the server

    alert('status: ' + statusText + '\n\nresponseText: \n' + responseText +
        '\n\nThe output div should have already been updated with the responseText.');
}


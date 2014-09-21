/**
 * Created by johnb on 9/17/14.
 */

//
//  function showValues() {
//    var str = $( "form.input.text" ).serialize();
//    $( "#results" ).text( str );
//  }
//  $( "input[type='checkbox'], input[type='radio']" ).on( "click", showValues );
//  $( "select" ).on( "change", showValues );
//
$(document).ready(function() {
    function submitChecked() {
        $('form #checkbox').is(':checked');

        var checkedValues = $('input:checkbox:checked').map(function () {
            return this.value;
        }).get();
    }
});

// Show Supplier data
$(document).ready(function() {
    function showValues() {
        var supplierImageAPI = "http://prodimages.ny.bluefly.com/api/v1/supplier-ingest-images/";
        var getFormInputs = $("input:text")
        colorstyle = getFormInputs.split('_')[0]
        alt = getFormInputs.split('_')[1]
        $.getJSON(supplierImageAPI, {
            //content: "application/json"
            format: "json",
            processDate: false,
            data: JSON.stringify({colorstyle: colorstyle, alt:alt})
        })
            .done(function (data) {
                $.each(data.items, function (i, item) {
                    //$( "<img>" ).attr( "src", item.media.m ).appendTo( "#searchResults" );
                    $("<img>").attr("src", item.image_url).appendTo("#resultsSearch");
                    if (i === 6) {
                        return false;
                    }
                });
            });
    };
});

//'image_url', 'bfly_local_src', 'bfly_zoom_src',  'bfly_list_site',
$(document).ready(function() {
    function submitSearchStyle() {
        $("#formSearchStyle").submit(function () {
            var colorstyle = $('#colorstyle').val();
            var inputAlt = colorstyle.split("_")[-1];
            var url = "http://prodimages.ny.bluefly.com/api/v1/supplier-ingest-images/";
            var res = {};
            $.ajax({
                type: "GET",
                url: "http://prodimages.ny.bluefly.com/api/v1/supplier-ingest-images/",
                dataType: "json",
                data: { colorstyle: colorstyle, alt: inputAlt },
                // $(colorstyle + "/" + inputAlt).serialize(), // serializes the form's elements.
                success: function () {
                    alert("Wow Lookie Here " + data); // show response from the python script.
                }
            });

            return false; // avoid to execute the actual submit of the form.
        });
    }
});


//  var supplierImageAPI = 'http://prodimages.ny.bluefly.com/api/v1/supplier-ingest-images/';
//  var jqxhr = $.ajax( supplierImageAPI )
//  .done(function() {
//    alert( "success" );
//  })
//  .fail(function() {
//    alert( "error" );
//  })
//  .always(function() {
//    alert( "complete" );
//  });
//
//// Perform other work here ...
//// Set another completion function for the request above
//    jqxhr.always(function() {
//      alert( "second complete" );
//    });

//   $( "#for" ).click(function() {  $( "#target" ).keypress();  });
$(document).ready(function() {
    function ajaxAnyInputBlur() {
        $(":input").blur(function () {
            var inputColorstyle = $('#inputColorstyle').val();
            var inputAlt = inputColorstyle.split("_")[-1];
            $.getJSON("http://prodimages.ny.bluefly.com/api/v1/supplier-ingest-images/", {
                colorstyle: inputColorstyle,
                alt: inputAlt
            })
                .done(function (json) {
                    console.log("JSON Data: " + json.colorstyle[ 0 ]);
                })
                .fail(function (jqxhr, textStatus, error) {
                    var err = textStatus + ", " + error;
                    console.log("Request Failed: " + err);
                })
                .always(function () {
                    alert("second complete");
                });
        });
    }
});
//
//
//var allInputs = $( ":input" );
//var formChildren = $( "form > *" );
//$( "#messages" ).text( "Found " + allInputs.length + " inputs and the form has " +
//  formChildren.length + " children." );
//
//$( "form" ).submit(function( event ) {
//  event.preventDefault();
//});
//

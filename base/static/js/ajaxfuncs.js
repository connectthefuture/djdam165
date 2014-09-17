/**
 * Created by johnb on 12/5/13.
 */
 
 
// ajax form entry on home page modal
//$(document).ready(function() {
//$('#searchSubmit').click(function() {
//    q = $('#input_list').val();
//    $('#results').html('&nbsp;').load('{% url 'searcher.run-script-views.script_runner' %}?q=' + q);
//    });
//});
//
$(document).ajaxStart(function() {
    $('#spinner').show();
    }).ajaxStop(function() {
    $('#spinner').hide();
});


//$(document).ready(function() {
//    var $colorstyle;
//    $colorstyle = $('#input_list');
//    $('#submitAjax').click(function() {
//    var jqxhr =
//        $.ajax({
//            url: "/api/v1/pmdata/" + $colorstyle,
//            dataType: 'json',
//            data: {
//                colorstyle : $colorstyle
//            }
//        })
//    .success (function(response) { $('#script-result').html(response)})
//    .error   (function()     { alert("Error")   ; })
//        });
////});
//
//
//var callback = $("#callback");
//$.ajax({
//    click: function (event, ui) {
//        var values = $.map(ui.inputs, function (checkbox) {
//            return checkbox.value;
//        }).join(", ");
//
//
//        $callback.html("Checkboxes " + (ui.checked ? "checked" : "unchecked") + ": " + values);
//    }
//});

//$(document).ready(function(){
////   $("#mutiple").multiselect();
//    $("select").multiselect().multiselectfilter();
//});

/// prevent refresh ajax
// $('#myFormSubmit{{ image.pk }}').click(function(e){
//      e.preventDefault();
//      alert($('#myField{{ image.pk }}').val());
//
//      $.post('http://path/to/post',
//         $('#myForm{{ image.pk }}').serialize(),
//         function(data, status, xhr){
//           // do something here with response;
//         });
//
//});


/// multiselect widget in modal
//$(document).ready(function () {
//    var el = $("select").multiselect(),
//        disabled = $('#disabled'),
//        selected = $('#selected'),
//        newItem = $('#newItem');
//
//    $("#add").click(function () {
//        var v = newItem.val(), opt = $('<option />', {
//            value: v,
//            text: v
//        });
//
//        if (disabled.is(':checked')) {
//            opt.attr('disabled', 'disabled');
//        }
//        if (selected.is(':checked')) {
//            opt.attr('selected', 'selected');
//        }
//
//        opt.appendTo(el);
//
//        el.multiselect('refresh');
//    });
//});

/////
 
/////
$(document).ready(function() {
    $("#override_input_list").change(function () {
        var val = $(this).val();
        if(val == "") return;
        $.getJSON("http://prodimages.ny.bluefly.com/api/v1/excel-view-vendorstyle-lookup/?format=json",
            {"output_colorstyle":val},
            function(response,code) {
            $("#output_colorstyle").val(response.colorstyle);
            $("#output_vendor_style").val(response.vendor_style);
            $("#output_color_group_id").val(response.color_group_id);
        })
    })
})


///// Input colorstyle AJAX get return to output vendor style
$(document).ready(function() {
    $("#inputColorstyle").blur(function () {
        $.post("http://prodimages.ny.bluefly.com/api/v1/excel-tool-data/" + $("#inputColorstyle").val() + "/?format=json",
        {output_vendor_style: $(this).val()},
        function (data) {
            $("#output_vendor_style").val(data);
        });
    });
});


/////
$(document).ready(function() {
    $("#input_clrstyle").bind("change", function (e) {
        $.getJSON("http://prodimages.ny.bluefly.com/api/v1/excel-view-vendorstyle-lookup/" + $("#inputColorstyle").val() + "/?format=json",
        function (data) {
            $.each(data, function (i, item) {
                if (item.field == "output_colorstyle") {
                    $("#colorstyle").val(item.value);
                } else if (item.field == "output_vendor_style") {
                    $("#vendor_style").val(item.value);
                } else if (item.field == "output_color_group_id") {
                    $("#output_color_group_id").val(item.value);
                } else if (item.field == "output_po_number") {
                    $("#po_number").val(item.value);
                }
            });
        });
    });
})

///// Input List return output list input fields
$(document).ready(function() {
    $("#input_list").change(function () {
        $.ajax({
            url: 'http://prodimages.ny.bluefly.com/api/v1/excel-tool-data/',
            type: 'GET',
            accepts: 'application/json',
            dataType: 'json',
            data: {input_list: $(this).val(),
                output_list: $("#output_list").val()
            },
            success: function (response) {
                $("#output_list").html(response)
            }
        })
    })
})


/////  Input POnumber
$(document).ready(function() {
    $("#po_number").bind("change", function (e) {
        $.getJSON("http://prodimages.ny.bluefly.com/api/v1/excel-view-vendorstyle-lookup/" + $("#inputColorstyle").val() + "/?format=json",
                {colorstyle: $(this).val()}, function (data) {
                    $("#colorstyle").val(data.colorstyle);
                    $("#vendor_style").val(data.vendor_style);
                    $("#color_group_id").val(data.color_group_id);
                    $("#po_number").val(data.color_group_id);
                })
    })
})


// Form scripts to grab and return input

///// Submit the search form with an input_list collected from input fields with id inputlist
$( "#searchForm" ).submit(function( event ) {
 
  // Stop form from submitting normally
  event.preventDefault();
 
  // Get some values from elements on the page:
  var $form = $(this),
    inputterm = $form.find( "input[name='input_list']" ).val(),
    url = $form.attr( "action" );
 
  // Send the data using post
  var posting = $.post( url, { input_list: inputterm } );
 
  // Put the results in a div
  posting.done(function(data) {
    var content = $(data).find( "#content" );
    $( "#output_list" ).empty().append( content );
  });
});


/////
$("#input_list_form").submit(function() {

    //var url = 'http://prodimages.ny.bluefly.com/api/v1/excel-tool-data/'; // the script where you handle the form input.
    // var url = 'http://prodimages.ny.bluefly.com/searcher/ajax/colorstyle/';
    //var url = '{% url 'searcher:views-ajax_colorstyle_search' %}';
    var url = 'searcher/ajax/colorstyle';
    $.ajax({
           type: "get",
           url: url,
           data: $("#input_list_form").serialize(), // serializes the form's elements.
           success: function(data) {
                    alert(data); // show response from the php script.
                    }
         });

    return false; // avoid to execute the actual submit of the form.
});
 

/////
$(document).ready(function(){
    ajax_search();
    $("#throbber").html('<img alt="loading..." src="/img/calendar.gif" />').hide();
    $("#sendFormButton").click(function(e){
        e.preventDefault();
        ajax_search();
    });
    $("#searchFormField").keyup(function(e){
        e.preventDefault();
        ajax_search();
    });
    $("#winkelFormSelect").change(function(e){
        e.preventDefault();
        ajax_search();
    });
});


////// example must adjust to work
var timeout = null;

function ajax_search() {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(function(){
        $("#throbber").show();
        $("#results").slideUp(); //Hide results DIV
        var search_val=$("#searchFormField").val()
        var winkel_id=$("#winkelFormSelect").val()
        var ajax_search_REQ=$.post("./json/", {search: search_val, winkel: winkel_id },function(jsondata){
            if (ajax_search_REQ) {ajax_search_REQ.abort();}
            $("#results").html(result_table(jsondata,search_val,winkel_id)).slideDown();
            $("#results table").tableSorter({
        		sortColumn: 'name',			// Integer or String of the name of the column to sort by.
        		sortClassAsc: 'headerSortUp',		// Class name for ascending sorting action to header
        		sortClassDesc: 'headerSortDown',	// Class name for descending sorting action to header
        		headerClass: 'header',			// Class name for headers (th's)
        		stripingRowClass: ['even','odd'],	// Class names for striping supplyed as a array.
        		stripRowsOnStartUp: true		// Strip rows on tableSorter init.
        	});
            $("#results table tr").hover(
                function() { $(this).addClass("hover"); },
                function() { $(this).removeClass("hover"); }
            );
            $("#throbber").hide();
        },"json");
    }, 400);
}


///// example
function result_table(jsondata,search_val,winkel_id) {
        var aantal = jsondata.length
        if (aantal == 0) {
            return '<b>Geen producten gevonden</b>';
        }
        else {
          if (aantal == 1) {html='<b>1 product gevonden</b>';}
          else {html='<b>'+aantal+' producten gevonden</b>';}
          html_table='<table>';
          html_table+='<tr><th>Naam</th><th>Prijs</th>';
          if (winkel_id == 0) {
              html_table+='<th>Winkel</th>';
          }
          html_table+='<th>Omschrijving</th></tr>';
          for (i in jsondata){
              html_table+='<tr><td class="naam">';
              html_table+=jsondata[i].naam;
              html_table+='</td><td class="prijs">';
              html_table+=jsondata[i].prijs;
              html_table+='</td><td>';
              if (winkel_id == 0) {
                  html_table+='<a class="winkel" href="'+jsondata[i].set.get_absolute_url+'">'+jsondata[i].set.winkel+'</a>';
                  html_table+='</td><td>';
              }
              html_table+=jsondata[i].omschrijving;
              html_table+='</td></tr>';
          }
          html_table+='</table>';
          html+=html_table
          return html;
        }
}

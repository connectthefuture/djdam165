/**
* Created by relic7 on 6/30/14.
*/
 
// ajax form entry on home page modal
$(document).ready(function() {
$('#searchSubmit').click(function() {
    q = $('#input_list').val();
    $('#results').html('&nbsp;').load('{% url 'searcher.run-script-views.script_runner' %}?q=' + q);
    });
});
 
$(document).ajaxStart(function() {
    $('#spinner').show();
    }).ajaxStop(function() {
    $('#spinner').hide();
});

/////
$("#input_list_form").submit(function() {

    //var url = 'http://prodimages.ny.bluefly.com/api/v1/excel-tool-data/'; // the script where you handle the form input.
    // var url = 'http://prodimages.ny.bluefly.com/searcher/ajax/colorstyle/';
    //var url = '{% url 'searcher:views-ajax_colorstyle_search' %}';
    var url = 'searcher/runscripts/script_runner_home';
    $.ajax({
           type: "get",
           url: url,
           data: $("#input_list_form").serialize(), // serializes the form's elements.
           success: function(data) {
                    alert(data); // show response from the python script.
                    }
         });

    return false; // avoid to execute the actual submit of the form.
});
 

//// Date picker popup calendar 
$('#daterange-container').find('.input-daterange').datepicker({
          todayBtn: true,
          orientation: "auto center",
          todayHighlight: true
      });


////
// prepare Options Object
      var options;
          options = {
          target: '#divToUpdate',
          url: '/admin/',
          success: function () {
          alert('Thanks for your comment!');
      }
      };
// pass options to ajaxForm

      // $('#myForm').ajaxForm(options);


////
$( "#datepicker" ).datepicker();

    var i = document.createElement("input");
    i.setAttribute("type", "date");
        if (i.type == "text") {
          $( "#datepicker" ).datepicker();
        // No native date picker support :(
        // Use Dojo/jQueryUI/YUI/Closure to create one,
        // then dynamically replace that <input> element.
        }
</script>
<script>
$('form #checkbox').is(':checked');
</script>
<script>
var checkedValues = $('input:checkbox:checked').map(function() {
        return this.value;
}).get();
</script>

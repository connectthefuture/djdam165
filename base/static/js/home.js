/**
* Created by relic7 on 6/30/14.
*/
 
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

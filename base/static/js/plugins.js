// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

// Place any jQuery/helper plugins in here.
$(function() {
    $( "#form_date_field" ).datepicker({
    todayBtn: true,
    orientation: "auto center",
    todayHighlight: true
    });
});


 $("button #testalert").submit(function (keyword_start, keyword_end) {
              alert("Start: " + keyword_start + "\nEnd: " + keyword_end);
          });


// Get value of all checked boxes
$('#submit').click(function() {
  var checkedBoxes = $('#CheckedBoxes').val('')[0];
  $('.a-checkbox:checked').each(function(){
     checkedBoxes.value += this.value + ' ';
  });
});

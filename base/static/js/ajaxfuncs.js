/**
 * Created by johnb on 12/5/13.
 */
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
/**
 * Cross-browser script to style object. Make sure id and name are set
 * DOES NOT ALWAYS WORK WELL WITH LAYERS
 * found at apple developer site... author unknown
 **/
function getStyleObject(objectId) {
    // cross-browser function to get an object's style object given its id
    if (document.all && document.all(objectId)) {
        // MSIE 4 DOM
        return document.all(objectId).style;
    } else if(document.getElementById && document.getElementById(objectId)) {
        // W3C DOM
        return document.getElementById(objectId).style;
    } else if (document.layers && document.layers[objectId]) {
        // NN 4 DOM.. note: this won't find nested layers
        return document.layers[objectId];
    } else {
        return false;
    }
}

/**
 * Cross-browser script to an object. Make sure id and name are set. 
 * DOES NOT ALWAYS WORK WELL WITH LAYERS
 * found at apple developer site... author unknown
 **/
function getAnObject(objectId) {
    // cross-browser function to get an object's style object given its id
    if(document.getElementById && document.getElementById(objectId)) {
        // W3C DOM
        return document.getElementById(objectId);
    } else if (document.all && document.all(objectId)) {
        // MSIE 4 DOM
        return document.all(objectId);
    } else if (document.layers && document.layers[objectId]) {
        // NN 4 DOM.. note: this won't find nested layers
        return document.layers[objectId];
    } else {
        return false;
    }
} // getAnObject


/**
 * Simple script to flip images.
 * author: unknown
 **/
function imgFlip(target,changeto) {
    if (menuItem==changeto) return;
    found = getAnObject( target );
    found.src = eval(changeto + ".src");
}

/**
 * Gets the value of the specified cookie.
 *
 * name  Name of the desired cookie.
 *
 * Returns a string containing value of specified cookie,
 *   or null if cookie does not exist.
 * found on the web... author unknown
 */
function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    } else {
        begin += 2;
    }
    var end = document.cookie.indexOf(";", begin);
    if (end == -1) {
        end = dc.length;
    }
    return unescape(dc.substring(begin + prefix.length, end));
}
/**
 * Sets a Cookie with the given name and value.
 *
 * name       Name of the cookie
 * value      Value of the cookie
 * [expires]  Expiration date of the cookie (default: end of current session)
 * [path]     Path where the cookie is valid (default: path of calling document)
 * [domain]   Domain where the cookie is valid
 *              (default: domain of calling document)
 * [secure]   Boolean value indicating if the cookie transmission requires a
 *              secure transmission
 * found on the web... author unknown
 */
function setCookie(name, value, expires, path, domain, secure) {
    document.cookie= name + "=" + escape(value) +
        ((expires) ? "; expires=" + expires.toGMTString() : "") +
        ((path) ? "; path=" + path : "") +
        ((domain) ? "; domain=" + domain : "") +
        ((secure) ? "; secure" : "");
}
/**
 * Selects all items in a select box.
 * author: unknown
 **/
function selectAll(selectObj) {
    if (selectObj == null) return false;
    if (selectObj.options.length == 0) return false;
    for (var i = 0; i < selectObj.length; i++) {
        selectObj.options[i].selected = true;
    }
    return;
}
/**
 * un-selects all items in a multi-select box
 * author: unknown
 **/
function unSelectAll(selectObj) {
    if (selectObj == null) return false;
    for (var i = 0; i < selectObj.length; i++) {
        selectObj.options[i].selected = false;
    }
    return true;
}

/**
 * Do nothing function
 * author: unknown
 **/
function doNothing() {
}

/*
DATE AND FORM RELATED FUNCTIONS Bootstrap and jQuery
*/

/* Pretty/Friendly URL rewrite for Submitting to Django url Conf */
$("form .navbar-form").submit(function() {
    /* Remove unwanted characters, only accept alphanumeric and space */
    var keyword = $('#searchtext').val().replace(/[^A-Za-z0-9 ]/g,''); 
    /* Replace multi spaces with a single space */
    keyword = keyword.replace(/\s{2,}/g,' ');
    /* Replace space with a '-' symbol */
    keyword = keyword.replace(/\s/g, "-");
    var cleanUrl = 'searcher/find/' + keyword.toLowerCase();
    window.location = cleanUrl;
    return false;  // Prevent default button behaviour
});


/**
 * Email validator
 * author: unknown
 **/
function checkEmail(src) {
    var regex = new RegExp("^([a-z0-9_]|\\-|\\.)+@(([a-z0-9_]|\\-)+\\.)+[a-z]{2,4}\$");
    return regex.test(src);
}


/**
* Clear the textbox and dropdowns on a button click
**/
 function clearSearchCriteria() {
        var elm; 
        var elements = document.forms[0].elements;  //document.forms[0] = the first form in the html document
        for( i=0, elm; elm=elements[i++]; ) {       //iterate each elements array and put a single element in variable elm to process
            if (elm.type == "text") {               //check the type of elm.type (if type = text or select then reset it)
                elm.value ='';
            } else if(elm.type == "select-one") {   //if type = dropdown
                elm.selectedIndex = 0;
            }else if(elm.type =="textarea"){
                elm.value ='';
            }
        }
   }


/**
 * Checks to see if a given variable is empty, just like in php
 * author: russellsimpkins@hotmail.com
 **/
function empty(value) {
    if( value == null ||
        value == "" ||
        value == 0 ||
        trim(value) == ""
        ) {
        return true;
    }
    return false;
}



/**
 * Helper function to check valid dates
 * It intellignetly tries to determine one of the date separators and
 * author: russellsimpkins@hotmail.com 
 **/
function valiDate( tdate, sep ) {
    if (sep == null || sep == "") sep = "/";
    document.write("<br>sep: " + sep);
    if ( tdate.indexOf(sep) > 0 ) {
        parts = tdate.split(sep);
        if ( parts.length != 3 ) return false;
        if ( parts[0].length == 4 ) {
            // test using YYYY/MM/DD format
            return checkDate( parts[1],parts[2],parts[0] );
        } else {
            // test using MM/DD/YYYY
            return checkDate( parts[0], parts[1], parts[2] );
        }
    }
    return false;
}
/**
 * Validates a given date
 * author: russellsimpkins@hotmail.com
 **/
function checkDate( month, day, year ) {
    months = new Array(32,29,32,31,32,31,32,32,31,32,31,32);
    // set the low year
    lowyear = 1880;
    if (--month < 0) return false;
    if ( year <= lowyear ) return false;
    // leap year test
    if ( (year%4) == 0 ) months[1]=30;
    if ( month < 12 && day > 0  && day < months[month] ) {
        return true;
    } else {
        return false;
    }
}

/**
 * Quick and dirty trim string function. It is recursive.
 * author: russellsimpkins@hotmail.com
 **/
function trim( str ) {
    if ( str.charAt(0) == " ") 
        return trim( str.substr(1) );
    if ( str.charAt( str.length - 1 ) == " ")
        return trim( str.substr(0, str.length - 2) );
    return str;
}

/**
 * Simple script to open a popup window
 * author: russellsimpkins@hotmail.com
 **/
function openPop(theURL,winName,features) {
    if (theURL==null) theURL="/";
    if (winName==null) winName="default";
    if (features==null) features="width=400;height=400";
  window.open(theURL,winName,features);
}

/**
 * Simple script to change address set in a drop-down menu
 * I expect your menu to be selected and to have uri/url as options
 * i.e. <option value="http://somewhere.com">Go somewhere now</option>
 * usage <select onchange="jumpmenu(this)">
 * author: russellsimpkins@hotmail.com
 **/
function jumpmenu(menu) {
    window.location.href = menu.options[menu.selectedIndex].value;
}

/**
 * One way to always get a form.
 * author: russellsimpkins@hotmail.com
 **/
function getForm( id ) {
    var allforms = document.forms;
    var index = 0;
    for ( index = 0; index < allforms.length; ++index) {
        if ( allforms[index].id == id ) {
            return allforms[index];
        }
    }
    return null;
}









/* Setup the javascript calendar popup. BFLY Example from PM */
// var start_date_cal,end_date_cal,priority_date_cal,dock_date_cal,in_receiving_date_cal,receive_date_cal,expected_date_cal,in_transit_date_cal,bfly_From_Date_cal,bfly_To_Date_cal,product_search_start_date_from_cal,product_search_start_date_to_cal;
// function calendarInit() {
//   start_date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('poStartDate'));
//   end_date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('poEndDate'));
//   priority_date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('promoLaunchDate'));
//   dock_date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('preReceiptDate'));
//   dock_date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('dockDate'));
//   in_receiving_date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('inReceivingDate'));
//   receive_date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('receiveDate'));
//   expected_date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('expectedDate'));
//   in_transit_date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('inTransitDate'));
//   bfly_From_Date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('bflyFromDate'));
//   bfly_To_Date_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('bflyToDate'));
//   product_search_start_date_from_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('productSearchStartDateFrom'));
//   product_search_start_date_to_cal =
//   new Epoch('epoch_popup', 'popup', document.getElementById('productSearchStartDateTo'));
  
// };
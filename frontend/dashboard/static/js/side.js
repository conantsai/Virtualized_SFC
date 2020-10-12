var fwErr = 2;
var idsErr = 2;
var dpiErr = 2;
var wafErr = 2;


function updateStatus() {
    $.get( "../SF_status/", function(status) {
        if (status.fw === true) {
            fwErr = 0;
        } else {
            fwErr++;
        }
        if (status.ids === true) {
            idsErr = 0;
        } else {
            idsErr++;
        }
        if (status.dpi === true) {
            dpiErr = 0;
        } else {
            dpiErr++;
        }
        if (status.waf === true) {
            wafErr = 0;
        } else {
            wafErr++;
        }
    })
        .fail(function() {
            fwErr++;
            idsErr++;
            dpiErr++;
            wafErr++;
        })
        .always(function() {
            if (fwErr >= 2) {
                $("#fw_status").attr("src","/static/img/exclamation.gif");
            } else {
                $("#fw_status").attr("src","/static/img/gear.gif");
            }
            if (idsErr >= 2) {
                $("#ids_status").attr("src","/static/img/exclamation.gif");
            } else {
                $("#ids_status").attr("src","/static/img/gear.gif");
            }
            if (dpiErr >= 2) {
                $("#dpi_status").attr("src","/static/img/exclamation.gif");
            } else {
                $("#dpi_status").attr("src","/static/img/gear.gif");
            }
            if (wafErr >= 2) {
                $("#waf_status").attr("src","/static/img/exclamation.gif");
            } else {
                $("#waf_status").attr("src","/static/img/gear.gif");
            }
        })
}

setInterval(updateStatus, 2000);

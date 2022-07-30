/* jshint esversion: 11, jquery: true */

// ensure start/end dates are not before "today", and end-date comes on/after start-date
setEndDateMin(); // set the min-value for end_date on page-load, if existing, otherwise disabled
let now = new Date(),
minDate = now.toISOString().substring(0,10);
$("#id_start_date").prop("min", minDate);
$("#id_start_date").on("change", setEndDateMin);
$("#id_end_date").on("change", setEndDateMin);
function setEndDateMin() {
    let startDate = $("#id_start_date").val();
    if (!startDate) {
        $("#id_end_date").prop("disabled", true);
    } else {
        $("#id_end_date").prop({"disabled": false, "min": startDate});
    }
}

// set the 'max' value for "amount-paid" no higher than the "total-price"
$("#id_total_price").on("change", setMaxPaidPrice);
$("#id_amount_paid").on("change", setMaxPaidPrice);
function setMaxPaidPrice() {
    let totalPrice = $("#id_total_price").val();
    $("#id_amount_paid").prop("max", totalPrice);
}

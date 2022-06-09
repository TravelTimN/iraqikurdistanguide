/* jshint esversion: 11 */

// update copyright year
document.getElementById("year").innerText = new Date().getFullYear();

// get local time in Kurdistan/Iraq
function updateTime() {
    let time = new Date().toLocaleTimeString("en-UK", {
        hour: "numeric",
        minute: "2-digit",
        timeZone: "Asia/Baghdad"
    });
    // add leading 0 to timestamp if single-digit hour
    if (!/^([0-9]{2}\:[0-9]{2})$/.test(time)) {
        time = `0${time}`;
    }
    return time;
}

// toggle 'clock' and 'time' in Kurdistan
let timeIcon;
$("#nav-link-time").on("mouseover", function() {
    timeIcon = $(this).html();
    $(this).html(updateTime());
});
$("#nav-link-time").on("mouseleave", function() {
    $(this).html(timeIcon);
});

// localStorage: remember if user closed the "review banner"
const btnCloseReview = document.getElementById("btn-close-review");
const reviewBanner = document.getElementById("banner-review");

// check for existing localStorage of "review banner" being closed previously
if (!JSON.parse(localStorage.getItem("reviewClosed"))) {
    // none found / allow clicking to close banner
    btnCloseReview?.addEventListener("click", closeReviewBanner);
} else {
    // previously closed / auto-hide banner from now on
    reviewBanner.classList.remove("show");
    reviewBanner.classList.add("d-none");
}

// add localStorage for "review banner" being closed
function closeReviewBanner() {
    localStorage.setItem("reviewClosed", JSON.stringify({"reviewClosed": true}));
}

// auto-hide alerts
const alerts = document.querySelectorAll("aside.alert");
let overlay = document.getElementById("overlay");
if (alerts.length > 0) {
    // only if any alerts found on DOM
    overlay?.classList.remove("hide");
    for (let i = 0; i < alerts.length; i++) {
        setTimeout(() => {
            // start after 2500ms
            setTimeout(() => {
                // slight delay between each alert
                alerts[i].classList.add("alert-slide");
                setTimeout(() => {
                    // remove from DOM entirely
                    alerts[i].style.display = "none";
                }, 1000);
            }, i * 100);
            // remove the overlay background
            setTimeout(() => {
                overlay?.classList.add("hide");
            }, 500);
        }, 2500);
    }
}

/*
    Initialize Bootstrap Components
*/
// tooltips
let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

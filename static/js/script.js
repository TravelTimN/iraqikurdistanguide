/* jshint esversion: 11, jquery: true */

// remove preloader animation once page is fully loaded
$(document).ready(function() {
    $("body").addClass("page-load-complete");
});

// $(".navbar-brand, .nav-link:not(.dropdown-toggle), .nav-item ul.dropdown-menu li a.dropdown-item, .breadcrumb-item:not(.dropdown), .breadcrumb-item ul.dropdown-menu li a.dropdown-item").on("click", function() {
//     $("body").removeClass("page-load-complete");
// });

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

// auto-expand/collapse breadcrumb dropdown-menu on hover
let breadcrumbDropdown = document.querySelectorAll(".breadcrumb-item.dropdown");
breadcrumbDropdown.forEach(dropdown => {
    // mouseover; show sub-menu
    dropdown.addEventListener("mouseover", function() {
        let dropdownToggle = this.querySelector(".dropdown-toggle");
        dropdownToggle.classList.add("show");
        dropdownToggle.setAttribute("aria-expanded", true);
        let menuUL = this.querySelector("ul.dropdown-menu");
        menuUL.classList.add("show");
        menuUL.setAttribute("data-popper-placement", "bottom-start");
    });
    // mouseleave; hide sub-menu
    dropdown.addEventListener("mouseleave", function() {
        let dropdownToggle = this.querySelector(".dropdown-toggle");
        dropdownToggle.classList.remove("show");
        dropdownToggle.setAttribute("aria-expanded", false);
        let menuUL = this.querySelector("ul.dropdown-menu");
        menuUL.classList.remove("show");
        menuUL.removeAttribute("data-popper-placement");
    });
});

/*
    Initialize Bootstrap Components
*/
// tooltips
let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// handling localStorage for "destinations"
let wishlist = localStorage.getItem("wishlist");

let destinationIcons = $("[id^='wishlist-icon_']");
$(destinationIcons).each(function() {
    let iconId = $(this).attr("id").split("_")[1];
    wishlist = localStorage.getItem("wishlist").split(",");
    for (let place in wishlist) {
        if (wishlist.hasOwnProperty(place)) {
            if (wishlist[place] == iconId) {
                // set solid-heart and 'remove' text
                setInWishlist($(this), $(this).siblings("span[id^='wishlist-text_']"));
            }
        }
    }
});

$("body").on("click", ".destination-card-text", function(e) {
    e.preventDefault();
    let destination = $(this).data("destination");
    let wishlistIcon = $(this).children("i[id^='wishlist-icon_']");
    let wishlistText = $(this).children("span[id^='wishlist-text_']");
    if ($(wishlistIcon).hasClass("far")) {
        // adding new wishlist destination
        addWishlistDestination(this, destination);
        setInWishlist(wishlistIcon, wishlistText);
    } else if ($(wishlistIcon).hasClass("fas")) {
        // removing existing wishlist destination
        removeWishlistDestination(this, destination);
        setNotInWishlist(wishlistIcon, wishlistText);
    }
});

function setInWishlist(wishlistIcon, wishlistText) {
    // update destination to be in wishlist
    $(wishlistIcon).removeClass("far").addClass("fas");
    $(wishlistText).text("remove from");
}

function setNotInWishlist(wishlistIcon, wishlistText) {
    // update destination to remove from wishlist
    $(wishlistIcon).removeClass("fas").addClass("far");
    $(wishlistText).text("add to");
}

function addWishlistDestination(e, destination) {
    // check if localStorage wishlist exists
    if (localStorage.getItem("wishlist")) {
        // exists - split the values
        wishlist = localStorage.getItem("wishlist").split(",");
        if (!wishlist.includes(destination)) {
            // only add destination if not already in the list
            wishlist.push(destination);
            wishlist.sort();
            localStorage.setItem("wishlist", wishlist.join(","));
        }
    } else {
        // doesn't exist, add the destination
        localStorage.setItem("wishlist", destination);
    }
}

function removeWishlistDestination(e, destination) {
    // wishlist MUST exist if calling this function, so remove the clicked 'destination'
    let wishlist = localStorage.getItem("wishlist").split(",");
    for (let place in wishlist) {
        if (wishlist.hasOwnProperty(place)) {
            if (wishlist[place] == destination) {
                // remove destination
                delete wishlist[place];
            }
        }
    }
    // filter only those that are not the destination
    wishlist = wishlist.filter(function(place) {return place["wishlist"] !== destination;});
    // re-add back to localStorage
    localStorage.setItem("wishlist", wishlist.join(","));
    
}

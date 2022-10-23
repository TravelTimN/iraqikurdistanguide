/* ----- jshint esversion: 11, jquery: true ----- */


/* ----- BOOTSTRAP COMPONENTS ----- */

// tooltips
let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});


/* ----- PRELOADER ----- */

// remove preloader animation once page is fully loaded
$(document).ready(function() {
    $("body").addClass("page-load-complete");
});

// $(".navbar-brand, .nav-link:not(.dropdown-toggle), .nav-item ul.dropdown-menu li a.dropdown-item, .breadcrumb-item:not(.dropdown), .breadcrumb-item ul.dropdown-menu li a.dropdown-item").on("click", function() {
//     $("body").removeClass("page-load-complete");
// });


/* ----- TO TOP BUTTON ----- */

// scroll to top button
let btnTop = document.getElementById("btn-top");
window.addEventListener("load", viewportMagic, true);
window.addEventListener("resize", viewportMagic, true);
window.addEventListener("scroll", viewportMagic, true);
function viewportMagic() {
    if (window.scrollY > 750) {
        btnTop.style.cssText = "bottom: 0.25em;";
    } else {
        btnTop.style.cssText = "bottom: -3em;";
    }
}


/* ----- NAVBAR LINKS ----- */

// update nav-links with 'active' state
let activeLink;
if (location.pathname.includes("/about/")) {
    activeLink = "about";
} else if (location.pathname.includes("/destinations/")) {
    activeLink = "destinations";
} else if (location.pathname.includes("/faqs/")) {
    activeLink = "faqs";
} else if (location.pathname.includes("/gallery/")) {
    activeLink = "gallery";
} else if (location.pathname.includes("/resources/")) {
    activeLink = "resources";
} else if (location.pathname.includes("/reviews/")) {
    activeLink = "reviews";
} else if (location.pathname.includes("/contact/")) {
    activeLink = "contact";
} else if (location.pathname.includes("/bookings/")) {
    activeLink = "bookings";
} else {
    activeLink = "home";
}
// apply classes and aria-current to relevant page link
$(`[id^="nav-link-${activeLink}"]`).removeClass("list-group-item-dark").addClass("active list-group-item-light").prop("aria-current", true);


/* ----- COPYRIGHT ----- */

// update copyright year
document.getElementById("year").innerText = new Date().getFullYear();


/* ----- KURDISH TIME ----- */

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

// display local time in Kurdistan when offcanvas-menu open
$("#offcanvas-toggle-btn").on("click", function() {
    $("#nav-link-time").html(updateTime());
});


/* ----- REVIEW BANNER ----- */

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


/* ----- COOKIES BANNER ----- */

// localStorage: remember if user closed the "cookies banner"
const btnCloseCookies = document.getElementById("btn-close-cookies");
const cookiesBanner = document.getElementById("banner-cookies");

// adjust padding-bottom on body to accommodate fixed-banner size
$(window).on("load resize", function() {
    let cookiesBannerHeight = $(cookiesBanner).height();
    document.body.style.paddingBottom = `${cookiesBannerHeight}px`;

    // check for existing localStorage of "cookies banner" being closed previously
    if (!JSON.parse(localStorage.getItem("cookiesClosed"))) {
        // none found / allow clicking to close banner
        btnCloseCookies?.addEventListener("click", closeCookiesBanner);
    } else {
        // previously closed / auto-hide banner from now on
        cookiesBanner.classList.remove("show");
        cookiesBanner.classList.add("d-none");
        document.body.style.paddingBottom = "unset";
    }
});

// add localStorage for "cookies banner" being closed
function closeCookiesBanner() {
    localStorage.setItem("cookiesClosed", JSON.stringify({"cookiesClosed": true}));
    document.body.style.paddingBottom = "unset";
}


/* ----- ALERTS ----- */

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


/* ----- BREADCRUMBS  ----- */

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


/* ----- WISHLIST (destinations) ----- */

// handling localStorage for "destinations"
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

let wishlist = localStorage.getItem("wishlist");

let destinationIcons = $("[id^='wishlist-icon_']");
$(destinationIcons).each(function() {
    let iconId = $(this).attr("id").split("_")[1];
    wishlist = localStorage.getItem("wishlist")?.split(",");
    for (let place in wishlist) {
        if (wishlist.hasOwnProperty(place)) {
            let wishlistPlace = wishlist[place].replace(" ", "").replace("-", "").replace("&", "").toLowerCase();
            if (wishlistPlace == iconId) {
                // set solid-heart and 'remove' text
                setInWishlist($(this), $(this).siblings("span[id^='wishlist-text_']"));
            }
        }
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
        wishlist = localStorage.getItem("wishlist")?.split(",");
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
    wishlist = localStorage.getItem("wishlist")?.split(",");
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


/* ----- CRUD Functionality ----- */

// disable first <option> in each <select> input (exception: booking guide defaults to Haval)
$("select:not(#id_guide)").each(function() {
    $(this).children("option:first").prop("disabled", true);
});

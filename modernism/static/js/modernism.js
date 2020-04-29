var nav = document.querySelector("nav");

var expandMobileNavigation = function () {
    nav.classList.add("mobile-navigation-expanded");
};

var collapseMobileNavigation = function () {
    nav.classList.remove("mobile-navigation-expanded");
};

var expandButton = document.querySelector("#expand-mobile-navigation");

expandButton.addEventListener("click", expandMobileNavigation);

var collapseButton = document.querySelector("#collapse-mobile-navigation");

collapseButton.addEventListener("click", collapseMobileNavigation);

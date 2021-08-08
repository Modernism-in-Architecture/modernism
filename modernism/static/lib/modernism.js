const NAV_BURGER = document.querySelector('.navbar-burger');

const toggleBurgerMenu = () => {
    document.querySelector('.navbar-menu').classList.toggle('is-active');
    NAV_BURGER.classList.toggle('is-active');
};

const addClickEventListenerToBurgerMenu = () => {
    NAV_BURGER.addEventListener('click', toggleBurgerMenu);
};

const FILTER_ICON = document.querySelector('.filter-icon');
const addClickEventListenerToFilterIcon = () => {
    if (FILTER_ICON) {
        FILTER_ICON.addEventListener('click', event => {
            event.preventDefault();
            let filterFormContainer = document.querySelector('.filter-form');
            let filterColumn = document.querySelector('.filter-column');
            filterFormContainer.classList.toggle('is-hidden');
            filterColumn.classList.toggle('is-hidden');
            FILTER_ICON.classList.toggle('filter-on');
            let setFilterBtn = document.querySelector('.set-filter-btn');
            setFilterBtn.classList.toggle('is-hidden');
            let removeFilterBtn = document.querySelector('.remove-filter-btn');
            removeFilterBtn.classList.toggle('is-hidden');
        });
    }
};

const addClickEventListenerToDropdownLinks = () => {
    const dropdownLinksBuildings = document.querySelectorAll('.dropdown-link');
    const dropdownLinksFacts = document.querySelectorAll('.fact-dropdown-link');
    dropdownLinksBuildings.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            link.nextElementSibling.classList.toggle('show');
            if (link.children[0].classList.contains('fa-chevron-down')) {
                link.children[0].classList.replace("fa-chevron-down", "fa-chevron-up");
            } else {
                link.children[0].classList.replace("fa-chevron-up", "fa-chevron-down");
            }
        });
    });
    dropdownLinksFacts.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            if (link.children[0].children[0].classList.contains('fa-chevron-down')) {
                link.children[0].children[0].classList.replace("fa-chevron-down", "fa-chevron-up");
            } else {
                link.children[0].children[0].classList.replace("fa-chevron-up", "fa-chevron-down");
            }
            link.nextElementSibling.classList.toggle('show');
        });
    });
};

addClickEventListenerToBurgerMenu();
addClickEventListenerToDropdownLinks();
addClickEventListenerToFilterIcon();

window.onload = () => {
    const currentMenuItem = document.querySelector(".active");
    if (currentMenuItem) {
        currentMenuItem.parentElement.parentElement.classList.toggle('show');
    }
};
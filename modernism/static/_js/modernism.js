const NAV_BURGER = document.querySelector('.navbar-burger');


const toggleBurgerMenu = () => {
    document.querySelector('.navbar-menu').classList.toggle('is-active');
    NAV_BURGER.classList.toggle('is-active');
}

const addClickEventListenerToBurgerMenu = () => {
    NAV_BURGER.addEventListener('click', toggleBurgerMenu);
}

const addClickEventListenerToDropdownLinks = () => {
    const dropdownLinksBuildings = document.querySelectorAll('.dropdown-link');
    const dropdownLinksFacts = document.querySelectorAll('.fact-dropdown-link');
    dropdownLinksBuildings.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            link.nextElementSibling.classList.toggle('show');
            if (link.children[0].classList.contains('fa-chevron-down')) {
                link.children[0].classList.replace("fa-chevron-down", "fa-chevron-up");
            } else {
                link.children[0].classList.replace("fa-chevron-up", "fa-chevron-down");
            }
        });
    })
    dropdownLinksFacts.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            if (link.children[0].children[0].classList.contains('fa-chevron-down')) {
                link.children[0].children[0].classList.replace("fa-chevron-down", "fa-chevron-up");
            } else {
                link.children[0].children[0].classList.replace("fa-chevron-up", "fa-chevron-down");
            }
            link.nextElementSibling.classList.toggle('show');
        });
    })
}

addClickEventListenerToBurgerMenu();
addClickEventListenerToDropdownLinks();

window.onload = () => {
    const currentMenuItem = document.querySelector(".active")
    if (currentMenuItem) {
        currentMenuItem.parentElement.parentElement.classList.toggle('show');
    }
}
const NAV_BURGER = document.querySelector('.navbar-burger');


const toggleBurgerMenu = () => {
    document.querySelector('.navbar-menu').classList.toggle('is-active');
    NAV_BURGER.classList.toggle('is-active');
}

const addClickEventListenerToBurgerMenu = () => {
    NAV_BURGER.addEventListener('click', toggleBurgerMenu);
}

const addClickEventListenerToDropdownLinks = () => {
    const dropdownLinks = document.querySelectorAll('.dropdown-link')
    dropdownLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
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
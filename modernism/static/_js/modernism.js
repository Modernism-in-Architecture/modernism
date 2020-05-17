const NAV_BURGER = document.querySelector('.navbar-burger');

const toggleBurgerMenu = () => {
    document.querySelector('.navbar-menu').classList.toggle('is-active');
    NAV_BURGER.classList.toggle('is-active');
}

const addClickEventListenerToBurgerMenu = () => {
    NAV_BURGER.addEventListener('click', toggleBurgerMenu);
}

addClickEventListenerToBurgerMenu();
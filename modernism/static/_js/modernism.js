const NAV_BURGER = document.querySelector('.navbar-burger');

const toggleBurgerMenu = () => {
    document.querySelector('.navbar-menu').classList.toggle('is-active');
    NAV_BURGER.classList.toggle('is-active');
}

const addClickEventListenerToBurgerMenu = () => {
    NAV_BURGER.addEventListener('click', toggleBurgerMenu);
}

const FILTER_ICON = document.querySelector('.filter-icon');
const addClickEventListenerToFilterIcon = () => {
    if (FILTER_ICON) {
        FILTER_ICON.addEventListener('click', (event) => {
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
        })
    }
}

const addClickEventListenerToDropdownLinks = () => {
    const dropdownLinksBuildings = document.querySelectorAll('.dropdown-link');
    const dropdownLinksFacts = document.querySelectorAll('.fact-dropdown-link');
    dropdownLinksBuildings.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            link.nextElementSibling.classList.toggle('show');
            if (link.children[0].classList.contains('chevron-down-outline')) {
                link.children[0].classList.replace("chevron-down-outline", "chevron-up-outline");
            } else {
                link.children[0].classList.replace("chevron-up-outline", "chevron-down-outline");
            }
        });
    })
    dropdownLinksFacts.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            if (link.children[0].children[0].classList.contains('chevron-down-outline')) {
                link.children[0].children[0].classList.replace("chevron-down-outline", "chevron-up-outline");
            } else {
                link.children[0].children[0].classList.replace("chevron-up-outline", "chevron-down-outline");
            }
            link.nextElementSibling.classList.toggle('show');
        });
    })
}

addClickEventListenerToBurgerMenu();
addClickEventListenerToDropdownLinks();
addClickEventListenerToFilterIcon();

window.onload = () => {
    const currentMenuItem = document.querySelector(".active")
    if (currentMenuItem) {
        currentMenuItem.parentElement.parentElement.classList.toggle('show');
    }
}

addBackToTop({
    showWhenScrollTopIs: screen.height*2,
    diameter: 50,
    backgroundColor: '#0598f7',
    innerHTML: '<svg viewBox="0 0 24 24"><path d="M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z"/></svg>',
    textColor: '#ffffff'
})
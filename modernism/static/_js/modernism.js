let modalImageIndex = 0
let currentBuilding = {}
let galleryImages = []

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
            let filterFormContainer = document.querySelector('.filter-form')
            filterFormContainer.classList.toggle('is-hidden');
            let setFilterBtn = document.querySelector('.set-filter-btn')
            setFilterBtn.classList.toggle('is-hidden');
            let removeFilterBtn = document.querySelector('.remove-filter-btn')
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

const addClickEventListenerToBuildingImages = () => {
    const previewImageBuildings = document.querySelectorAll('.preview-image');

    previewImageBuildings.forEach(image => {
        image.addEventListener('click', (event) => {
            event.preventDefault();
            let imageModal = document.getElementById("image-modal");
            let large_image = document.getElementById("modal-image");
            let description = document.getElementById("image-description");
            let photographer = document.getElementById("image-photographer");
            if (!imageModal.classList.contains("is-active")) {
                imageModal.classList.toggle("is-active");
                large_image.src = image.getAttribute("large-url");
                modalImageIndex = image.getAttribute("index");
                imgData = galleryImages[modalImageIndex];
                if (imgData) {
                    description.innerText = imgData["value"]["description"]
                    photographer.innerText = imgData["value"]["photographer"] ? "Photo by " + imgData["value"]["photographer"] : ""
                }
            }
        });
    })
}

const addClickEventListenerToModalCloseButton = () => {
    let closeButton = document.getElementById("close-button");
    if (closeButton) {
        closeButton.addEventListener('click', (event) => {
            event.preventDefault();
            let imageModal = document.getElementById("image-modal");
            if (imageModal.classList.contains("is-active")) {
                imageModal.classList.toggle("is-active");
            }
        });
    }

}

const setModalImage = (direction) => {
    let largeImage = document.getElementById("modal-image");
    let description = document.getElementById("image-description");
    let photographer = document.getElementById("image-photographer");
    let imgData = {};
    let imgUrl = "";

    if (direction == "next") {
        modalImageIndex = parseInt(modalImageIndex) + 1;
        if (modalImageIndex > galleryImages.length - 1) {
            modalImageIndex = 0;
        }

    }
    if (direction == "prev") {
        modalImageIndex = parseInt(modalImageIndex) - 1;
        if (modalImageIndex < 0) {
            modalImageIndex = galleryImages.length - 1;
        }
    }

    imgData = galleryImages[modalImageIndex];
    if (imgData) {
        imgUrl = imgData["value"]["image"]["large"]["src"]
        largeImage.src = imgUrl;
        description.innerText = imgData["value"]["description"]
        photographer.innerText = imgData["value"]["photographer"] ? "Photo by " + imgData["value"]["photographer"] : ""
    }

}


addClickEventListenerToBurgerMenu();
addClickEventListenerToDropdownLinks();
addClickEventListenerToBuildingImages();
addClickEventListenerToModalCloseButton();
addClickEventListenerToFilterIcon();

window.onload = () => {
    const currentMenuItem = document.querySelector(".active")
    if (currentMenuItem) {
        currentMenuItem.parentElement.parentElement.classList.toggle('show');
    }
}

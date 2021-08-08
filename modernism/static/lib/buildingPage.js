let modalImageIndex = 0;
let currentBuilding = {};
let galleryImages = [];

async function getBuildingObject() {
    if (pageId) {
        let response = await fetch(window.location.origin + "/api/v2/pages/" + pageId + "/");
        let data = await response.json();
        currentBuilding = data;
        galleryImages = data["gallery_images"];
    }
}

const addClickEventListenerToBuildingImages = () => {
    const previewImageBuildings = document.querySelectorAll('.preview-image');

    previewImageBuildings.forEach(image => {
        image.addEventListener('click', event => {
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
                    description.innerText = imgData["value"]["description"];
                    photographer.innerText = imgData["value"]["photographer"] ? "Photo by " + imgData["value"]["photographer"] : "";
                }
            }
        });
    });
};

const setModalImage = direction => {
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
        imgUrl = imgData["value"]["image"]["large"]["src"];
        largeImage.src = imgUrl;
        description.innerText = imgData["value"]["description"];
        photographer.innerText = imgData["value"]["photographer"] ? "Photo by " + imgData["value"]["photographer"] : "";
    }
};

const addClickEventListenerToModalCloseButton = () => {
    let closeButton = document.getElementById("close-button");
    if (closeButton) {
        closeButton.addEventListener('click', event => {
            event.preventDefault();
            let imageModal = document.getElementById("image-modal");
            if (imageModal.classList.contains("is-active")) {
                imageModal.classList.toggle("is-active");
            }
        });
    }
};

getBuildingObject();
addClickEventListenerToBuildingImages();
addClickEventListenerToModalCloseButton();
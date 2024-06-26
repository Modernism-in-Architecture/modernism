const markers = L.markerClusterGroup({
    spiderfyOnMaxZoom: false,
    showCoverageOnHover: false,
});
const map = L.map('mapBuilding');

let modalImageIndex= 0;
let galleryImages= {};

const customIcon = new L.Icon({
        iconUrl: staticUrl + "img/marker.png",
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [40, 40],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
});

const customSingleIcon = new L.Icon({
        iconUrl: staticUrl + "img/marker_single.png",
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [40, 40],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
});

const setUpMap = () => {
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        useCache: true
    }).addTo(map);

    L.marker([buildingLat, buildingLong], { icon: customSingleIcon }).addTo(map)
    map.setView([buildingLat, buildingLong], 15)
}

const addClickEventListenerToBuildingImages = () => {
    const previewImageBuildings = document.querySelectorAll('.preview-image');

    previewImageBuildings.forEach(image => {

        galleryImages[image.getAttribute("index")] =
        {
            largeUrl: image.getAttribute("large-url"),
            description: image.getAttribute("description"),
            photographer: image.getAttribute("photographer"),
        }
        image.addEventListener('click', (event) => {
            // event.preventDefault();
            let imageModal = document.getElementById("image-modal");
            let large_image = document.getElementById("modal-image");
            let description = document.getElementById("image-description");
            let photographer = document.getElementById("image-photographer");

            if (!imageModal.classList.contains("is-active")) {
                large_image.src = image.getAttribute("large-url");
                modalImageIndex = image.getAttribute("index");
                description.innerText = image.getAttribute("description");
                photographer.innerText = image.getAttribute("photographer");
            }
            imageModal.classList.toggle("is-active");
        });
    });
}

const setModalImage = (direction) => {
    let largeImage = document.getElementById("modal-image");
    let description = document.getElementById("image-description");
    let photographer = document.getElementById("image-photographer");
    let imgData = {};

    if (direction === "next") {
        modalImageIndex = parseInt(modalImageIndex) + 1;
        if (modalImageIndex > Object.keys(galleryImages).length - 1) {
            modalImageIndex = 0;
        }

    }
    if (direction === "prev") {
        modalImageIndex = parseInt(modalImageIndex) - 1;
        if (modalImageIndex < 0) {
            modalImageIndex = Object.keys(galleryImages).length - 1;
        }
    }

    imgData = galleryImages[modalImageIndex];
    if (imgData) {
        largeImage.src = imgData["largeUrl"];
        description.innerText = imgData["description"];
        photographer.innerText = imgData["photographer"] ? "Photo by " + imgData["photographer"] : "";
    }
}

const addClickEventListenerToModalCloseButton = () => {
    let closeButton = document.getElementById("close-button");
    if (closeButton) {
        closeButton.addEventListener('click', (event) => {
            event.preventDefault();
            let imageModal = document.getElementById("image-modal");
            imageModal.classList.toggle("is-active");
        });
    }
}

const addBuildingsOfCityToMap = () => {

    for (let i = 0; i < buildingsOfTheCityData.length; i++) {
        let cityBuilding = buildingsOfTheCityData[i];

        if (cityBuilding.fields.latitude === buildingLat && cityBuilding.fields.longitude === buildingLong) {
            continue;
        }

        let cityBuildingURL = window.location.href.replace(buildingSlug, cityBuilding.fields.slug)
        let marker = L.marker([cityBuilding.fields.latitude, cityBuilding.fields.longitude], { icon: customIcon });
        marker.bindPopup(
            '<a href=' + cityBuildingURL + '><p>' + cityBuilding.fields.name + ",<br>" + cityBuilding.fields.address + '</p></a>'
        ).openPopup();
        markers.addLayer(marker);
        map.addLayer(markers);
    }
}

const addClickEventListenerToAccordions = () => {

    let historyHead = document.getElementById("history");
    let descriptionHead = document.getElementById("description");
    let sourceHead = document.getElementById("source");
    let descriptionContent = document.getElementById("description-content");
    let historyContent = document.getElementById("history-content");
    let sourceContent = document.getElementById("source-content");

    historyHead.addEventListener('click', (event) => {
            historyContent.classList.toggle("is-sr-only");
        }
    );
    descriptionHead.addEventListener('click', (event) => {
            descriptionContent.classList.toggle("is-sr-only");
        }
    );
    sourceHead.addEventListener('click', (event) => {
            sourceContent.classList.toggle("is-sr-only");
        }
    );
}


setUpMap();
addBuildingsOfCityToMap();
addClickEventListenerToBuildingImages();
addClickEventListenerToModalCloseButton();
addClickEventListenerToAccordions();

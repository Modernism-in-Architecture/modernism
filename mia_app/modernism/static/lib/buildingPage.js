const pageURL = window.location.origin + "/api/v2/pages/";
const buildingsOfCityURL = window.location.origin + "/api/v2/pages?type=buildings.BuildingPage&fields=lat_long,name,address&city=";
const map = L.map('mapBuilding');
const markers = L.markerClusterGroup();
let modalImageIndex = 0;
let currentBuilding = {};
let galleryImages = [];
let latlongOfFeaturedBuilding = buildingLatLong.split(",");
let lat = latlongOfFeaturedBuilding[0].trim();
let long = latlongOfFeaturedBuilding[1].trim();

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> Contributers',
    'useCache': true
}).addTo(map);

const greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

L.marker([lat, long], { icon: greenIcon }).addTo(map);
map.setView([lat, long], 12);

const fetchData = async (url, limit, offset) => {
    try {
        let apiResponse = await fetch(url + "&offset=" + offset + "&limit=" + limit);
        let data = await apiResponse.json();
        return data;
    } catch (e) {
        return console.error(e);
    }
};

const getBuildingsOfCity = async () => {
    if (!cityId) {
        return;
    }
    let url = buildingsOfCityURL + cityId;
    let limit = 50;
    let offset = 0;
    let buildingData = [];
    let totalCount = 0;

    let apiData = await fetchData(url, limit, offset);
    totalCount = apiData.meta.total_count;
    buildingData = [...apiData.items, ...buildingData];

    while (buildingData.length < totalCount) {
        offset = offset + limit;
        apiData = await fetchData(url, limit, offset);
        buildingData = [...apiData.items, ...buildingData];
    }
    return buildingData;
};

const getBuildingObject = async () => {
    if (pageId) {
        let response = await fetch(pageURL + pageId + "/");
        let data = await response.json();
        currentBuilding = data;
        galleryImages = data["gallery_images"];
    }
};

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

const addBuildingsOfCityToMap = () => {
    getBuildingsOfCity().then(buildings => {
        for (let i = 0; i < buildings.length; i++) {
            let coord = [];
            let langLong = buildings[i].lat_long.split(",");
            if (langLong[0] == latlongOfFeaturedBuilding[0] && langLong[1] == latlongOfFeaturedBuilding[1]) {
                continue;
            }
            coord.push(langLong[0]);
            coord.push(langLong[1]);
            let marker = L.marker(coord);
            marker.bindPopup('<a href=' + window.location.origin + '/buildings/' + buildings[i].meta.slug + '><p>' + buildings[i].name + ",<br>" + buildings[i].address + '</p></>').openPopup();
            markers.addLayer(marker);
            map.addLayer(markers);
        }
    });
};

getBuildingObject();
addBuildingsOfCityToMap();
addClickEventListenerToBuildingImages();
addClickEventListenerToModalCloseButton();
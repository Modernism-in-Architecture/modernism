let zoomLevel;

if (document.documentElement.clientWidth >= 1400) {
    // Large screens
    zoomLevel = 5;
} else {
    // small devices and laptops
    zoomLevel = 4
}

const mapMia = L.map('mapMia').setView([51.339642, 12.374462], zoomLevel);
const markers = L.markerClusterGroup({ maxClusterRadius: 20 });

const setUpMap = () => {
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> Contributers',
        'useCache': true
    }).addTo(mapMia);
}

const addBuildingsToMap = () => {
    for (let i = 0; i < mapBuildings.length; i++) {
        let building = mapBuildings[i];
        let buildingURL = window.location.href.replace("map/", "buildings/" + building.fields.slug)
        let marker = L.marker([building.fields.latitude, building.fields.longitude]);
        marker.bindPopup(
            '<a href=' + buildingURL + '><p>' + building.fields.name + ",<br>" + building.fields.address + '</p></a>'
        ).openPopup();
        markers.addLayer(marker);
        mapMia.addLayer(markers);
    }
};

setUpMap();
addBuildingsToMap();
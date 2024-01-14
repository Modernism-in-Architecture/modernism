const zoomLevel = document.documentElement.clientWidth >= 1400 ? 5 : 4;

const customIcon = new L.Icon({
    iconUrl: staticUrl + "img/marker.png",
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [40, 40],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const markers = L.markerClusterGroup({
    maxClusterRadius: 35,
    spiderfyOnMaxZoom: false,
	showCoverageOnHover: false,
});

const mapMia = L.map('mapMia').setView([51.339642, 12.374462], zoomLevel);

const setUpMap = () => {
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        useCache: true
    }).addTo(mapMia);
}

const addBuildingsToMap = () => {
    for (let i = 0; i < mapBuildings.length; i++) {
        let building = mapBuildings[i];
        let buildingURL = window.location.href.replace("map/", "buildings/" + building.fields.slug)
        let marker = L.marker([building.fields.latitude, building.fields.longitude], { icon: customIcon });
        marker.bindPopup(
            '<a href=' + buildingURL + '><p>' + building.fields.name + ",<br>" + building.fields.address + '</p></a>'
        ).openPopup();
        markers.addLayer(marker);
        mapMia.addLayer(markers);
    }
};

setUpMap();
addBuildingsToMap();

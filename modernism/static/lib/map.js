const map = L.map('mapid').setView([51.339642, 12.374462], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> Contributers',
    'useCache': true
}).addTo(map);

const markers = L.markerClusterGroup();

async function getBuildingData() {
    let response = await fetch(window.location.origin + "/api/v2/pages/?type=buildings.BuildingPage&fields=*");
    let data = await response.json();
    return data;
}
getBuildingData().then(data => {
    let buildings = data.items;
    for (let i = 0; i < buildings.length; i++) {
        let coord = [];
        let langLong = buildings[i].lat_long.split(",");
        coord.push(langLong[0]);
        coord.push(langLong[1]);
        markers.addLayer(L.marker(coord));
        map.addLayer(markers);
    }
});
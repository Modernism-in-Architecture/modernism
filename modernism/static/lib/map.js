const map = L.map('mapid').setView([51.339642, 12.374462], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> Contributers',
    'useCache': true
}).addTo(map);

const markers = L.markerClusterGroup();

async function getBuildingData() {
    let response = await fetch(window.location.origin + "/api/v2/pages/?type=buildings.BuildingPage&fields=*&limit=100");
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
        let marker = L.marker(coord);
        marker.bindPopup('<a href=' + buildings[i].meta.html_url + '><p>' + buildings[i].name + ",<br>" + buildings[i].address + '</p></>').openPopup();
        markers.addLayer(marker);
        map.addLayer(markers);
    }
});
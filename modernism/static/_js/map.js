const map = L.map('mapid').setView([51.339642, 12.374462], 6);
const markers = L.markerClusterGroup();
const buildingDataURL = window.location.origin + "/api/v2/pages/?type=buildings.BuildingPage&fields=-gallery_images,lat_long,name,address";

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> Contributers',
    'useCache': true
}).addTo(map);

async function fetchData(url, limit, offset) {
    try {
        let apiResponse = await fetch(url + "&offset=" + offset + "&limit=" + limit);
        let data = await apiResponse.json();
        return data;
    } catch (e) {
        return console.error(e);
    }
}

async function getBuildingData() {
    let url = buildingDataURL;
    let limit = 50;
    let offset = 0;
    let buildingData = [];
    let totalCount = 0;

    let apiData = await fetchData(url, limit, offset)

    totalCount = apiData.meta.total_count
    buildingData = [...apiData.items, ...buildingData]

    while (buildingData.length < totalCount) {
        offset = offset + limit;
        apiData = await fetchData(url, limit, offset)
        buildingData = [...apiData.items, ...buildingData]
    }
    return buildingData;
}

getBuildingData().then(buildings => {
    for (let i = 0; i < buildings.length; i++) {
        let coord = [];
        let langLong = buildings[i].lat_long.split(",")
        coord.push(langLong[0]);
        coord.push(langLong[1]);
        let marker = L.marker(coord);
        marker.bindPopup('<a href=' + window.location.origin + '/buildings/' + buildings[i].meta.slug + '><p>' + buildings[i].name + ",<br>" + buildings[i].address + '</p></>').openPopup();
        markers.addLayer(marker);
        map.addLayer(markers);
    }
});


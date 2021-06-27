async function getBuildingObject() {
    if (pageId) {
        let response = await fetch(window.location.origin + "/api/v2/pages/" + pageId + "/");
        let data = await response.json();
        currentBuilding = data;
        galleryImages = data["gallery_images"];
    }

}

getBuildingObject();
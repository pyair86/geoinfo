const map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        })
    ],
    view: new ol.View({
        projection: 'EPSG:4326',
        center: [9.2823054705243, 47.38591365135608],
        zoom: 7
    })
});


function addPopup() {
    const popup = new ol.Overlay({
        element: document.getElementById('popup'),
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    });

    map.addOverlay(popup);
    return popup;
}

function setPopupCloser() {
    const popupCloser = document.getElementById('popup-closer');

    popupCloser.addEventListener('click', function() {
        popup.setPosition(undefined);
        popupCloser.blur();
        return false;
    });
}


function getPoints() {
    fetch('/points')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            const vectorSource = new ol.source.Vector({
                features: new ol.format.GeoJSON().readFeatures(data)
            });

            const vectorLayer = new ol.layer.Vector({
                source: vectorSource
            });

            map.addLayer(vectorLayer);
            if (isFinite(vectorSource.getExtent()[0])) {
                map.getView().fit(vectorSource.getExtent(), {
                    padding: [50, 50, 50, 50],
                    maxZoom: 7
                });
            }
        });
}

function handlePopup(popup) {
    map.on('click', function(event) {
        const feature = map.forEachFeatureAtPixel(event.pixel, function(feature) {
            return feature;
        });
        if (feature) {
            const geometry = feature.getGeometry();
            const coordinate = geometry.getCoordinates();
            const attributes = feature.getProperties();

            let content = '<div style="background-color: #f7f7f7; padding: 10px;">';
            for (const key in attributes) {
                if (key !== 'geometry') {
                    content += '<strong>' + key + ':</strong> ' + attributes[key] + '<br>';
                }
            }
            content += '</div>';

            document.getElementById('popup-content').innerHTML = content;
            popup.setPosition(coordinate);
        } else {
            popup.setPosition(undefined);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    getPoints();
    popup = addPopup();
    setPopupCloser();
    handlePopup(popup);
}, false);
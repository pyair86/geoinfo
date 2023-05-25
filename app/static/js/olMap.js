  const map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM() // OpenStreetMap as the base layer
      })
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([9.2823054705243, 47.38591365135608]), // Set the initial center coordinates
      zoom: 8 // Set the initial zoom level
    })
  });

  const popup = new ol.Overlay({
    element: document.getElementById('popup'),
    autoPan: true,
    autoPanAnimation: {
      duration: 250
    }
  });

  map.addOverlay(popup);

  const popupCloser = document.getElementById('popup-closer');

  popupCloser.addEventListener('click', function() {
    popup.setPosition(undefined);
    popupCloser.blur();
    return false;
  });

  map.on('click', function(evt) {
    var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
      return feature;
    });

    if (feature) {
      var coordinate = evt.coordinate;
      var popupContent = document.getElementById('popup-content');
      popupContent.innerHTML = '<p>You clicked on the point!</p>';
      popup.setPosition(coordinate);
    }
  });

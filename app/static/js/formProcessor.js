    document.getElementById('geomForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const long = parseFloat(document.getElementById('long').value.substr(0,21));
    const lat = parseFloat(document.getElementById('lat').value.substr(0,20));
    const name = document.getElementById('pointName').value.substr(0,30)

    if (isNaN(long) || isNaN(lat)) {
      alert('Invalid long or lat. Please enter numeric values.');
      return;
    }

    function CoordinateIsOutOfRange(coordinate, degree){
      return coordinate < -degree || coordinate > degree
    }

    const latLimitDegrees = 180;
    const longLimitDegrees = 90;

    if (CoordinateIsOutOfRange(lat, latLimitDegrees) || CoordinateIsOutOfRange(long, longLimitDegrees)) {
      alert('Invalid long or lat. Out of range.');
      return;
    }

    async function postData(url, data) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error('Error occurred during POST request');
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error);
    throw error;
  }
}


const data = {
  lat: lat,
  long: long,
  name: name
};

postData('/add_point', data)
  .then(response => {
    console.log(response);
    // Process the response here
     fetch('/points')
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {

                // Create an OpenLayers vector layer with the GeoJSON data
                var vectorSource = new ol.source.Vector({
                    features: new ol.format.GeoJSON().readFeatures(data)
                });

                var vectorLayer = new ol.layer.Vector({
                    source: vectorSource
                });
                // Add the vector layer to the map
                map.addLayer(vectorLayer);
                // Fit the map view to the extent of the vector layer
                map.getView().fit(vectorSource.getExtent(), {
                    padding: [50, 50, 50, 50],
                    maxZoom: 15
                });
            });
  })
  .catch(error => {
    console.error(error);
    // Handle the error here
  });

    document.getElementById('geomForm').reset();
  });



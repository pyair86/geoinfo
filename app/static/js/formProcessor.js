    document.getElementById('geomForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const long = parseFloat(document.getElementById('long').value.substr(0,21));
    const lat = parseFloat(document.getElementById('lat').value.substr(0,20));

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

    addPoint(long, lat);

    document.getElementById('geomForm').reset();
  });

  function addPoint(latitude, longitude) {
    // Implement your logic to add a point with the provided latitude and longitude
    // You can use this function to make an AJAX request to your server or update your application's data model
    console.log( 'Adding point: Latitude ' + String(lat) + ', Longitude ' + String(long) );
  }
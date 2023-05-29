function validateCoordinateWithinRange(coordinate, degree) {
    if (coordinate < -degree || coordinate > degree) {
        alert('coordinate is out of range.');
        throw new Error('coordinate is out of range.');
    }
}


function validateCoordinateValidDataType(long, lat) {
    if (isNaN(long) || isNaN(lat)) {
        alert('Invalid long or lat. Please enter numeric values.');
        throw new Error('Invalid long or lat. Please enter numeric values.');
    }
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

document.getElementById('geomForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const long = parseFloat(document.getElementById('long').value.substr(0, 21));
    const lat = parseFloat(document.getElementById('lat').value.substr(0, 20));
    const name = document.getElementById('pointName').value.substr(0, 30);

    validateCoordinateValidDataType(long, lat);

    const latLimitDegrees = 90;
    const longLimitDegrees = 180;

    validateCoordinateWithinRange(lat, latLimitDegrees);
    validateCoordinateWithinRange(long, longLimitDegrees);

    const data = {
        lat: lat,
        long: long,
        name: name
    };

    postData('/add_point', data)
        .then(response => {
            console.log(response);
            getPoints();
        })
        .catch(error => {
            console.error(error);
            throw new Error('Error occurred...');
        });
    document.getElementById('geomForm').reset();
});
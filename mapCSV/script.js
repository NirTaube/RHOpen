// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Parse the CSV file using Papa Parse library
    Papa.parse('sales.csv', {
        header: true,
        download: true,
        complete: function(results) {
            var salesData = results.data; // Contains the parsed CSV data

            // Call a function to create and populate the map with markers
            createMap(salesData);
        }
    });

    function createMap(salesData) {
        // Create the map centered on the USA
        var map = L.map('map').setView([37.8, -96], 4);
    
        // Add the OpenStreetMap tile layer to the map
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
        }).addTo(map);
    
        // Create a marker cluster group
        var markers = L.markerClusterGroup();
    
        // Loop through the sales data and add markers to the marker cluster group
        for (var i = 0; i < salesData.length; i++) {
            var location = salesData[i].LOCATION;
            var latitude = parseCoordinate(salesData[i].Latitude);
            var longitude = parseCoordinate(salesData[i].Longitude);
            var netSales = salesData[i].Net_Sales;
    
            // Create a marker with a popup for each location
            var marker = L.marker([latitude, longitude])
                .bindPopup(`<strong>${location}</strong><br>Net Sales: ${netSales}`)
                .addTo(markers);
    
            // Add the marker to the marker cluster group
            markers.addLayer(marker);
        }
    
        // Add the marker cluster group to the map
        map.addLayer(markers);
    }
    
    function parseCoordinate(coordinate) {
        var parts = coordinate.split(' ');
        var value = parseFloat(parts[0]);
        var direction = parts[1];
    
        // Convert to negative value for western and southern hemisphere
        if (direction === 'S' || direction === 'W') {
            value = -value;
        }
    
        return value;
    }
});    
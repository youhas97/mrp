<template>
    <div class="Map"/>
</template>


<script>
import gmapsInit from '../utils/gmaps.js'

let positionTimer;

function handleLocationError(browserHasGeolocation, infoWindow, pos, map) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ? 'Error: Geolocation misslyckades!' : 'Error: Din webbläsare stödjer inte geolocation');
    infoWindow.open(map);
}

function geoLocate(map, infoWindow){
    navigator.geolocation.getCurrentPosition(function(position) {
         let pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        infoWindow.setPosition(pos);
        infoWindow.setContent('Här är du.');
        infoWindow.open(map);
        map.setCenter(pos);
        return position;
    }, function() {
        // Geolocation ej tillåtet
        handleLocationError(true, infoWindow, map.getCenter(), map);
    });
}

function sendPostition(pos){
    // Skriv kod här som skickar "position" till backend
}

function watchCurrentPosition(infoWindow){
    positionTimer = navigator.geolocation.watchPosition(
        function(position){
            let pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            infoWindow.setPosition(pos);
            sendPostition(pos);
        }
    ,null,
    {
        enableHighAccuracy: false,
        timeout: 5000,
        maximumAge: Infinity
    });
}

export default {
    name: 'Map',
    async mounted() {
        const google = await gmapsInit();
        const geocoder = new google.maps.Geocoder();
        const map = new google.maps.Map(this.$el);

        geocoder.geocode({address: 'Arboga'}, (results, status) =>{
            if (status !== 'OK' || !results[0]){
                throw new Error(status);
            }
        
        map.setCenter(results[0].geometry.location);
        map.fitBounds(results[0].geometry.viewport);

        let infoWindow = new google.maps.InfoWindow;
        
        if(navigator.geolocation){
            let position = geoLocate(map, infoWindow);
            watchCurrentPosition(infoWindow, position);
            var marker = new google.maps.Marker({
                position: position,
                map: map,
                title: 'Hello World!',
                icon: 'https://maps.google.com/mapfiles/kml/shapes/info-i_maps.png',
            });
            /*navigator.geolocation.getCurrentPosition(function(position) {
                let pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                infoWindow.setPosition(pos);
                infoWindow.setContent('Här är du.');
                infoWindow.open(map);
                map.setCenter(pos);
            }, function() {
                // Geolocation ej tillåtet
                handleLocationError(true, infoWindow, map.getCenter(), map);
            });*/
        } else {
            // Geolocation ej activerat
            handleLocationError(false, infoWindow, map.getCenter(), map);
        }
        });
    },
};
</script>

<style>
    html,
    body{
        margin: 0;
        padding: 0;
    }    
    .Map{
        width: 100vw;
        height: 100vh;
    }
</style>

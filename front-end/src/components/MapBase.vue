<template>
    <div class="Map"/>
</template>

<script>
import gmapsInit from '../utils/gmaps.js'

export default {
    name: 'Map',
    data: function() {
        return {
            alert_on: false,
        }
    },
    async mounted() {
        const google = await gmapsInit();
        const geocoder = new google.maps.Geocoder();
        const map = new google.maps.Map(this.$el);

        geocoder.geocode({address: 'Sverige'}, (results, status) =>{
            if (status !== 'OK' || !results[0]){
                throw new Error(status);
            }
        
        map.setCenter(results[0].geometry.location);
        map.fitBounds(results[0].geometry.viewport);

        let infoWindow = new google.maps.InfoWindow;
        
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(function(position) {
                let pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                var image = "http://maps.google.com/mapfiles/ms/icons/police.png";
                
                var marker = new google.maps.Marker({
                    position: pos,
                    title: "location",
                    icon: image
                })
                marker.setMap(map);
                /*
                infoWindow.setPosition(pos);
                infoWindow.setContent('Här är du.');
                infoWindow.open(map);
                */

                map.setCenter(pos);
            }, function() {
                handleLocationError(true, infoWindow, map.getCenter());
            });
        } else {
            // Geolocation ej activerat
            handleLocationError(false, infoWindow, map.getCenter());
        }
        function handleLocationError(browserHasGeolocation, infoWindow, pos) {
            infoWindow.setPosition(pos);
            infoWindow.setContent(browserHasGeolocation ? 'Error: Geolocation misslyckades!' : 'Error: Din webbläsare stödjer inte geolocation');
            infoWindow.open(map);
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

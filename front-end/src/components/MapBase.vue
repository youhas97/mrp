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
            needBackUp: false
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

                var image = "https://img.icons8.com/color/48/000000/filled-circle.png";

                var marker = new google.maps.Marker({
                    title: "location",
                    map:map,
                    icon:image})
                var needBackUp=true;
                if(needBackUp){
                    var alert = {
                        url: "https://img.icons8.com/flat_round/64/000000/error.png",
                        scaledSize: new google.maps.Size(35,35)
                    }
                    marker.setIcon(alert);
                    marker.setAnimation(google.maps.Animation.BOUNCE)
                }
                else{
                    var blueDot = {
                        url: "https://img.icons8.com/color/48/000000/filled-circle.png",
                        scaledSize: new google.maps.Size(25,25)
                    }
                    marker.setIcon(blueDot);
                }

                marker.setPosition(pos);
                marker.addListener()

                map.setCenter(pos);
                map.setZoom(15);

                //google.maps.event.addDomListener(window, 'load', initialize);

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
      //google.maps.event.addDomListener(window, 'load', tempFunc);

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
    img[src^='http://www.google.com/mapfiles/marker.png?i=']{opacity: 0.5};
</style>

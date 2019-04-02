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

function geoGoal(map, goalWindow, results){
        let pos = results[0].geometry.location;
        
        goalWindow.setPosition(pos);
        goalWindow.setContent('Här ska du.');
        goalWindow.open(map);
        map.setCenter(pos);
        
    }


function sendPostition(pos){
    // Skriv kod här som skickar "position" till backend som packar det i en lista new_pos.
}


function recievePosition(listfrombackend){
    // tar emot new_list
    listfrombackend = [];
    curpos = listfrombackend;
}

/*
Får lista med nya positioner från backend.
Om första loop sätt new_list till old_list

Får lista med nya positioner från backend,
jämnför alla person-objekt om de har nya pos.
Updatera alla person-objekts positioner, genom
att sätta old_pos till new_pos om det skiljer sig,
annars do nothing.

Sedan sätt new_list till old_list.

Repeat

[[person1],[person2],[person3],[person4]]


[person1] = ["id", "(lat, long)", "namn", "grupp#"]


*/

/*
function watchOtherPosition(oldpos){   

    if(!oldpos){
        
    } else{
        //nån typ av loop
        person_1_old_pos = oldpos[0].getpos;
        person_1_cur_pos = curpos[0].getpos;


        if(person_1_old_pos == person_1_cur_pos){
            return 0;
        } else {
            person_1.setPos(person_1_cur_pos);
            
        }

    } 
    
}
*/


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
            
        let goal_loc;

         geocoder.geocode({address: 'Linköpings Universitet'}, (results_goal, status_goal) =>{
            if (status_goal !== 'OK' || !results_goal[0]){
                throw new Error(status_goal);
            }
            goal_loc = results_goal            
         });

        
        
        map.setCenter(results[0].geometry.location);
        map.fitBounds(results[0].geometry.viewport);

        let infoWindow = new google.maps.InfoWindow;
        let goalWindow = new google.maps.infoWindow;

        if(navigator.geolocation){
            let position = geoLocate(map, infoWindow);
            geoGoal(map,goalWindow,goal_loc);
            watchCurrentPosition(infoWindow, position);
            //update watchOtherPosition
            
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

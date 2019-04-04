<template>
    <div class="Map"/>
</template>


<script>
import gmapsInit from '../utils/gmaps.js'

let google;
let positionTimer;
let markerList = [];
let meObj = ["1234", {lat: 58, lng: 15}, "Joakim", "11", false];
let JLObj = ["6363", {lat: 58.3960254, lng: 15.58599}, "Jacob", "11", false];
let YHObj = ["1241234", {lat: 58.4128164, lng: 15.5586258}, "Yousef", "12", false];
let VBObj = ["98484", {lat: 58.4090253, lng: 15.59499}, "Viktor", "12", false];

let testlist = [JLObj,YHObj,VBObj];

function handleLocationError(browserHasGeolocation, marker, pos, map) {
    marker.setPosition(pos);
    marker.setContent(browserHasGeolocation ? 'Error: Geolocation misslyckades!' : 'Error: Din webbläsare stödjer inte geolocation');
    marker.open(map);
}

function geoLocate(map, marker){
    navigator.geolocation.getCurrentPosition(function(position) {
         let pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        marker.setPosition(pos);
        marker.setMap(map);
        marker.setLabel("Jag");
        marker.setIcon({ url:"http://maps.google.com/mapfiles/ms/icons/red-dot.png"});
        //marker.setContent('Här är du.');
        //marker.open(map);
        map.setCenter(pos);
        return position;
    }, function() {
        // Geolocation ej tillåtet
        handleLocationError(true, marker, map.getCenter(), map);
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


[person1] = ["id", "(lat, long)", "namn", "grupp#", "callingHelp"]


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


function watchCurrentPosition(marker){
    positionTimer = navigator.geolocation.watchPosition(
        function(position){
            let pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            marker.setPosition(pos);
            sendPostition(pos);
        }
    ,null,
    {
        enableHighAccuracy: false,
        timeout: 5000,
        maximumAge: Infinity
    });
}

function socketSetup(map){
    var socket = new WebSocket('ws://127.0.0.1:8080/ws/connect/');

        socket.onmessage = function(event) {
            var data = JSON.parse(event.data);
            // If message is of 'gps' type then parse the data and distribute the new markers
            if(data['type'] == 'gps'){
                markerList = [];
                for(let i = 0; i < data['gpslist'].length(); i++){
                    let personObj = data['gpslist'][i];
                    let marker = new google.maps.Marker({
                        position: personObj.pos,
                        map: map,
                        label: personObj.name
                    });
                    markerList.push(marker);
                }
            } else {
                alert('GPS data is unavailable');
            }
        };

        }

export default {
    

    

    name: 'Map',
    async mounted() {
        google = await gmapsInit();
        const geocoder = new google.maps.Geocoder();
        const map = new google.maps.Map(this.$el);
        socketSetup(map);
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

        let marker = new google.maps.Marker;
        let goalWindow = new google.maps.InfoWindow;

        if(navigator.geolocation){
            let position = geoLocate(map, marker);
            //geoGoal(map,goalWindow,goal_loc);
            watchCurrentPosition(marker, position);
            let i=0;
            testlist.forEach(function(){
                 /* eslint-disable no-console */
                console.log("username:");
                console.log("pw:", markerList);
                /* eslint-enable no-console */
                let marker3 = new google.maps.Marker;
                marker3.setIcon({ url:"http://maps.google.com/mapfiles/ms/icons/red-dot.png"});
                if(testlist[i][3] != meObj[3]){
                    marker3.setIcon({ url:"http://maps.google.com/mapfiles/ms/icons/blue-dot.png"});
                }
                marker3.setPosition(testlist[i][1]);
                marker3.setMap(map);
                marker3.setLabel(testlist[i][2]);
                markerList.push(marker3);
                i++;
            });
        } else {
            // Geolocation ej activerat
            handleLocationError(false, marker, map.getCenter(), map);
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

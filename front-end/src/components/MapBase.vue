<template>
    <div class="Map"/>
</template>


<script>
import gmapsInit from '../utils/gmaps.js'

let google;
let positionTimer;
let markerList = [];
let personList = [];
let app;
let meObj = {
    "id": null,
    "pos": null,
    "name": null,
    "group": null,
    "needHelp": null
}
let meObjtest = ["1234", {lat: 58, lng: 15}, "Joakim", "11", false];
let testlist = [];
let JLObj = ["6363", {lat: 58.3960254, lng: 15.58599}, "Jacob", "11", false];
let YHObj = ["1241234", {lat: 58.4128164, lng: 15.5586258}, "Yousef", "12", true];
let VBObj = ["98484", {lat: 58.4090253, lng: 15.59499}, "Viktor", "12", true];

function handleLocationError(browserHasGeolocation, marker, pos, map) {
    //marker.setPosition(pos);
    //marker.setContent(browserHasGeolocation ? 'Error: Geolocation misslyckades!' : 'Error: Din webbläsare stödjer inte geolocation');
    //marker.open(map);
}

function geoLocate(map, marker){
    navigator.geolocation.getCurrentPosition(function(position) {
         let pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        marker.setPosition(pos);
        marker.setMap(map);
        marker.setLabel(meObj.name);
        marker.setIcon({ url:"http://maps.google.com/mapfiles/ms/icons/red-dot.png"});
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
}

export default {
    name: 'Map',
    async mounted() {
        google = await gmapsInit();
        const geocoder = new google.maps.Geocoder();
        const map = new google.maps.Map(this.$el);
        meObj = this.$store.state.meObj;
        app = this;
        this.recieveMessage(map);
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
            this.watchCurrentPosition(marker);
            let i=0;
            testlist.forEach(function(){
                let marker3 = new google.maps.Marker;
                marker3.setIcon({ url:"http://maps.google.com/mapfiles/ms/icons/red-dot.png"});
                if(testlist[i] != meObj[3]){
                    marker3.setIcon({ url:"http://maps.google.com/mapfiles/ms/icons/blue-dot.png"});
                }
                if(testlist[i][4]){
                    marker3.setIcon({ url:"https://img.icons8.com/flat_round/64/000000/error.png",
                                      scaledSize: new google.maps.Size(30,30)});
                    marker3.setAnimation(google.maps.Animation.BOUNCE)

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
    methods:{
    recieveMessage: function(map){
        app.$store.state.websocket.onmessage = function(event) {
            var data = JSON.parse(event.data);
            /* eslint-disable no-console */
            console.log("onmessage data:", data);
            /* eslint-enable no-console */
            // If message is of 'gps' type then parse the data and distribute the new markers
            if(data['type'] == 'gps_values'){
                markerList = [];
                personList = [];
                let objList = Object.values(data['gps_list']);
                for(let i = 0; i < objList.length; i++){
                    let personObj = objList[i];
                    let marker = new google.maps.Marker({
                        position: personObj.pos,
                        map: map,
                        label: personObj.name                    
                    });                
                    marker.setIcon({ url:"http://maps.google.com/mapfiles/ms/icons/red-dot.png"});
                    if(personObj.needHelp){
                        marker.setIcon({ url:"https://img.icons8.com/flat_round/64/000000/error.png",
                                        scaledSize: new google.maps.Size(30,30)});
                        marker.setAnimation(google.maps.Animation.BOUNCE)

                    } else if(personObj.group != meObj.group){                    
                        marker.setIcon({ url:"http://maps.google.com/mapfiles/ms/icons/blue-dot.png"});
                    }
                    markerList.push(marker);
                    personList.push(personObj);
                }
            } else {
                alert('GPS data is unavailable');
            }
        };
    },
    sendPerson: function(){
    // Skriv kod här som skickar "position" till backend som packar det i en lista new_pos.
    app.$store.state.websocket.send(JSON.stringify({
        'type': 'gps',
        'id': meObj.id,
        'pos': meObj.pos,
        'name': meObj.name,
        'group': meObj.group,
        'needHelp': meObj.needHelp
    }))
    },
    watchCurrentPosition: function(marker){
        positionTimer = navigator.geolocation.watchPosition(
        function(position){
            let pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            marker.setPosition(pos);
            meObj.pos = pos;
            app.sendPerson();
        }
        ,null,
        {
            enableHighAccuracy: false,
            timeout: 5000,
            maximumAge: Infinity
        });
    }}
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

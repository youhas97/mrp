<template>
    <div class="Map" />
</template>

<script>
/* eslint-disable no-unused-vars */

import gmapsInit from '../utils/gmaps.js';


let google;
let positionTimer;
let app;


/*
    name = client_data['name']
    id = client_data['id']
    pos = client_data['pos']
    group = client_data['group']
    need_help = client_data['needHelp']
    GPS_VALUES[id] = {
        'pos' : pos, 
        'name' : name, 
        'group' : group, 
        'needHelp' : need_help
        }
*/

function handleLocationError(browserHasGeolocation, marker, pos, map) {
    //marker.setPosition(pos);
    //marker.setContent(browserHasGeolocation ? 'Error: Geolocation misslyckades!' : 'Error: Din webbläsare stödjer inte geolocation');
    //marker.open(map);
}

function geoLocate(map) {
    navigator.geolocation.getCurrentPosition(function(position) {
        let pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        map.setCenter(pos);
        return position;
    }, function() {
        // Geolocation ej tillåtet
        handleLocationError(true, map.getCenter(), map);
    });
}

function geoGoal(map, goalWindow, results) {
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
        app = this;

        //var updatePos = window.setInterval(app.sendPerson, 500);

        this.recieveMessage(map);
        geocoder.geocode({ address: 'Arboga' }, (results, status) => {
            if (status !== 'OK' || !results[0]) {
                throw new Error(status);
            }
            let goal_loc;

            geocoder.geocode({ address: 'Linköpings Universitet' }, (results_goal, status_goal) => {
                if (status_goal !== 'OK' || !results_goal[0]) {
                    throw new Error(status_goal);
                }
                goal_loc = results_goal
            });
            map.setCenter(results[0].geometry.location);
            map.fitBounds(results[0].geometry.viewport);

            let goalWindow = new google.maps.InfoWindow;


            if (navigator.geolocation) {
                let position = geoLocate(map);
                app.sendPerson();
            } else {
                handleLocationError(false, map.getCenter(), map);
            }
        });

    },
    methods: {
        recieveMessage: function(map) {
            app.$store.state.websocket.onmessage = function(event) {
                var data = JSON.parse(event.data);
                /* eslint-disable no-console */
                console.log("onmessage data: " + event.data);
                // If message is of 'gps' type then parse the data and distribute the new markers

                let username = Object.keys(data)[0];

                if (data[username].type == 'gps_data') {
                    var userData = data[username];
                    if (!(username in app.$store.state.allUsers)) {
                        /* eslint-disable no-console */
                        console.log("pos: " + JSON.stringify(userData));
                        /* eslint-enable no-console */

                        let marker = new google.maps.Marker({
                            position: userData.pos,
                            map: map,
                            label: username
                        });

                        if (userData.needHelp) {
                            marker.setIcon({
                                url: "https://img.icons8.com/flat_round/64/000000/error.png",
                                scaledSize: new google.maps.Size(30, 30)
                            });
                            marker.setAnimation(google.maps.Animation.BOUNCE)

                        } else if (userData.group != app.$store.state.meObj.group) {
                            marker.setIcon({ url: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png" });
                        } else {
                            marker.setIcon({ url: "https://maps.google.com/mapfiles/ms/icons/red-dot.png" });
                        }


                        app.$store.state.allMarkers[username] = marker;
                        app.$store.state.allUsers[username] = userData;


                    } else {
                        app.$store.state.allMarkers[username].setPosition(userData.pos);
                    }

                    if (username == app.$store.state.username) {
                        app.$store.state.meObj = userData;
                        app.watchCurrentPosition(app.$store.state.allMarkers[username]);
                    }
                } else {
                    alert('GPS data is unavailable');
                }

                /* eslint-enable no-console */

            };
        },
        sendPerson: function() {
            // Skriv kod här som skickar "position" till backend som packar det i en lista new_pos.
            let meObj = app.$store.state.meObj;

            app.$store.state.websocket.send(JSON.stringify({
                'type': 'gps',
                'id': meObj.id,
                'pos': meObj.pos,
                'fname': meObj.fname,
                'group': meObj.group,
                'needHelp': meObj.needHelp
                /*
                'type': 'gps',
                'client_data': app.$store.state.meObj,
                */

            }))

        },
        watchCurrentPosition: function(marker) {
            positionTimer = navigator.geolocation.watchPosition(
                function(position) {
                    let pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    marker.setPosition(pos);
                    app.$store.state.meObj.pos = pos;

                    var delayInMilliseconds = 500;
                    setTimeout(function() {
                        //Code will be executed after 10ms
                        app.sendPerson();
                    }, delayInMilliseconds);
                }, null, {
                    enableHighAccuracy: false,
                    timeout: 5000,
                    maximumAge: Infinity
                });
        }
    }
};
</script>

<style>
html,
body {
    margin: 0;
    padding: 0;
}

.Map {
    width: 100vw;
    height: 100vh;
}

img[src^='http://www.google.com/mapfiles/marker.png?i='] {
    opacity: 0.5
}

;
</style>

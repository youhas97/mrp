<template>
    <div class="Map">

    </div>
</template>

<script>
/* eslint-disable no-console */
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
        // Geolocation ej tillåte
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
    data: function() {
        return {
            directionsService: null,
            directionsDisplay: null
        }
    },
    async mounted() {
        google = await gmapsInit();
        const geocoder = new google.maps.Geocoder();
        const map = new google.maps.Map(this.$el, {
            disableDefaultUI: true
        });
        app = this;

        app.directionsService = new google.maps.DirectionsService();
        app.directionsDisplay = new google.maps.DirectionsRenderer({
            suppressMarkers: true
        });
        app.directionsDisplay.setMap(map);

        // If user is not ledning then broadcast meObj.
        if (app.$store.state.users.meObj !== null) {
            app.sendPerson();
        }

        /* This function will be called when search function 
        has been triggered with vue.$root.$emit('locateUser') in
        Backup component.*/
        this.$root.$on('locateUser', (username) => {
            let pos = app.$store.state.users.allMarkers[username].position;
            map.panTo(pos);
            map.setZoom(15);
            map.setCenter(pos);
            google.maps.event.trigger(
                app.$store.state.users.allMarkers[username],
                'click'
            );
        });

        /* This function will be called when a user calls for backup
        and the marker icon has to be changed, in Backup component. */
        this.$root.$on('changeMarker', () => {
            this.changeMarker(
                this.$store.state.users.allMarkers[
                    this.$store.state.users.username
                ],
                this.$store.state.users.meObj
            );
        });

        /* Create click listener for alert creation */
        google.maps.event.addListener(map, 'click', function(event) {
            if (app.$store.state.alert.alerting) {
                // modal window that appears in CommandCenter.vue
                let modal = document.getElementById('modal-window');
                modal.style.display = "block";

                let sendAlertBtn = document.getElementById('send-alert-btn');
                sendAlertBtn.onclick = () => {
                    var marker = new google.maps.Marker({
                        id: app.$store.state.alert.alertID,
                        position: event.latLng,
                        map: map,
                        draggable: false
                    });
                    marker.setIcon({
                        url: "https://img.icons8.com/flat_round/64/000000/error.png",
                        scaledSize: new google.maps.Size(30, 30)
                    });
                    marker.setAnimation(google.maps.Animation.BOUNCE);
                    map.panTo(event.latLng);
                    app.$store.state.alert.allAlerts[app.$store.state.alert.alertID] = marker;

                    let textArea = document.getElementById('modal-textarea');
                    let input = document.getElementById('modal-input');

                    /* Create an infowindow for the alert icon */
                    let windowContent = '<div id="content">'+
                        `<h3>${input.value}</h3>`+
                        `<p>Beskrivning: ${textArea.value}</p>`+
                        `<button onclick="document.getElementById('app').__vue__.$root.$emit('removeAlert', ${marker.id})">Ta bort larm</button>`+
                        '</div>';

                    let infowindow = new google.maps.InfoWindow({
                        content: windowContent
                    });

                    // send alert to other users.
                    app.sendAlert(marker.id, input.value, textArea.value);

                    /* Listen for clicks on marker */
                    google.maps.event.addListener(marker, 'click', function(event) {
                        infowindow.open(map, marker);
                    });

                    app.$store.state.alert.alertID += 1;
                    app.$store.state.alert.alerting = false;
                    modal.style.display = "none";
                }

            }
        });

        /* Listener for $emit('removeAlert'), which is called on 
        alert infowindow button onclick. The infowindow is defined 
        in the listener method above.*/
        this.$root.$on('removeAlert', (id) => {
            this.removeAlert(id);
        });

        /* Listener for $emit('calcRoute'), which is called on the USERS
        alert infowindow button onclick "vägbeskrivning", which is added
        in receiveMessage(). */
        this.$root.$on('calcRoute', (markerID) => {
            this.calcRoute(markerID);
            this.directionsDisplay.setMap(map);
        });

        /* Listener for $emit('cancelDirections') in Backup component. 
        Removes directions from map. */
        this.$root.$on('cancelDirections', () => {
            this.directionsDisplay.setMap(null);
        });

        this.recieveMessage(map);
        geocoder.geocode({ address: 'Linköping' }, (results, status) => {
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

            if (navigator.geolocation && app.$store.state.users.meObj !== null) {
                console.log("name: " + app.$store.state.users.username);
                /* Creation of self data in list */
                let marker = new google.maps.Marker({
                    map: map,
                    label: app.$store.state.users.username
                });
                marker.setIcon({ url: "https://maps.google.com/mapfiles/ms/icons/red-dot.png" });

                let username = app.$store.state.users.username;
                app.$store.state.users.allUsers[username] = app.$store.state.users.meObj;
                app.$store.state.users.allMarkers[username] = marker;

                window.setInterval(function() {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        //let position = geoLocate(map);
                        //console.log(position);
                        let pos = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude
                        };
                        marker.setPosition(pos);
                        app.$store.state.users.meObj.pos = pos;
                        app.sendPerson();
                    })
                }, 200);

                //let position = geoLocate(map);
                //var updatePos = window.setInterval(app.sendPerson, 500);
            } else {
                handleLocationError(false, map.getCenter(), map);
            }
        });
    },
    methods: {
        recieveMessage: function(map) {
            /* Receive socket message from server. */

            app.$store.state.websocket.onmessage = function(event) {
                var data = JSON.parse(event.data);
                //console.log("onmessage data: " + event.data);

                if (data.type == 'gps_alert' || data.type == 'gps_alert_user') {
                    // make alert visible on the map.
                    let marker = new google.maps.Marker({
                        id: data.id,
                        position: data.pos,
                        map: map
                    });
                    marker.setIcon({
                        url: "https://img.icons8.com/flat_round/64/000000/error.png",
                        scaledSize: new google.maps.Size(30, 30)
                    });
                    marker.setAnimation(google.maps.Animation.BOUNCE);
                    map.panTo(data.pos);
                    app.$store.state.alert.allAlerts[data.id] = marker;
                    /* Create an infowindow for the alert icon */
                    let windowContent = '<div id="content">'+
                        `<h3>${data['infowindow-header']}</h3>`+
                        `<p>Beskrivning: ${data['infowindow-content']}</p>`+
                        `<button onclick=`+
                        `"document.getElementById('app').__vue__.$root.$emit(`+
                        `'calcRoute', ${marker.id}`+
                        `)">`+
                        `Vägbeskrivning`+
                        `</button>`+
                        '</div>';

                    let infowindow = new google.maps.InfoWindow({
                        content: windowContent
                    });
                    /* Listen for clicks on marker */
                    google.maps.event.addListener(marker, 'click', function(event) {
                        infowindow.open(map, marker);
                    });
                    return;
                } else if (data.type == 'gps_cancel_alert') {
                    // remove alert from the map.
                    app.$store.state.alert.allAlerts[data.id].setMap(null);
                    delete app.$store.state.alert.allAlerts[data.id];
                    return;
                } else if (data.type == 'logout') {
                    // delete user and its marker upon logout.
                    app.$store.state.users.allMarkers[data.username].setMap(null);  
                    delete app.$store.state.users.allMarkers[data.username];
                    delete app.$store.state.users.allUsers[data.username];
                    return;
                }

                // If message is of 'gps' type then parse the data and distribute the new markers
                var username = Object.keys(data)[0];

                if (data[username].type == 'gps_data') {
                    var userData = data[username];
                    if (!(username in app.$store.state.users.allUsers)) {
                        /* New user has appeared! Create a marker for their position and
                        add them to the list of all users. */

                        let marker = new google.maps.Marker({
                            position: userData.pos,
                            map: map,
                            label: username,
                            optimized: false
                        });

                        app.changeMarker(marker, userData);

                        let windowContent = '<div id="content">'+
                            `<h1>${username}</h1>`+
                            `<p>Group: ${userData.group}</p>`+
                            '</div>';

                        let infowindow = new google.maps.InfoWindow({
                            content: windowContent
                        });
                        marker.addListener('click', function() {
                            infowindow.open(map, marker);
                        });

                        app.$store.state.users.allMarkers[username] = marker;
                        app.$store.state.users.allUsers[username] = userData;

                        /* If current user is ledning, then make sure we send all
                        the alerts to the new user that has appeared. */
                        if(!app.$store.state.users.meObj) {
                            for (let key in Object.keys(app.$store.state.alert.allAlerts)) {
                                app.sendAlertTo(
                                    username, 
                                    app.$store.state.alert.allAlerts[key].id
                                )
                            }
                        }
                    } else {
                        /* Update position of already existing users. */
                        let marker = app.$store.state.users.allMarkers[username];
                        app.changeMarker(marker, userData);
                        marker.setPosition(userData.pos);
                    }

                    app.$store.state.users.allUsers[username] = userData;
                } else {
                    alert('GPS data is unavailable');
                }


            };
        },
        changeMarker: function(marker, userData) {
            if (userData.needHelp) {
                marker.setIcon({
                    url: "https://img.icons8.com/flat_round/64/000000/error.png",
                    scaledSize: new google.maps.Size(30, 30)
                });
                marker.setAnimation(google.maps.Animation.BOUNCE)

            } else if (app.$store.state.users.meObj !== null && userData.group == app.$store.state.users.meObj.group) {
                marker.setIcon({ url: "https://maps.google.com/mapfiles/ms/icons/red-dot.png" });
                marker.setAnimation(google.maps.Animation.NONE);
            } else {
                marker.setIcon({ url: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png" });
                marker.setAnimation(google.maps.Animation.NONE);
            }

        },
        sendPerson: function() {
            let meObj = app.$store.state.users.meObj;

            app.$store.state.websocket.send(JSON.stringify({
                'type': 'gps',
                'id': meObj.id,
                'pos': meObj.pos,
                'fname': meObj.fname,
                'group': meObj.group,
                'needHelp': meObj.needHelp
            }))

        },
        sendAlert: function(alertID, header, content) {
            app.$store.state.websocket.send(JSON.stringify({
                'type': 'gps_alert',
                'id': alertID,
                'pos': app.$store.state.alert.allAlerts[alertID].position,
                'infowindow-header': header,
                'infowindow-content': content
            }));
        },
        sendAlertTo: function(username, alertID) {
            app.$store.state.websocket.send(JSON.stringify({
                'type': 'gps_alert_user',
                'id': alertID,
                'pos': app.$store.state.alert.allAlerts[alertID].position,
                'sent_to': username
            }));
        },
        watchCurrentPosition: function(marker) {
            positionTimer = navigator.geolocation.watchPosition(
                function(position) {
                    let pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    marker.setPosition(pos);
                    app.$store.state.users.meObj.pos = pos;
                    app.sendPerson();
                }, null, {
                    enableHighAccuracy: false,
                    timeout: 5000,
                    maximumAge: Infinity
                });
        },
        calcRoute: function(markerID) {
            let start = this.$store.state.users.allMarkers[
                this.$store.state.users.username
            ].position;
            let end = this.$store.state.alert.allAlerts[markerID].position;
            var request = {
                origin: start,
                destination: end,
                travelMode: 'DRIVING'
            };  
            this.directionsService.route(request, (result, status) => {
                if (status == 'OK')
                    this.directionsDisplay.setDirections(result);
            });
        },
        removeAlert: function(id) {
            let marker = this.$store.state.alert.allAlerts[id];
            this.$store.state.websocket.send(JSON.stringify({
                'type': 'gps_cancel_alert',
                'id': marker.id
            }));
            this.$store.state.alert.allAlerts[marker.id] = null;
            marker.setMap(null);
        }
    }
};

/* eslint-enable no-console */
</script>

<style scoped>
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
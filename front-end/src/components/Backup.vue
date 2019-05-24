<template>
    <div style="width: 180px; height: 40px; margin: 0 auto;" class="navBar">
        <button id="backupButton" @mousedown="hold" @mouseup="release" @mouseout="release"
        @touchstart="hold" @touchend="release">
        {{buttonText}}
        </button>

        <div id="userSelection" class="dropdownList">
            <button class="dropdownBtn" type="submit" @mousedown="toggleUsers">Aktiva poliser</button>
            <div id="dropdown" class="dropdownContent">
            </div>
        </div>

        <div id="choiceList" class="dropdownList">
            <button id="gearBtn"  @mousedown="toggleMenu"/>
            <div id="menus" class="dropdownContent">
                <button id="cancelDirectionsBtn" @mousedown="cancelDirections">Avsluta vägbeskrivning</button>
            </div>
        </div>
    </div>
</template>

<script>

let app;

export default {
    name: 'Backup',
    data: function() {
        return {
            buttonText: "Förstärkning",
            timerStarted: false,
            timeoutId: 0,
            intervalId: 0,
            backUpCalled: false,
            secs: 0,

            searchText: ""
        }
    },
    mounted() {
        let dropdown = document.getElementById('dropdown');
        let menus = document.getElementById('menus');
        window.onclick = (event) => {
            if(!event.target.closest('#choiceList'))
                if(menus.classList.contains('show'))
                    this.toggleMenu();
            if(!event.target.closest('#userSelection'))
                if(dropdown.classList.contains('show'))
                    this.toggleUsers();
        };
    },
    methods: {
        hold: function() {
            var secs = 3;
            this.buttonText = "Håll i " + secs + " sekunder";
            this.timerStarted = true;
            app = this;
            this.intervalId = setInterval(function(){
                secs -= 1;
                app.buttonText = "Håll i " + secs + " sekunder";
            },1000)
            this.timeoutId = setTimeout(function() {
                clearInterval(app.intervalId);
                app.timerStarted = false;
                app.backUpCalled = !app.backUpCalled;
                app.$store.state.users.meObj.needHelp = app.backUpCalled;
                // Tell MapBase component to change marker.
                app.$root.$emit('changeMarker');
                /* eslint-disable no-console */
                console.log("backup: ", app.$store.state.users.meObj.needHelp);
                /* eslint-enable no-console */
                app.fetchButtonText();
            }, secs * 1000);


        },
        release: function() {
            if (this.timerStarted) {
                //Backup regreted
                clearInterval(this.intervalId);
                clearTimeout(this.timeoutId);
            }
            this.timerStarted = false;
            this.fetchButtonText();
        },
        fetchButtonText: function() {
            if (this.backUpCalled) {
                this.buttonText = "Avbryt Larm";
            } else {
                this.buttonText = "Förstärkning";
            }
        },
        distanceTo: function(pos) {
            /*  
                This function uses the Haversine formula to calculate the 
                shortest distance between two points.
                
                P1: users current position
                P2: pos (input to function)
            */
            var meObj =  this.$store.state.users.meObj;

            var rad = function(x) {
                return x * Math.PI / 180;
            };
            

            console.log(meObj.pos);

            var R = 6378137; // Earth's mean radius in meter

            var dLat = rad(pos.lat - meObj.pos.lat);
            var dLng = rad(pos.lng - meObj.pos.lng);
            
            var a = Math.sin(dLat/2) * Math.sin(dLat/2) + 
                Math.cos(rad(meObj.pos.lat)) * Math.cos(rad(pos.lat)) *
                Math.sin(dLng/2) * Math.sin(dLng/2);

            var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
            var d = R*c; // d = distance in meter
            
            return (d/1000).toFixed(2); // return distance in km
        }
        ,
        toggleUsers: function() {
            /* This function is executed by the dropdown button */
            document.getElementById('dropdown').classList.toggle('show');

            /* If the dropdown list already contains elements, 
                don't add duplicates. */
            if(!document.getElementById('dropdown').firstChild) {
                /* Make a list out of the dictionary of users */
                var allUsers = this.$store.state.users.allUsers;
                var userList = Object.keys(allUsers).map((key) => { 
                    return [key, this.distanceTo(allUsers[key].pos)];
                });
                

                /* Sort list of all users based on distance to self */
                userList.sort((a,b) => {return a[1] - b[1]});

                // Add all users to the dropdown div. 
                for(var user in userList){
                    if(user == 'ledning')
                        continue;
                    var dropdown = document.getElementById('dropdown');
                    var userButton = document.createElement('button');
                    // styling.
                    userButton.style.padding = "5px 0px";
                    userButton.style.width = "100%";
                    userButton.style.borderRadius = "10px";
                    userButton.style.fontSize = "120%";
                    userButton.style.display = "block";
                    userButton.style.border = "2px solid #4a86e8";
                     
                    // userList[user][0] is the name, 
                    // userList[user][1] is the distance 
                    userButton.innerHTML = userList[user][0] + ' (' + userList[user][1] + 'km)';
                    
                    // add click listener that locates user that is clicked.
                    userButton.addEventListener('click', (event) => {
                        var username = event.target.innerHTML.slice(
                            0, event.target.innerHTML.indexOf(' ')
                        );
                        this.$root.$emit('locateUser', username);
                        this.toggleUsers();
                    });
                    dropdown.appendChild(userButton);
                }
            } else if(
                !document.getElementById('dropdown').classList.contains('show') &&
                document.getElementById('dropdown').firstChild
            ) {
                /* If dropdownList is hidden with toggle, 
                delete all children element */
                var dropdownList = document.getElementById('dropdown');
                while(dropdownList.firstChild)
                    dropdownList.removeChild(dropdownList.firstChild);
            }
        },
        toggleMenu: function() {
            document.getElementById('menus').classList.toggle('show');
        },
        cancelDirections: function() {
            /* Tell MapBase to remove directions. */
            this.$root.$emit('cancelDirections');
            this.toggleMenu();
        }
    }
}
</script>

<style scoped>
#dropdown button {
    display: block;
    padding: "12px 16px";
    margin: 0;
    width: 100%;
    color: black;
    background-color: #e7e7e7;
    border: none;
}

#dropdown button:hover {
    background-color: blue;
    color: white;
}

#dropdown {
    width: 100%;
}

button {
    font-size: 150%;
    border-radius: 10px;
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 5px;
    padding-bottom: 5px;
    border: 2px solid #4a86e8;

    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

#backupButton {
    position: absolute;
    bottom: 10px;
    margin: auto auto;
}

#userSelection {
    position: relative;
    margin: 0 auto;
    padding: 0;
    display: inline-block;
}

.dropdownBtn {
    margin: 0;
}

.dropdownContent {
    display: none;
    position: absolute;
    background-color: #f1f1f1;
    min-width: 100px;
    overflow: auto;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
    background-color: transparent;
}

#menus {
    right: 0;
    left: auto;
}

#menus button {
    font-size: 100%;
}

.show {
    display: block;
}

#gearBtn {
    background-image: url('../assets/gearIcon.png');
    background-position: center center;
    background-repeat: no-repeat;
    background-size: contain;
    background-color: transparent;
    width: 1.5em;
    height: 1.5em;
    z-index: 1;
    border: none;
}

#choiceList {  
    position: absolute;
    display: inline-block;
    top: 15px;
    right: 15px;
}
</style>

<template>
    <div class="navBar">
        <button id="backupButton" @mousedown="hold" @mouseup="release" @mouseout="release"
        @touchstart="hold" @touchend="release">
        {{buttonText}}
        </button>

        <div id="userSelection" class="dropdownList">
            <button class="dropdownBtn" type="submit" @mousedown="searchUser">Aktiva poliser</button>
            <div id="dropdown" class="dropdown-content">
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
        window.onclick = (event) => {
            if(!event.target.matches('.dropdownBtn')) {
                /* If click event is outside dropdownBtn, then hide dropdown div
                and delete child elements */
                var dropdownList = document.getElementById('dropdown');
                if(dropdownList.classList.contains('show'))
                    dropdownList.classList.remove('show');
                while(dropdownList.firstChild) 
                    dropdownList.removeChild(dropdownList.firstChild);
            }
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
        searchUser: function() {
            /* This function is executed by the dropdown button */
            document.getElementById('dropdown').classList.toggle('show');

            /* If the dropdown list already contains elements, 
                don't add duplicates. */
            if(!document.getElementById('dropdown').firstChild) {
                // Add all users to the dropdown div. 
                for(var user in this.$store.state.users.allUsers){
                    var dropdown = document.getElementById('dropdown');
                    var userButton = document.createElement('button');
                    // styling.
                    userButton.style.padding = "5px 0px";
                    userButton.style.width = "100%";
                    userButton.style.borderRadius = "10px";
                    userButton.style.fontSize = "150%";
                    userButton.style.display = "block";
                    userButton.style.border = "2px solid #4a86e8";
                    userButton.innerHTML = user;
                    // add click listener that locates user that is clicked.
                    userButton.addEventListener('click', (event) => {
                        let username = event.srcElement.innerHTML;
                        this.$root.$emit('locateUser', username);
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
        }
        /*
                countSecs: function(){
                    for(var i; i < 3; i++){
                        let that = this;
                        setTimeout(function () {
                            that.secs = i + 1;
                        }, 1000*i + 10);
                    }
                }*/
    }
}
</script>

<style scoped>
#dropdown button {
    display: block;
    padding: "12px 16px";
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
    margin: 10px;
}

#userSelection {
    position: relative;
    display: inline-block;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: #f1f1f1;
    min-width: 100px;
    overflow: auto;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
}

.show {
    display: block;
}
</style>

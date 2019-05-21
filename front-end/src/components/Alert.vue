<template>
    <div class="navBar">
            <button @mouseup="alert">
                {{buttonText}}
            </button>

            <div id="userSelection" class="dropdownList">
                <button class="dropdownBtn" type="submit" @mousedown="toggleUsers">Aktiva poliser</button>
                <div id="dropdown" class="dropdownContent">
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
            buttonText: "Larma",
            timerStarted: false,
            fetchTextInterval: null,
        }
    },
    mounted() {
        let dropdown = document.getElementById('dropdown');
        window.onclick = (event) => {
            if(!event.target.closest('#userSelection'))
                if(dropdown.classList.contains('show'))
                    this.toggleUsers();
        };
    },
    methods: {
        alert: function() {
            app = this;
            app.$store.state.alert.alerting = !app.$store.state.alert.alerting;
            /* eslint-disable no-console */
            console.log("alerting: ", app.$store.state.alert.alerting);
            /* eslint-enable no-console */

            if (app.fetchTextInterval == null) {
                app.fetchTextInterval = setInterval(function() {
                    app.fetchButtonText();
                }, 1);
            }
        },
        fetchButtonText: function() {
            if (app.$store.state.alert.alerting) {
                app.buttonText = "Välj position";
            } else {
                app.buttonText = "Larma";
            }
        },
        toggleUsers: function() {
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
                        //document.getElementById('dropdown').classList.toggle('show');
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
        }
    }
}
</script>

<style scoped>
button {
    margin: 10px;
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

.show {
    display: block;
}
</style>

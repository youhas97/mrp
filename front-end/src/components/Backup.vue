<template>
    <div class="navBar">
        <button id="backupButton" @mousedown="hold" @mouseup="release" @mouseout="release"
        @touchstart="hold" @touchend="release">
        {{buttonText}}
        </button>

        <form id="searchForm" @submit.prevent="searchUser">
            <input v-model="searchText" type="text" placeholder="Search user...">
            <button type="submit" @release="searchUser">Search</button>
        </form>
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
            var user = this.$store.state.users.allUsers[this.searchText];
            if(!user)
                alert("User does not exist.");
            else {
                alert("User found!");
                this.$root.$emit('locateUser', this.searchText);
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

#backupButton {
    margin: 10px;
    font-size: 200%;
    border-radius: 10px;
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 5px;
    padding-bottom: 5px;
    border: 2px solid #4a86e8;
}
</style>

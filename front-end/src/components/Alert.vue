<template>
    <div>
        <button @mousedown="hold" @mouseup="release" @mouseout="release">
            {{buttonText}}
            </button>
        <Map/>
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
            timeoutId: 0,
            intervalId: 0,
            fetchTextInterval: 0,
            secs: 0,
        }
    },

    methods: {
        hold: function() {
            app = this;
            var secs = 3;
            app.buttonText = "Håll i " + secs + " sekunder";
            app.timerStarted = true;
            app.intervalId = setInterval(function() {
                secs -= 1;
                app.buttonText = "Håll i " + secs + " sekunder";
            }, 1000)
            app.timeoutId = setTimeout(function() {
                clearInterval(app.intervalId);
                app.timerStarted = false;
                app.$store.state.alert.alerting = !app.$store.state.alert.alerting;
                /* eslint-disable no-console */
                console.log("alerting: ", app.$store.state.alert.alerting);
                /* eslint-enable no-console */
                app.fetchButtonText();
            }, secs * 1000);

            app.fetchTextInterval = setInterval(function() {
                if (!app.timerStarted) {
                    app.fetchButtonText();
                }
            }, 100);

        },
        release: function() {
            if (app.timerStarted) {
                //Cancel alert
                clearInterval(app.intervalId);
                clearTimeout(app.timeoutId);
            }
            app.timerStarted = false;
            app.fetchButtonText();
        },
        fetchButtonText: function() {
            if (app.$store.state.alert.alerting) {
                app.buttonText = "Välj position";
            } else {
                app.buttonText = "Larma";
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
</style>

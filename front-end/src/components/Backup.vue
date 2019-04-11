<template>
    <div>
        <button @mousedown="hold" @mouseup="release" @mouseout="release">
        {{buttonText}}
        </button>
    </div>
</template>

<script>

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
        }
    },

    methods: {
        hold: function() {
            var secs = 3;
            this.buttonText = "Håll i " + secs + " sekunder";
            this.timerStarted = true;
            let app = this;
            this.intervalId = setInterval(function(){
                secs -= 1;
                app.buttonText = "Håll i " + secs + " sekunder";
            },1000)
            this.timeoutId = setTimeout(function() {
                clearInterval(app.intervalId);
                app.timerStarted = false;
                app.backUpCalled = !app.backUpCalled;
                app.$store.state.meObj.needHelp = app.backUpCalled;
                /* eslint-disable no-console */
                console.log("backup: ", app.$store.state.meObj.needHelp);
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

button {
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

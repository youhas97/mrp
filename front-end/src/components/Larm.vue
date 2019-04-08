<template>
    <div>
        <button
            @mousedown="hold"
            @mouseup="release"
            @mouseout="release">
            {{buttonText}}
        </button>
        <Map/>
    </div>
</template>

<script>
import Map from './MapBase';


export default {
    name: 'Larm',
    components: {
        Map
    },
    data: function () {
            return {
                buttonText: "Förstärkning",
                timerStarted: false,
                timeoutId: 0,
                backUpCalled: false,
                secs: 0,
            }
        },

    methods: {
        hold: function() {
            this.buttonText="Håll i 3 sekunder";
            this.timerStarted = true;
            let that = this;
            this.timeoutId = setTimeout(function () {
                //Map.needBackUp=true;
                that.timerStarted = false;
                if(that.backUpCalled){
                    //Send to backend that user need backup
                    that.backUpCalled = false;
                }
                else{
                    that.backUpCalled = true;
                }
                that.fetchButtonText();
            }, 3000);


        },
        release: function(){
            if(this.timerStarted){
                //Backup regreted
                clearTimeout(this.timeoutId);
            }
            this.timerStarted = false;
            this.fetchButtonText();
        },
        fetchButtonText: function(){
          if(this.backUpCalled){
              this.buttonText = "Avbryt Larm";
          }
          else{
              this.buttonText = "Förstärkning";
          }
        }/*
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
html,
body {
    height: 100%;
    margin: 0;
}
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

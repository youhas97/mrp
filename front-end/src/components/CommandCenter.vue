<template>
    <div id="mobile">
        <Alert/>
        <Map/>

        <!-- Modal window that appears when ledning wants to send an alert. -->
        <div id="modal-window" class="modal">
            <div class="modal-content">
                <h1>Larm</h1>
                <p>Rubrik: </p><input type="text" id="modal-title">
                <p>Beskrivning: </p><textarea id="modal-textarea" rows="4" cols="50"></textarea>
                <p>Ladda upp bild: </p>
                <button id="send-alert-btn">Skicka larm</button>
            </div>
        </div>
    </div>
</template>

<script>
import Alert from './Alert'
import Map from './MapBase'

export default {
    name: 'CommandCenter',
    components: {
        Alert,
        Map
    },
    mounted() {
        // remove modal window if clicked outside the modal window.
        let app = this;
        window.onclick = function(event) {
            let modal = document.getElementById('modal-window');
            if (event.target == modal) {
                modal.style.display = "none";
                app.$store.state.alert.alerting = false;
            }
        } 
    }
}
</script>

<style scoped>
.Map {
    position: absolute;
    top: 0px;
    left: 0px;
    z-index: -1;
    /*margin: auto;*/
}
.Alert {
    position: absolute;
    z-index: 1;
}

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content/Box */
.modal-content {
  background-color: #fefefe;
  margin: 5% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}

#send-alert-btn {
    font-size: 100%;
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


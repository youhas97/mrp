<template>
    <div id="app">
        <router-view></router-view>
    </div>
</template>

<script>
    let that = this;

    var socket = new WebSocket('ws://127.0.0.1:9000/ws/connect/');

    socket.onclose = function(event) {
        /* eslint-disable no-console */
        console.error('Socket closed unexpectedly!', event.code);
        /* eslint-enable no-console */
    };

    socket.onopen = function() {
        /* eslint-disable no-console */
        console.error('Socket opened!', event.code);
        /* eslint-enable no-console */
    };
</script>

<style>
body {
    background-size: cover;
    background-repeat: no-repeat;
    background-image: url("./assets/background.png");
}
img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 300px;
}
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #000000;
    margin-top: 5%;
}
</style>

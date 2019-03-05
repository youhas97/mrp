<template>
    <div id="app">
        <img alt="Map background" src="./assets/logo.png">
        <LogIn/>
    </div>
</template>

<script>

import LogIn from './components/LogIn.vue'
    export default {
    name: 'app',
    components: {
        LogIn
    }
}
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
    width: 50%;
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

<template>
    <div id="app">
        <router-view></router-view>
    </div>
</template>

<script>
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

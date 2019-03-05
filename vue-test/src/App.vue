<template>
  <div id="app">'
    <img alt="Map background" src="./assets/logo.png">'
    <LogIn msg="Log In"/>
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
  background-repeat:no-repeat;
  background-image: url("./assets/background.png");
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #000000;
  margin-top: 60px;
}
</style>

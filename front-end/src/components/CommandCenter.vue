<template>
    <div id="mobile">
        <Alert/>
        <Map/>
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
</style>


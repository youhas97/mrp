<template>
    <div id="mobile">
        <Larm/>
        <Map/>
    </div>
</template>

<script>
import Larm from './Larm'
import Map from './MapBase'

export default {
    name: 'Mobile',
    components: {
        Larm,
        Map
    },
}
</script>

<style scoped>
.Map {
    width: 99vw;
    height: 90vh;
    margin: auto;
}
</style>


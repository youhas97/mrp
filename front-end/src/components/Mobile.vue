<template>
    <div id="mobile">
        <Backup/>
        <Map/>
    </div>
</template>

<script>
import Backup from './Backup'
import Map from './MapBase'

export default {
    name: 'Mobile',
    components: {
        Backup,
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


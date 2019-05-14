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
    position: absolute;
    top: 0px;
    left: 0px;
    z-index: -1;
    /*margin: auto;*/
}
.Backup {
    position: absolute;
    z-index: 1;
}
</style>


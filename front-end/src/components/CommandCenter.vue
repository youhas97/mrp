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
    width: 99vw;
    height: 90vh;
    margin: auto;
}
</style>


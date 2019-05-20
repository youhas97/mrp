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
    mounted() {
        Map.ontouchend = (e) => {
            e.preventDefault();
        };
    }
}
</script>

<style scoped>
 html, body {
    margin: 0; 
    height: 100%; 
    overflow: hidden
}

body {
    overflow-x: hidden;
    overflow-y: hidden;
}

.Map {
    position: absolute; /* prevent overscroll bounce*/
    top: 0;
    left: 0;
    z-index: -1;
    /*margin: auto;*/
}
.Backup {
    position: absolute;
    z-index: 1;
}
</style>


<template>
    <div>
        <button
        @click="larm">
            Press me
        </button>
        <Map/>
    </div>
</template>

<script>
import Map from './MapBase';

export default {
    name: 'Larm',
    components: {
        Map
    },
    methods: {
        larm: function() {
            alert('det här funkar');
        }
    }
}


</script>

<style scoped>
html,
body {
    height: 100%;
    margin: 0;
}
button {
    margin: 10px;
    font-size: 200%;
    border-radius: 10px;
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 5px;
    padding-bottom: 5px;
    border: 2px solid #4a86e8;
}

</style>
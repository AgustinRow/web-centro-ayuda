<template>
    <div>
        <l-map
            style="height: 350px"
            :zoom="zoom"
            :center="center"
            @click="addPoint"
        >
            <l-tile-layer :url="url"> </l-tile-layer>
            <l-marker v-if="this.show" :lat-lng="punto"  @click="removePoint"/>     
        </l-map>    
    </div>
</template>

<script>
import L from 'leaflet';
import {LMap, LTileLayer, LMarker} from 'vue2-leaflet'

export default {
    components: {
        LMap,
        LTileLayer,
        LMarker
    },
    data(){
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            zoom: 14,
            center: [-34.9187, -57.956],
            punto:null,
            show:false
        }
    },
    methods: {
        removePoint (){
            this.punto=null
            this.show=false

        },
        addPoint (point){
            this.punto=L.latLng(point.latlng.lat, point.latlng.lng)
            this.show=true
            this.$emit('pointChanged', this.punto)
        }
    }
}
</script>
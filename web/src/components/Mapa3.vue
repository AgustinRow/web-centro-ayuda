<template>
    <div>
        <l-map
            style="height: 350px"
            :zoom="zoom"
            :center="center"
            @click="addPoint"
        >
            <l-tile-layer :url="url"> </l-tile-layer>
            <l-marker :lat-lng="point" @click="removePoint(point)"/>     
        </l-map>    
    </div>
</template>

<script>
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
            point:[]
        }
    },
    methods: {
        removePoint (point){
            const index = this.points.indexOf(point)
            this.points.splice(index,1)
        },
        addPoint (point){
            this.point.push(point.latlng)
        },
        sendMessageToParent(){
            this.$emit('messageFromChild', this.point)
        }
    }
}
</script>
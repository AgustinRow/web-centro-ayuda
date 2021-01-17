<template>
<l-map style="height: 93vh" :zoom="zoom" :center="center">
<l-tile-layer :url="url"></l-tile-layer>
<l-marker  v-bind:key="dato" v-for="dato in datos" :lat-lng="latLng(dato.latitud, dato.longitud)" >
  <l-tooltip>{{dato.nombre}}</l-tooltip>
  <l-popup>
    <h4 style="text-align: center;">{{dato.nombre}}</h4>  
    <b>Direccion:</b> {{dato.direccion}}  
    <br><b>Telefono:</b> {{dato.telefono}} 
    <br><b>Horario:</b> {{dato.horario_apertura}} - {{dato.horario_cierra}} 
    <br>
    <b-button variant="outline-primary" :to="{name:'Turno', params: {'id':dato.id}}">Nuevo Turno</b-button></l-popup>

  

</l-marker>
</l-map> 
</template>

<script>
import L from 'leaflet';
import {LMap, LTileLayer, LMarker, LPopup, LTooltip} from 'vue2-leaflet';
import axios from 'axios';
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup, 
    LTooltip
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 14,
      center: [-34.92158510832922, -57.95440818271786],
      markerLatLng: [-34.92158510832922, -57.95440818271786],
      datos:[]
    };
  },
  mounted: function(){
    axios.get('https://admin-grupo16.proyecto2020.linti.unlp.edu.ar/centros')
          .then(response => {
          this.datos = response.data.centros;
          })
  },
  methods: {
    latLng:function(lat, lng){
      return L.latLng(lat, lng);
    }
  }
}
</script>

<style scoped>
</style>
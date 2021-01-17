<template>
<div class="custom-card header-card card">
<div class="card-body pt-0 display: flex">
  <div style="height: 350px; width: 350px">
    <l-map
      v-if="showMap"
      :zoom="zoom"
      :center="center"
      :options="mapOptions"
      style="height: 100%"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      <l-marker :lat-lang="markers">
        <l-popup>
          <div @click="innerClick">
            Nombre {{this.centros.nombre}}
            <br>
            Abierto/Cerrado 
            <br>
            Horarios:  
            <p v-show="showParagraph">
              Lorem 
            </p>
          </div>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</div>
</div>

</template>

<script>
import axios from 'axios';
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup, L } from "vue2-leaflet";

export default {
  name: "Maps",
  props: [],
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  data() {
    return {
      centros: [],
      errors: [],
      zoom: 7,
      center: latLng(-34.825466, -57.961466),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      withPopup: '',
      markers:[],
      latLong: '',
      currentZoom: 11,
      showParagraph: false,
      mapOptions: {
        zoomSnap: 0.5
      },
      showMap: true
    };
  },
  methods: {
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
    showLongText() {
      this.showParagraph = !this.showParagraph;
    },
    innerClick() {
      alert("Click!");
    },
    latLng: function (lat, lng){
      const coord= latLng(lat, lng);
      console.log(coord)
      this.latLong=coord
      //return coord
    },
    fetchApi: async function() {
    await axios.get('https://admin-grupo16.proyecto2020.linti.unlp.edu.ar/centros')
          .then(response => {
            console.log(response.data.centros[0])
          // JSON responses are automatically parsed.
          this.centros[0] = response.data.centros[0];
          })
          .catch(e => {
            console.log(e)
            this.errors.push(e)
          })
  }
  }, 
  beforeCreate() {
     axios.get('https://admin-grupo16.proyecto2020.linti.unlp.edu.ar/centros')
          .then(response => {
            console.log(response.data.centros[0])
          // JSON responses are automatically parsed.
          this.centros[0] = response.data.centros[0];
          this.marker.push(L.latLng(this.centros.latitud, this.centros.longitud))
          })
          .catch(e => {
            console.log(e)
            this.errors.push(e)
          })
  },

 
  }

</script>

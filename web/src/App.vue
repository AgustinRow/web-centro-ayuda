<template style="background-color: #009aae99">
  <div id="app">
  <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand href="#">Aplicación Don<b>AR</b></b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item :to="{name:'Home'}">Home</b-nav-item>
        <b-nav-item :to="{name:'Mapa2'}">Mapa</b-nav-item>
        <b-nav-item :to="{name:'Centro'}">Centro</b-nav-item>
        <b-nav-item :to="{name:'SeleccionarCentro'}">Sacar Turno</b-nav-item>
        <b-nav-item :to="{name:'Estadisticas'}">Estadisticas</b-nav-item>
        <!--<b-nav-item :to="{name:'Prueba'}">Prueba</b-nav-item>-->

      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
  <router-view/>
  </div>
</template>

<script>
//import Home from './components/Home.vue'
export default {
  name: 'app',
  components: {
    //Home
  }
}
</script>

<style>

</style>

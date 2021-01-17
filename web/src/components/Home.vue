<template style="background-color: #009aae99; height:100%" >
  <div>
    <div class="container" style="margin-bottom:20px">
      <div style="margin-top:40px">
        <h1 style=" color: black; text-align: center;">Centros de Ayuda de la Provincia de Buenos Aires<br>COVID-19</h1>
      </div>
      <div class="row mt-4">
        <div class="col-lg-4 d-flex align-items-stretch">
          <b-button variant="link" :to="{name:'Mapa2'}" text-decoration-none class="card list-group-item list-group-item-action">
          <div class="card-body">
              <h3 style="text-align: center;" >Mapa</h3>
            <hr>
            <p style="text-align: center;">Mapa con ubicaciones de los centros </p>
            <center><img style="max-width: 200px;" src="/mapa.png"></center>
            <br>
          </div>
          </b-button>
        </div>
        <div class="col-lg-4 d-flex align-items-stretch">
          <b-button variant="link" :to="{name:'Centro'}" text-decoration-none class="card list-group-item list-group-item-action">
          <div class="card-body">
              <h3 style="text-align: center;">Nuevo Centro</h3>
            <hr>
            <p style="text-align: center;">Agregar un centro nuevo </p>
            <center><img style="max-width: 200px;" src="/centro.png"></center>
            <br>
          </div>
          </b-button>
        </div>
        <div class="col-lg-4 d-flex align-items-stretch">
          <b-button variant="link" :to="{name:'Estadisticas'}" text-decoration-none class="card list-group-item list-group-item-action">
          <div class="card-body">
              <h3 style="text-align: center;">Estadisticas</h3>
            <hr>
            <p style="text-align: center;">Sector de estadisticas y porcentajes</p>
            <center><img style="max-width: 200px;" src="/estadisticas.png"></center>
            <br>
          </div>
          </b-button>
        </div>
      </div>
      <div style="justify-content:center; display:flex; margin-top: 10px">
        <div class="col-lg-4 d-flex align-items-stretch">
          <b-button variant="link" :to="{name:'SeleccionarCentro'}" text-decoration-none class="card list-group-item list-group-item-action">
          <div class="card-body">
              <h3 style="text-align: center;">Sacar Turno</h3>
            <hr>
            <p style="text-align: center;">Elija un Centro de Ayuda y reserve un turno</p>
            <center><img style="max-width: 200px;" src="/turnos.jpg"></center>
            <br>
          </div>
          </b-button>
        </div>
      </div>
    </div>
    <br>
    
    <center><p>¿Sos Operador? <a href="https://admin-grupo16.proyecto2020.linti.unlp.edu.ar"><b style="text-decoration: underline">Iniciar Sesion</b></a></p></center> 
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home'
}
</script>

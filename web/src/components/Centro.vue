<template>
  <div class="container card col-md-6 mt-3">
    <h2>Cargar Nuevo Centro</h2>
    <div>
      <b-modal
        v-model="this.exito" hide-header-close no-close-on-backdrop
      >
      <b-container fluid>
        <center>
          <p style="color: green; text-decoration: underline "><b>¡Centro enviado con Exito!</b></p>
          <div style="margin-bottom:10px ;display: flex; justify-content: center;">
            <div style="text-align: left;">
            <p><b>Nombre:</b> {{ form.name }}</p>
            <p><b>Tipo:</b> {{ form.tipo }}</p>
            <p><b>Municipio:</b> {{ form.municipio }}</p>
            <p><b>Telefono:</b> {{ form.phone }}</p>
            </div>
          </div>
          <p style="color: #afafaf;">Su centro fue enviado para revisión. Una vez que un operador lo acepte sera visible para el público</p>
        </center>
      </b-container>

      <template #modal-footer>
        <div style="text-align: center" class="w-100">
          <b-button :to="{name:'Home'}">
            Volver al Inicio
          </b-button>
        </div>
      </template>
    </b-modal>
    </div>

    <div style="margin-bottom:50px">
      <form v-on:submit.prevent="submitForm">
        <div class="form-group">
          <label for="name">Nombre Centro</label>
          <input
            type="text"
            class="form-control"
            id="name"
            placeholder="Nombre"
            v-model="form.name"
           required
          />
        </div>
        <div class="form-group">
          <label for="direccion">Direccion</label>
          <input
            type="text"
            class="form-control"
            id="direccion"
            placeholder="Direccion"
            v-model="form.direccion"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            placeholder="Correo Electronico"
            v-model="form.email"
            
          />
        </div>
        <div class="form-group">
          <label for="phone">Telefono</label>
          <input
            type="phone"
            class="form-control"
            id="phone"
            placeholder="Numero de Telefono"
            v-model="form.phone"
            required
          />
        </div>

        <div class="form-group">
          <label for="refer">Municipio</label>
          <select
            name="refer"
            class="form-control"
            id="refre"
            required
            v-model="form.municipio"
           
          >
            <option selected="true">Seleccione un Municipio</option>
            <option
              v-for="dato in datos"
              v-bind:key="dato"
              :value="dato.name"
            >
              {{ dato.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="refer">Horario Apertura</label>
          <b-form-timepicker 
            v-model="form.horarioApertura" 
            locale="en" 
            minutes-step="30"
            required
            ></b-form-timepicker>
        </div>

        <div class="form-group">
          <label for="refer">Horario Cierre</label>
          <b-form-timepicker 
            v-model="form.horarioCierre" 
            locale="en" 
            minutes-step= "30"
            required
           ></b-form-timepicker>
        </div>
        
        <div class="form-group">
          <label for="refer">Tipo de Centro</label><br>
          <select
            v-model="form.tipo"
            required
          >
            <option>Merendero</option>
            <option>Iglesia</option>
            <option>Institucion Municipal</option>
          </select>
        </div>

        <div class="form-group">
          <label for="phone">Pagina Web</label>
          <input
            type="text"
            class="form-control"
            id="web"
            placeholder="Sitio Web"
            v-model="form.web"
          />
        </div>

        <b-form-group label="Mapa" label-for="input-7">
          <maps @pointChanged="point= $event"></maps>
        </b-form-group>

        <br>
        <div class="row justify-content-md-center mb-3">
          <div class="col-1">
            <vue-recaptcha 
              :sitekey="this.siteKey" 
              @verify="onVerify()" 
              @expired="onExpired()" >
            </vue-recaptcha>
          </div>
          <div class="col-2 mr-5"></div>
        </div>
        <div v-if="captcha">
          <center><button type="submit" class="btn btn-primary">Enviar Centro</button></center>
        </div>
    </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Vue from "vue";
import VueRecaptcha from "vue-recaptcha";
import MapaDinam from './MapaDinam.vue';
Vue.prototype.$globalData = Vue.observable({
  fecha: new Date(),
});

export default {
  name: "Turno",
  components: {
    'maps': MapaDinam,
    VueRecaptcha,
  },
  data() {
    return {
      lat:'',
      form: {
        name: "",
        direccion: "",
        email: "",
        horarioApertura: "",
        horarioCierre:"",
        phone: "",
        tipo: "",
        web: "",
        municipio:"",
        file1:null,
        latitud: 0,
        longitud: 0,
      },
      siteKey:"6Lc5QgUaAAAAALijVaqz5msG3kWreRwt6D8Cbyo5",
      id: null,
      reactive: true,
      exito:false,
      respuesta: null,
      status: null,
      errores: null,
      datos:[],
      horarios:[],
      captcha:false,
      point:"",
      borrarHorario() {
        this.horarios = null;
        this.$forceUpdate();
      },
      childMessageReceived(punto){
        this.form.latitud= punto.lat;
        this.form.longitud= punto.lng;
      },
      submitForm() {
        if(this.captcha){
          let horaApertura = this.form.horarioApertura.substring(0,5);
          let horaCierre = this.form.horarioCierre.substring(0,5);
          let dicci = ({ nombre: this.form.name, 
                        direccion: this.form.direccion,
                        email: this.form.email, 
                        telefono: this.form.phone, 
                        hora_apertura: horaApertura, 
                        hora_cierre: horaCierre, 
                        tipo: this.form.tipo,
                        web: this.form.web,
                        municipio: this.form.municipio,
                        latitud: this.point.lat,
                        longitud: this.point.lng});
          axios
            .post(
              "https://admin-grupo16.proyecto2020.linti.unlp.edu.ar/centros",dicci
            )
            .then((response) => (this.respuesta = response['data'],
                                this.exito=response.status==201));
        } 

      },

      onVerify () {
        this.captcha=true;
      },
      onExpired () {
        console.log("Expired");
        this.captcha=false;
      },

      resetForm(){
        this.form.horarioApertura= "";
        this.form.horarioCierre="";
        this.form.phone='';
        this.form.name='';
        this.form.direccion='';
        this.form.email='';
        this.form.fecha='';
        this.form.municipio='';
        this.form.files=''
          
      },

      obtenerMunicipios(){
        axios.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios')
          .then(response => {
          this.datos = response.data.data.Town;
          console.log(this.datos)
          })
      },
    
    };
  },
  method: {
      previewFiles() {
        this.files = this.$refs.myFiles.files
      },
  },

  mounted() {
    this.form.fecha = String(new Date());
    this.obtenerMunicipios();
  },
};
</script>

<template>
  <div class="container card col-md-6 mt-3">
    <h2>Solicitar turno</h2>
    <div>
      <b-modal
        v-model="this.exito" hide-header-close no-close-on-backdrop
      >
      <b-container fluid>
        <center>
          <p style="color: green; text-decoration: underline "><b>¡Turno reservado Con Exito!</b></p>
          <div style="margin-bottom:10px">
            <p><b>Fecha:</b> {{ form.fecha }}</p>
            <p><b>Hora Inicio:</b> {{ form.horario }}</p>
          </div>
          <p><b>Los turnos serán de 30 MINUTOS.</b></p>
          <p style="color: #afafaf;">Por favor recordar acudir con tapaboca y mantener la distancia social dentro del centro</p>
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
    <div>
      <form v-on:submit.prevent="submitForm">
        <div class="form-group">
          <label for="name">Nombre</label>
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
          <label for="surname">Apellido</label>
          <input
            type="text"
            class="form-control"
            id="surname"
            placeholder="Apellido"
            v-model="form.surname"
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
            required
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

       <!--  <div class="form-group">
          <label for="refer">Centros de Ayuda</label>
          <select
            name="refer"
            class="form-control"
            id="refre"
            @mouseover="centroSelected()"
            v-model="idCentro"
            required
          >
           <option selected="true">Seleccione un Centro</option>
            <option
              v-for="dato in datos"
              v-bind:key="dato.nombre"
              :value="dato.id"
            >
              {{ dato.nombre }}
            </option>
          </select>
        </div>-->

        <div>
          <label for="example-datepicker">Seleccione una fecha</label>
          <datepicker
            :bootstrap-styling="true"
            input-class="form-control"
            :open-date="openDate"
            :disabled-dates="{ to: new Date() }"
            @selected="borrarHorario()"
            id="datepicker"
            v-model="form.fecha"
            required
          >
          </datepicker>
        </div>

        <div class="form-group">
          <label for="refer">Horarios de turnos disponibles</label>
          <select
            name="refer"
            class="form-control"
            id="refre"
            @mouseover="dateSelected()"
            v-model="form.horario"
            required
          >
            <option selected="true">Seleccione horario</option>
            <option
              v-for="turno in horarios"
              v-bind:key="turno"
              :value="turno.horaInicio"
            >
              {{ turno.horaInicio }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <button class="btn btn-primary">Crear turno</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Datepicker from "vuejs-datepicker";
import moment from "moment";
import Vue from "vue";
Vue.prototype.$globalData = Vue.observable({
  fecha: new Date(),
});

export default {
  name: "Turno",
  components: {
    Datepicker,
  },
  data() {
    return {
      form: {
        name: "",
        surname: "",
        email: "",
        horario: "",
        fecha: "",
        phone: "",
      },
      id: null,
      idCentro: null,
      fechaElegida:false,
      centroElegido:false,
      openDate: new Date(),
      reactive: true,
      date: new Date(),
      respuesta: null,
      status: null,
      errores: null,
      datos:[],
      horarios:[],
      exito:false,
      borrarHorario() {
        this.horarios = null;
        this.$forceUpdate();
      },
  
      dateSelected() {
        let valorFecha = document.getElementById("datepicker").value;
        this.fechaElegida= true;
        this.obtenerHorarios(valorFecha,this.idCentro);
        
      },

      centroSelected() {
        this.centroElegido=true;
        console.log("setee centro en true")
        if(this.fechaElegida){
          let valorFecha = document.getElementById("datepicker").value;
          this.obtenerHorarios(valorFecha, this.idCentro);
        }
      },

      obtenerHorarios(valorFecha, idCentro) {
        let fecha = moment(String(valorFecha)).format("YYYY-MM-DD");
        console.log(idCentro);
        axios
          .get(
            "https://admin-grupo16.proyecto2020.linti.unlp.edu.ar/centros/" +
              this.$route.params.id +
              "/turnos_disponibles?fecha=" +
              String(fecha)
          )
          .then((response) => (this.horarios = response.data.Turnos_Disponibles));
      },
      submitForm() {
        this.form.fecha = document.getElementById("datepicker").value;
        let fecha = moment(String(this.form.fecha)).format("YYYY-MM-DD");
        this.respuesta = null;
        let horarioIni = this.form.horario.substring(0,5);
        let horarioFin = null;
        if (horarioIni.substring(3,5)=="00"){
          horarioFin = horarioIni.substring(0,3)+"30";
        }else{
          let hora = String(parseInt(horarioIni.substring(0,2)) + 1)
          horarioFin = hora+":00";
        }
        console.log("HORARIO DE FIN: " + horarioFin);
        let dicci = { "idCentro": String(this.idCentro), "email_donante": this.form.email, "telefono_donante": this.form.phone, "horaInicio": horarioIni, "fecha": fecha, "horaFin":horarioFin, "nombre": this.form.name, "apellido": this.form.surname};
        console.log(dicci);
        const json = JSON.stringify(dicci);
        console.log(json);
        axios
          .post(
            "https://admin-grupo16.proyecto2020.linti.unlp.edu.ar/centros/" +
              String(this.idCentro) + 
              "/reservas",dicci
          )
          .then((response) => (this.respuesta = response['data'],
                              this.exito=response.status==201));
          

      },
      resetForm(){
          this.form.horario='';
          this.form.phone='';
          this.form.name='';
          this.form.surname='';
          this.form.email='';
          this.form.fecha='';
          
      },

      obtenerCentros(){
        console.log(this.$route.params)
        axios.get('https://admin-grupo16.proyecto2020.linti.unlp.edu.ar/centros')
          .then(response => {
          this.datos = response.data.centros;
          })
      },
    };
  },
  method: {
    obtenerIDCentro:function(id){
      return id;
    }
  },

  mounted() {
    this.form.fecha = String(new Date());
    this.idCentro= this.$route.params.id;
    this.obtenerHorarios(new Date());
    this.obtenerCentros();
  },
};
</script>
<template>
    <div style="justify-content:center; display:flex">
    <div style="background-color:white;width:50%;margin-top:50px;">
        <div class="modal-content">
            <div class="col-12">
                <div class="form-row">
                    <div class="form-group col-md-12">
                        <br>
                        <div style="text-align:center">
                            <label> Seleccione un Centro de Ayuda </label>
                        </div>
                        <select
                            name="refer"
                            class="form-control"
                            id="refre"
                            v-model="idCentro"
                            required
                        >
                            <option
                            v-for="dato in datos"
                            v-bind:key="dato.nombre"
                            :value="dato.id"
                            @click="changeStatus()"
                            >
                            {{ dato.nombre }}
                            </option>
                        </select>
                    </div>
                </div>
                <br>
                <div style="text-align:center">
                    <b-button class="btn btn-info" v-if="idCentro!=null" :to="{name:'Turno', params: {'id':idCentro}}">SIGUIENTE</b-button>
                    <button v-if="idCentro==null" disabled class="btn btn-info">SIGUIENTE</button><br><br>
                </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  import axios from "axios";
  export default {
    data () {
      return {
          centroElegido:false,
          faltaCentro:true,
          datos:[],
          idCentro:null,
      };
    },
    methods:{
        obtenerCentros(){
            console.log(this.$route.params)
            axios.get('https://admin-grupo16.proyecto2020.linti.unlp.edu.ar/centros')
            .then(response => {
            this.datos = response.data.centros;
            })
        },
        changeStatus(){
            this.centroElegido=true;
            this.faltaCentro=false;
            console.log("Falta Centro: " + this.faltaCentro);
            console.log("Centro Elegido: " + this.centroElegido);
        },
    },
    mounted(){
        this.obtenerCentros();
    }
  }
</script>
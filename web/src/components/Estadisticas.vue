<template>
  <div style="margin-top:30px">
    <div style="text-align:center">
      <h5 style="text-decoration:underline">Centros de Ayuda según Tipo de Centro</h5><br>
      <ve-pie :data="chartData"></ve-pie>
    </div> 
    <hr>
    <div style="text-align:center">
      <h5 style="text-decoration:underline">Centros de Ayuda según Localidad</h5><br>
      <ve-pie :data="chartData2"></ve-pie>
    </div>
    <hr>
    <div style="text-align:center">
      <h5 style="text-decoration:underline">Centros de Ayuda según formas de Contacto Online</h5><br>
      <ve-pie :data="chartData3"></ve-pie>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
  export default {
    data () {
      return {
        datos: [],
        resultado: [],
        chartData: {
          columns: ['date', 'PV'],
          rows: []
        },
        chartData2: {
          columns: ['date', 'PV'],
          rows: []
        },
        chartData3: {
          columns: ['date', 'PV'],
          rows: []
        },
        estadisticaCategoria(){
        const datos1 = new Map()
        for (var i = 0; i < this.datos.length; i++) {
          const obj= this.datos[i];
          if (datos1.has(obj.tipo)){
            datos1.set(obj.tipo, datos1.get(obj.tipo)+1);
          }else{datos1.set(obj.tipo,1)}
          }
        for (var [key, value] of datos1) {
          this.chartData.rows.push({ 'date': key, 'PV': value });
          }
        console.log(this.resultado);
      },
      estadisticaCategoria2(){
        const datos1 = new Map()
        for (var i = 0; i < this.datos.length; i++) {
          const obj= this.datos[i];
          if (datos1.has(obj.municipio)){
            datos1.set(obj.municipio, datos1.get(obj.municipio)+1);
          }else{datos1.set(obj.municipio,1)}
          }
        for (var [key, value] of datos1) {
          this.chartData2.rows.push({ 'date': key, 'PV': value });
          }
        console.log(this.resultado);
      },
      estadisticaCategoria3(){
        const datos1 = new Map()
        for (var i=0; i <this.datos.length; i++){
          const obj= this.datos[i];
          let web = obj.web!="";
          let email = obj.email!="";
          if (web && email){
            if (datos1.has("Ambos")){
              datos1.set("Ambos", datos1.get("Ambos")+1);
            }else{
              datos1.set("Ambos",1);
            }
          }else{
            if (web){
              if (datos1.has("Solo Web")){
                datos1.set("Solo Web", datos1.get("Solo Web")+1);
              }else{
                datos1.set("Solo Web",1);
              }
            }else{
              if (email){
                if (datos1.has("Solo Email")){
                  datos1.set("Solo Email", datos1.get("Solo Email")+1);
                }else{
                  datos1.set("Solo Email",1);
                }
              }else{
                if (datos1.has("Ninguno")){
                  datos1.set("Ninguno", datos1.get("Ninguno")+1);
                }else{
                  datos1.set("Ninguno",1);
                }
              }
            }
          }
        }
        for (var [key, value] of datos1) {
          this.chartData3.rows.push({ 'date': key, 'PV': value });
        }

      }
      };
    },
    mounted(){
    axios
          .get(
            "https://admin-grupo16.proyecto2020.linti.unlp.edu.ar/centros"
          )
          .then(response => {
          this.datos = response.data.centros;
          console.log(this.datos);
          this.estadisticaCategoria();
          this.estadisticaCategoria2();
          this.estadisticaCategoria3();
          })
  }
  }
</script>
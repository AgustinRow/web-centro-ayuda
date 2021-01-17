import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../components/Home.vue";
import Centro from "../components/Centro.vue";
//import Map from "/components/Map.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/nuevo_centro",
    name: "Centro",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Centro,
  },
  {
    path: "/mapa",
    name: "Mapa2",
    component: () =>
      import(/* webpackChunkName: "Mapa" */ "../components/Mapa2.vue"),
  },
  {
    path: "/mapadin",
    name: "MapaDinam",
    component: () =>
      import(/* webpackChunkName: "Mapa" */ "../components/MapaDinam.vue"),
  },
  {
    path: "/turno/:id",
    name: "Turno",
    component: () =>
      import(/* webpackChunkName: "Mapa" */ "../components/Turno.vue"),
  },
  {
    path:"/estadisticas",
    name: "Estadisticas",
    component: () =>
      import(/* webpackChunkName: "Mapa" */ "../components/Estadisticas.vue"),
  },
  {
    path:"/seleccionar-centro",
    name: "SeleccionarCentro",
    component: () =>
      import(/* webpackChunkName: "Mapa" */ "../components/SeleccionarCentro.vue"),
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;

import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import * as VeeValidate from "vee-validate";
//---------------//
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
//---------------//
import "leaflet/dist/leaflet.css";
import { Icon } from "leaflet";
//---------------//
import VCharts from "v-charts";
// Install BootstrapVue
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);

Vue.use(VeeValidate);
Vue.config.productionTip = false;
Vue.use(VCharts);
new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

import Vue from 'vue'
import App from './materialupdate.vue'
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueFormulate from '@braid/vue-formulate'

Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(VueFormulate);

new Vue({
  render: h => h(App),
}).$mount('#materialupdate')

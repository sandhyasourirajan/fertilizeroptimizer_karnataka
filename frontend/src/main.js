// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import VeeValidate from 'vee-validate';
import PageHeader from './components/PageHeader.vue'
import FertilizerOptimizer from './components/FertilizerOptimizer.vue'
import AddFertilizer from './components/AddFertilizer.vue'

// import dialog1 from './components/dialog1.vue'
import store from './store/store'
import VueStash from 'vue-stash';

Vue.use(Vuetify, { theme: {
  primary: '#B11117',
  secondary: '#B11117',
  accent: '#B11117',
  error: '#B11117',
  info: '#B11117',
  success: '#B11117',
  warning: '#B11117'
}})

Vue.use(VueStash)
Vue.use(VeeValidate);

Vue.config.productionTip = false

Vue.component('page-header', PageHeader)
Vue.component('fertilizer-optimize', FertilizerOptimizer)
Vue.component('add-fertilizer', AddFertilizer)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  data:{store},
  router,
  render: h => h(App)
})

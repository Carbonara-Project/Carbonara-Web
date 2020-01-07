import Vue from 'vue'

import store from './store'
import router from './router'

import pubnub from './pubnub'

import VueHighlightJS from 'vue-highlightjs'
Vue.use(VueHighlightJS)

import VeeValidate from 'vee-validate'
Vue.use(VeeValidate)

import App from './components/App.vue'

new Vue({
  el: '#app',
  store,
  router,
  components: {
    App
  },
  render: h => h(App)
})

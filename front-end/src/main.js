import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false


// Make websocket accessible by all Vue components. First created in LogIn.vue.
Vue.prototype.$websocket = null;

/*var store = {
  debug: true,
  state: {
    websocket: null
  },

  sendWebSocketMessage(json_string) {
    if (this.debug) {
      /* eslint-disable no-console */
      //console.log('sendWebSocketMessage triggered with ', json_string);
      /* eslint-enable no-console */
    /*}
    this.websocket.send(json_string);
  }
}*/

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

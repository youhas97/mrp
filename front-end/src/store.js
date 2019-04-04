import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

/*
Shares the state of Vuex Store across all Vue components.
In this case, we can use the same websocket in all of our components.
'websocket' is first assigned a WebSocket in LogIn.vue.
*/
export default new Vuex.Store({
  state: {
    websocket: null,
    meObj: null
  },
  mutations: {

  },
  actions: {

  }
})

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

/*
Shares the state of Vuex Store across all Vue components.
In this case, we can use the same websocket in all of our components.
'websocket' is first assigned a WebSocket in LogIn.vue.
*/

const moduleAlert = {
    state: {
        alerting: false,
        buttonText: "Larma"
    }
}

export default new Vuex.Store({
    state: {
        websocket: null,
        meObj: {
            "id": null,
            "pos": null,
            "name": null,
            "group": null,
            "needHelp": null
        },
        username: "",
        allUsers: {},
        allMarkers: {},
    },
    mutations: {

    },
    actions: {

    },
    modules: {
        alert: moduleAlert,
    }

})

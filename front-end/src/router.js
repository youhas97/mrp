import Vue from 'vue'
import Router from 'vue-router'
import LogIn from './components/LogIn.vue'
import Map from './components/MapBase.vue'
import Mobile from './components/Mobile.vue'
import CommandCenter from './components/CommandCenter.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'login',
            component: LogIn
        },
        {
            path: '/map',
            name: 'map',
            component: Map
        },
        {
            path: '/mobile',
            name: 'mobile',
            component: Mobile
        },
        {
            path: '/cc',
            name: 'commandcenter',
            component: CommandCenter
        }
    ]
})

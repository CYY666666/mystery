import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Customer from '../views/Customer.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Customer',
    component: Customer
  },
  {
    path: '/customer',
    name: 'Customer',
    component: Customer
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router

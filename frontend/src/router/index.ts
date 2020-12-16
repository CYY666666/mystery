import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Customer from '../views/Customer.vue'
import Login from '../views/Login.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    component: Customer
  },
  {
    path: '/customer',
    name: 'Customer',
    component: Customer
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router

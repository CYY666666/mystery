import api from '../api'

const { get, post } = api
export const getAllCustomer = (params: any) => get('/customer', params)
export const insertCustomer = (data: any) => post('/customer', data)
export const restartTask = (data: any) => post('/customer/restart_task', data)

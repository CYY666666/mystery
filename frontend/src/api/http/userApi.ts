import api from '../api'

const { post } = api
export const loginApi = (data: any) => post('/login/access-token', data)
export const resetPasswordApi = (data: any) => post('/user/reset_password', data)

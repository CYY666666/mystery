import api from '../api'

const { post, get } = api
export const loginApi = (data: any) => post('/login/access-token', data)
export const resetPasswordApi = (data: any) => post('/user/reset_password', data)
export const getAllUsersApi = () => get('/user/get_users', null)

import api from '../api'

const { post } = api
export const loginApi = (data: any) => post('/login/access-token', data)

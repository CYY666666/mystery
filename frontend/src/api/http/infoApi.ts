import api from '../api'

const { get } = api
export const getInfo = () => get('/info', null)

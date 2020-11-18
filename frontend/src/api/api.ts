import axios from 'axios'
const baseURL = process.env.VUE_APP_BASE_API

axios.interceptors.request.use(config => {
  if (localStorage.token) {
    config.headers.Authorization = 'Bearer ' + localStorage.token
  }
  return config
}, err => Promise.reject(err))

axios.interceptors.response.use(res => res, err => {
  return Promise.reject(err)
})
function axiosHttp (method: string, url: string, data: any) {
  const config = {
    url,
    method,
    baseURL,
    timeout: 30000,
    params: ['GET', 'DELETE'].includes(method) ? data : null,
    data: ['POST', 'PUT'].includes(method) ? data : null,
    headers: {
      'Content-Type': 'application/json'
    }
  }
  return new Promise((resolve, reject) => {
    axios(config as any).then(res => resolve(res)).catch(err => reject(err))
  })
}

export default {
  get: (url: string, data: any) => axiosHttp('GET', url, data),
  post: (url: string, data: any) => axiosHttp('POST', url, data),
  put: (url: string, data: any) => axiosHttp('PUT', url, data),
  delete: (url: string, data: any) => axiosHttp('DELETE', url, data)
}

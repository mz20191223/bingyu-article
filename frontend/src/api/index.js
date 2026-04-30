import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  console.log('Token from localStorage:', token ? 'exists' : 'null')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('Authorization header set:', config.headers.Authorization)
  }
  console.log('Request URL:', config.baseURL + config.url)
  return config
})

api.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code === 200) {
      return res
    } else {
      if (res.code === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        router.push('/login')
      }
      return Promise.reject(new Error(res.msg || 'Error'))
    }
  },
  error => {
    console.error('Response error:', error)
    return Promise.reject(error)
  }
)

export default api
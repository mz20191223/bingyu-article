import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

request.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  response => {
    // 如果是blob类型（如下载文件），直接返回原始响应
    if (response.config.responseType === 'blob') {
      return response
    }
    
    const res = response.data
    if (res.code === 200) {
      return res
    } else {
      if (res.code === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        window.location.href = '/login'
      }
      return Promise.reject(new Error(res.msg || 'Error'))
    }
  },
  error => {
    return Promise.reject(error)
  }
)

export default request
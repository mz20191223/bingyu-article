import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'))
  const menus = ref([])
  const permissions = ref([])

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUserInfo = (info) => {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  const setMenus = (newMenus) => {
    menus.value = newMenus
  }

  const setPermissions = (newPermissions) => {
    permissions.value = newPermissions
  }

  const logout = () => {
    token.value = ''
    userInfo.value = {}
    menus.value = []
    permissions.value = []
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  async function login(username, password) {
    const res = await api.post('/auth/login', { username, password })
    setToken(res.data.token)
    setUserInfo(res.data.userInfo)
    return res.data
  }

  async function getUserInfo() {
    const res = await api.get('/auth/info')
    setUserInfo(res.data)
    setMenus(res.data.menus || [])
    setPermissions(res.data.permissions || [])
    return res.data
  }

  return {
    token,
    userInfo,
    menus,
    permissions,
    setToken,
    setUserInfo,
    setMenus,
    setPermissions,
    logout,
    login,
    getUserInfo
  }
})
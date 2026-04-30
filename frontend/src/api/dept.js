import request from '@/utils/request'

export const getDeptList = () => {
  return request({
    url: '/api/dept',
    method: 'get'
  })
}

export const addDept = (data) => {
  return request({
    url: '/api/dept',
    method: 'post',
    data
  })
}

export const updateDept = (data) => {
  return request({
    url: `/api/dept/${data.deptId}`,
    method: 'put',
    data
  })
}

export const deleteDept = (deptId) => {
  return request({
    url: `/api/dept/${deptId}`,
    method: 'delete'
  })
}
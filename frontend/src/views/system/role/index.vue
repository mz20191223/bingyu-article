<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>角色管理</span>
          <el-button type="primary" @click="handleAdd">新增角色</el-button>
        </div>
      </template>
      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="roleId" label="ID" width="80" />
        <el-table-column prop="roleName" label="角色名称" />
        <el-table-column prop="roleCode" label="角色编码" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'info'">{{ row.status === 0 ? '正常' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="角色名称" prop="roleName"><el-input v-model="form.roleName" placeholder="请输入角色名称" /></el-form-item>
        <el-form-item label="角色编码" prop="roleCode"><el-input v-model="form.roleCode" placeholder="请输入角色编码" /></el-form-item>
        <el-form-item label="状态"><el-switch v-model="form.status" :active-value="0" :inactive-value="1" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" placeholder="请输入备注" /></el-form-item>
        <el-form-item label="权限菜单">
          <el-tree
            ref="menuTreeRef"
            :data="menuTreeData"
            :props="treeProps"
            show-checkbox
            node-key="menuId"
            :default-expand-all="true"
            :default-checked-keys="defaultCheckedKeys"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()
const menuTreeRef = ref()
const menuTreeData = ref([])
const defaultCheckedKeys = ref([])

const form = reactive({ roleId: null, roleName: '', roleCode: '', status: 0, remark: '' })

const rules = { 
  roleName: [{ required: true, message: '请输入角色名称', trigger: 'blur' }], 
  roleCode: [{ required: true, message: '请输入角色编码', trigger: 'blur' }] 
}

const treeProps = {
  children: 'children',
  label: 'menuName'
}

const loadData = async () => { 
  loading.value = true
  try { 
    const res = await api.get('/roles', { params: { page: 1, pageSize: 100 } })
    tableData.value = res.data.list || [] 
  } catch (error) { 
    console.error(error) 
  } finally { 
    loading.value = false 
  } 
}

const loadMenuTree = async () => {
  try {
    const res = await api.get('/menus/tree')
    menuTreeData.value = res.data || []
  } catch (error) {
    console.error('加载菜单树失败:', error)
  }
}

const handleAdd = async () => { 
  Object.assign(form, { roleId: null, roleName: '', roleCode: '', status: 0, remark: '' })
  dialogTitle.value = '新增角色'
  defaultCheckedKeys.value = []
  await loadMenuTree()
  dialogVisible.value = true 
}

const handleEdit = async (row) => {
  Object.assign(form, { ...row })
  dialogTitle.value = '编辑角色'
  await loadMenuTree()
  
  try {
    const res = await api.get(`/roles/${row.roleId}/menus`)
    defaultCheckedKeys.value = res.data || []
  } catch (error) {
    defaultCheckedKeys.value = []
  }
  
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该角色吗？', '提示', { type: 'warning' })
    await api.delete(`/roles/${row.roleId}`)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => { 
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => { 
    if (valid) { 
      try {
        const checkedKeys = menuTreeRef.value.getCheckedKeys()
        const data = { ...form, menuIds: checkedKeys }
        
        if (form.roleId) { 
          await api.put(`/roles/${form.roleId}`, data) 
        } else { 
          await api.post('/roles', data) 
        }
        
        ElMessage.success('操作成功')
        dialogVisible.value = false
        loadData()
      } catch (error) { 
        ElMessage.error(error.message || '操作失败') 
      } 
    } 
  }) 
}

onMounted(() => { 
  loadData() 
})
</script>

<style scoped>
.page-container { padding: 20px }
.card-header { display: flex; justify-content: space-between; align-items: center }
</style>
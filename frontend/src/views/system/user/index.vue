<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleAdd">新增用户</el-button>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="userId" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="nickname" label="昵称" />
        <el-table-column prop="deptName" label="所属部门" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'info'">{{ row.status === 0 ? '正常' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" layout="total, prev, pager, next" style="margin-top: 20px; justify-content: flex-end" @change="loadData" />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username"><el-input v-model="form.username" placeholder="请输入用户名" /></el-form-item>
        <el-form-item label="密码" prop="password" v-if="!form.id"><el-input v-model="form.password" type="password" placeholder="请输入密码" /></el-form-item>
        <el-form-item label="昵称"><el-input v-model="form.nickname" placeholder="请输入昵称" /></el-form-item>
        <el-form-item label="所属部门"><el-select v-model="form.deptId" placeholder="请选择部门"><el-option v-for="dept in deptOptions" :key="dept.deptId" :label="dept.deptName" :value="dept.deptId" /></el-select></el-form-item>
        <el-form-item label="手机号"><el-input v-model="form.phone" placeholder="请输入手机号" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" placeholder="请输入邮箱" /></el-form-item>
        <el-form-item label="状态"><el-switch v-model="form.status" :active-value="0" :inactive-value="1" /></el-form-item>
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

const loading = ref(false), tableData = ref([]), pagination = reactive({ page: 1, pageSize: 10, total: 0 }), dialogVisible = ref(false), dialogTitle = ref(''), formRef = ref()
const form = reactive({ id: null, username: '', password: '', nickname: '', deptId: null, phone: '', email: '', status: 0 })
const rules = { username: [{ required: true, message: '请输入用户名', trigger: 'blur' }], password: [{ required: true, message: '请输入密码', trigger: 'blur' }] }
const deptOptions = ref([])

const loadData = async () => { loading.value = true; try { const res = await api.get('/users', { params: { page: pagination.page, pageSize: pagination.pageSize } }); tableData.value = res.data.list; pagination.total = res.data.total } catch (error) { ElMessage.error('加载失败') } finally { loading.value = false } }
const loadDeptOptions = async () => { try { const res = await api.get('/dept/all'); deptOptions.value = res.data } catch (error) { ElMessage.error('加载部门失败') } }
const handleAdd = () => { Object.assign(form, { id: null, username: '', password: '', nickname: '', deptId: null, phone: '', email: '', status: 0 }); dialogTitle.value = '新增用户'; dialogVisible.value = true }
const handleEdit = (row) => { Object.assign(form, { id: row.userId, username: row.username, password: '', nickname: row.nickname, deptId: row.deptId, phone: row.phone, email: row.email, status: row.status }); dialogTitle.value = '编辑用户'; dialogVisible.value = true }
const handleDelete = async (row) => { try { await ElMessageBox.confirm('确定删除?', '提示', { type: 'warning' }); await api.delete(`/users/${row.userId}`); ElMessage.success('删除成功'); loadData() } catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') } }
const handleSubmit = async () => { if (!formRef.value) return; await formRef.value.validate(async (valid) => { if (valid) { try { form.id ? await api.put(`/users/${form.id}`, form) : await api.post('/users', form); ElMessage.success('操作成功'); dialogVisible.value = false; loadData() } catch (error) { ElMessage.error(error.message || '操作失败') } } }) }
onMounted(() => { loadData(); loadDeptOptions() })
</script>

<style scoped>
.page-container { padding: 20px }
.card-header { display: flex; justify-content: space-between; align-items: center }
</style>

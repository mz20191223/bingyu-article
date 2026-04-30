<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>关键词管理</span>
          <div>
            <el-button type="primary" @click="handleAdd">新增</el-button>
            <el-button @click="handleImport">批量导入</el-button>
          </div>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="keyword" label="关键词" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'info'">{{ row.status === 0 ? '启用' : '禁用' }}</el-tag>
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="400px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="关键词" prop="keyword">
          <el-input v-model="form.keyword" placeholder="请输入关键词" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="importVisible" title="批量导入" width="400px">
      <el-upload ref="uploadRef" :auto-upload="false" :limit="1" accept=".xlsx,.xls" :on-change="handleFileChange">
        <el-button>选择文件</el-button>
        <template #tip>
          <div class="el-upload__tip">支持.xlsx/.xls格式，第一列为关键词</div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="importVisible = false">取消</el-button>
        <el-button type="primary" @click="handleImportSubmit">导入</el-button>
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
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })
const dialogVisible = ref(false)
const importVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()
const uploadRef = ref()
const form = reactive({ id: null, keyword: '', status: 1 })
const rules = { keyword: [{ required: true, message: '请输入关键词', trigger: 'blur' }] }
let importFile = null

const loadData = async () => {
  loading.value = true
  try {
    const res = await api.get('/keywords', { params: { page: pagination.page, pageSize: pagination.pageSize } })
    tableData.value = res.data.list
    pagination.total = res.data.total
  } catch (error) { ElMessage.error('加载失败') }
  finally { loading.value = false }
}

const handleAdd = () => { Object.assign(form, { id: null, keyword: '', status: 1 }); dialogTitle.value = '新增关键词'; dialogVisible.value = true }
const handleEdit = (row) => { Object.assign(form, { id: row.id, keyword: row.keyword, status: row.status }); dialogTitle.value = '编辑关键词'; dialogVisible.value = true }
const handleDelete = async (row) => {
  try { await ElMessageBox.confirm('确定删除?', '提示', { type: 'warning' }); await api.delete(`/keywords/${row.id}`); ElMessage.success('删除成功'); loadData() }
  catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') }
}
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try { form.id ? await api.put(`/keywords/${form.id}`, form) : await api.post('/keywords', form); ElMessage.success('操作成功'); dialogVisible.value = false; loadData() }
      catch (error) { ElMessage.error(error.message || '操作失败') }
    }
  })
}
const handleImport = () => { importFile = null; importVisible.value = true }
const handleFileChange = (file) => { importFile = file.raw }
const handleImportSubmit = async () => {
  if (!importFile) return ElMessage.warning('请选择文件')
  const formData = new FormData()
  formData.append('file', importFile)
  try {
    await api.post('/keywords/import', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    ElMessage.success('导入成功')
    importVisible.value = false
    loadData()
  } catch (error) { ElMessage.error(error.message || '导入失败') }
}
onMounted(() => { loadData() })
</script>

<style scoped>
.page-container { padding: 20px }
.card-header { display: flex; justify-content: space-between; align-items: center }
</style>

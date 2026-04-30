<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>图片管理</span>
          <el-button type="primary" @click="handleAdd">新增图片</el-button>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="url" label="图片" width="120">
          <template #default="{ row }">
            <el-image :src="row.url" style="width: 80px; height: 60px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="positionType" label="插入位置" width="100" />
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="图片URL" prop="url">
          <el-input v-model="form.url" placeholder="请输入图片URL" />
        </el-form-item>
        <el-form-item label="插入位置" prop="positionType">
          <el-select v-model="form.positionType" style="width: 100%">
            <el-option label="自动" value="auto" />
            <el-option label="首段" value="first" />
            <el-option label="尾段" value="last" />
            <el-option label="自定义" value="custom" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="form.positionType === 'custom'" label="段落号">
          <el-input-number v-model="form.positionValue" :min="1" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="0" :inactive-value="1" />
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
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()
const form = reactive({ id: null, url: '', positionType: 'auto', positionValue: 1, status: 1 })
const rules = { url: [{ required: true, message: '请输入图片URL', trigger: 'blur' }] }

const loadData = async () => {
  loading.value = true
  try {
    const res = await api.get('/images', { params: { page: pagination.page, pageSize: pagination.pageSize } })
    tableData.value = res.data.list
    pagination.total = res.data.total
  } catch (error) { ElMessage.error('加载失败') }
  finally { loading.value = false }
}

const handleAdd = () => { Object.assign(form, { id: null, url: '', positionType: 'auto', positionValue: 1, status: 1 }); dialogTitle.value = '新增图片'; dialogVisible.value = true }
const handleEdit = (row) => { Object.assign(form, { id: row.id, url: row.url, positionType: row.positionType, positionValue: row.positionValue, status: row.status }); dialogTitle.value = '编辑图片'; dialogVisible.value = true }
const handleDelete = async (row) => {
  try { await ElMessageBox.confirm('确定删除?', '提示', { type: 'warning' }); await api.delete(`/images/${row.id}`); ElMessage.success('删除成功'); loadData() }
  catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') }
}
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try { form.id ? await api.put(`/images/${form.id}`, form) : await api.post('/images', form); ElMessage.success('操作成功'); dialogVisible.value = false; loadData() }
      catch (error) { ElMessage.error(error.message || '操作失败') }
    }
  })
}
onMounted(() => { loadData() })
</script>

<style scoped>
.page-container { padding: 20px }
.card-header { display: flex; justify-content: space-between; align-items: center }
</style>

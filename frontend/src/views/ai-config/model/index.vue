<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>AI模型配置</span>
          <el-button type="primary" @click="handleAdd">新增模型</el-button>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="模型名称" />
        <el-table-column prop="provider" label="服务商" width="100">
          <template #default="{ row }">
            <el-tag>{{ row.provider === 'openai' ? 'OpenAI' : '智谱AI' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="apiUrl" label="API地址" show-overflow-tooltip />
        <el-table-column prop="modelName" label="模型" width="150" />
        <el-table-column prop="isDefault" label="默认" width="80">
          <template #default="{ row }"><el-tag v-if="row.isDefault === 1" type="success">默认</el-tag></template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }"><el-tag :type="row.status === 0 ? 'success' : 'info'">{{ row.status === 0 ? '启用' : '禁用' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="success" link @click="handleSetDefault(row)" v-if="row.isDefault !== 1">设为默认</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" layout="total, prev, pager, next" style="margin-top: 20px; justify-content: flex-end" @change="loadData" />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="模型名称" prop="name"><el-input v-model="form.name" placeholder="请输入模型名称" /></el-form-item>
        <el-form-item label="服务商" prop="provider">
          <el-select v-model="form.provider" style="width: 100%">
            <el-option label="OpenAI" value="openai" />
            <el-option label="智谱AI" value="zhipuai" />
          </el-select>
        </el-form-item>
        <el-form-item label="API Key" prop="apiKey"><el-input v-model="form.apiKey" placeholder="请输入API Key" /></el-form-item>
        <el-form-item label="API地址" prop="apiUrl"><el-input v-model="form.apiUrl" placeholder="如: https://api.openai.com/v1" /></el-form-item>
        <el-form-item label="模型名称"><el-input v-model="form.modelName" placeholder="如: gpt-3.5-turbo" /></el-form-item>
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
const form = reactive({ id: null, name: '', provider: 'openai', apiKey: '', apiUrl: '', modelName: '', status: 1 })
const rules = { name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }], provider: [{ required: true, message: '请选择服务商', trigger: 'change' }], apiKey: [{ required: true, message: '请输入API Key', trigger: 'blur' }], apiUrl: [{ required: true, message: '请输入API地址', trigger: 'blur' }] }

const loadData = async () => { loading.value = true; try { const res = await api.get('/models', { params: { page: pagination.page, pageSize: pagination.pageSize } }); tableData.value = res.data.list; pagination.total = res.data.total } catch (error) { ElMessage.error('加载失败') } finally { loading.value = false } }
const handleAdd = () => { Object.assign(form, { id: null, name: '', provider: 'openai', apiKey: '', apiUrl: '', modelName: '', status: 1 }); dialogTitle.value = '新增模型'; dialogVisible.value = true }
const handleEdit = (row) => { Object.assign(form, { id: row.id, name: row.name, provider: row.provider, apiKey: row.apiKey, apiUrl: row.apiUrl, modelName: row.modelName, status: row.status }); dialogTitle.value = '编辑模型'; dialogVisible.value = true }
const handleDelete = async (row) => { try { await ElMessageBox.confirm('确定删除?', '提示', { type: 'warning' }); await api.delete(`/models/${row.id}`); ElMessage.success('删除成功'); loadData() } catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') } }
const handleSetDefault = async (row) => { try { await api.put(`/models/${row.id}/default`); ElMessage.success('设置成功'); loadData() } catch (error) { ElMessage.error('设置失败') } }
const handleSubmit = async () => { if (!formRef.value) return; await formRef.value.validate(async (valid) => { if (valid) { try { const data = { name: form.name, provider: form.provider, apiKey: form.apiKey, apiUrl: form.apiUrl, modelName: form.modelName, status: form.status }; form.id ? await api.put(`/models/${form.id}`, data) : await api.post('/models', data); ElMessage.success('操作成功'); dialogVisible.value = false; loadData() } catch (error) { ElMessage.error(error.message || '操作失败') } } }) }
onMounted(() => { loadData() })
</script>

<style scoped>
.page-container { padding: 20px }
.card-header { display: flex; justify-content: space-between; align-items: center }
</style>

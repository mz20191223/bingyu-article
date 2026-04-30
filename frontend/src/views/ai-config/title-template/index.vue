<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>标题模板</span>
          <el-button type="primary" @click="handleAdd">新增模板</el-button>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="模板名称" />
        <el-table-column prop="businessType" label="业务类型" width="120" />
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
        <el-form-item label="模板名称" prop="name"><el-input v-model="form.name" placeholder="请输入模板名称" /></el-form-item>
        <el-form-item label="业务类型"><el-input v-model="form.businessType" placeholder="请输入业务类型" /></el-form-item>
        <el-form-item label="标题提示词" prop="titlePrompt"><el-input v-model="form.titlePrompt" type="textarea" :rows="5" placeholder="请输入标题提示词，可以使用{product_name}、{keywords}占位符" /></el-form-item>
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
const form = reactive({ id: null, name: '', businessType: '', titlePrompt: '', status: 1 })
const rules = { name: [{ required: true, message: '请输入模板名称', trigger: 'blur' }], titlePrompt: [{ required: true, message: '请输入标题提示词', trigger: 'blur' }] }

const loadData = async () => { loading.value = true; try { const res = await api.get('/title-templates', { params: { page: pagination.page, pageSize: pagination.pageSize } }); tableData.value = res.data.list; pagination.total = res.data.total } catch (error) { ElMessage.error('加载失败') } finally { loading.value = false } }
const handleAdd = () => { Object.assign(form, { id: null, name: '', businessType: '', titlePrompt: '', status: 1 }); dialogTitle.value = '新增模板'; dialogVisible.value = true }
const handleEdit = (row) => { Object.assign(form, { id: row.id, name: row.name, businessType: row.businessType, titlePrompt: row.titlePrompt, status: row.status }); dialogTitle.value = '编辑模板'; dialogVisible.value = true }
const handleDelete = async (row) => { try { await ElMessageBox.confirm('确定删除?', '提示', { type: 'warning' }); await api.delete(`/title-templates/${row.id}`); ElMessage.success('删除成功'); loadData() } catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') } }
const handleSetDefault = async (row) => { try { await api.put(`/title-templates/${row.id}/default`); ElMessage.success('设置成功'); loadData() } catch (error) { ElMessage.error('设置失败') } }
const handleSubmit = async () => { if (!formRef.value) return; await formRef.value.validate(async (valid) => { if (valid) { try { form.id ? await api.put(`/title-templates/${form.id}`, form) : await api.post('/title-templates', form); ElMessage.success('操作成功'); dialogVisible.value = false; loadData() } catch (error) { ElMessage.error(error.message || '操作失败') } } }) }
onMounted(() => { loadData() })
</script>

<style scoped>
.page-container { padding: 20px }
.card-header { display: flex; justify-content: space-between; align-items: center }
</style>

<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>内容模板</span>
          <el-button type="primary" @click="handleAdd">新增模板</el-button>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="模板名称" />
        <el-table-column prop="productNames" label="关联产品" width="150">
          <template #default="{ row }">
            <span v-if="row.productNames && row.productNames.length > 0">{{ row.productNames.join(', ') }}</span>
            <span v-else class="text-gray">未关联</span>
          </template>
        </el-table-column>
        <el-table-column prop="businessType" label="业务类型" width="120" />
        <el-table-column prop="isDefault" label="默认" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.isDefault === 1" type="success">默认</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'info'">{{ row.status === 0 ? '启用' : '禁用' }}</el-tag>
          </template>
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="模板名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入模板名称" />
        </el-form-item>
        <el-form-item label="关联产品">
          <el-select v-model="form.productIds" placeholder="请选择产品（支持多选）" style="width: 100%" multiple>
            <el-option v-for="p in products" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="业务类型">
          <el-input v-model="form.businessType" placeholder="请输入业务类型" />
        </el-form-item>
        <el-form-item label="Meta标题">
          <el-input v-model="form.metaTitle" placeholder="请输入Meta标题" />
        </el-form-item>
        <el-form-item label="Meta描述">
          <el-input v-model="form.metaDescription" type="textarea" :rows="2" placeholder="请输入Meta描述" />
        </el-form-item>
        <el-form-item label="关键词提示词">
          <el-input v-model="form.keywordPrompt" type="textarea" :rows="3" placeholder="请输入关键词提示词，可以使用{keywords}占位符" />
        </el-form-item>
        <el-form-item label="内容提示词" prop="contentPrompt">
          <el-input v-model="form.contentPrompt" type="textarea" :rows="5" placeholder="请输入内容提示词，可以使用{product_name}、{product_url}、{keywords}占位符" />
        </el-form-item>
        <el-form-item label="结论提示词">
          <el-input v-model="form.conclusionPrompt" type="textarea" :rows="3" placeholder="请输入结论提示词" />
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
const products = ref([])
const form = reactive({ id: null, name: '', productIds: [], businessType: '', metaTitle: '', metaDescription: '', keywordPrompt: '', contentPrompt: '', conclusionPrompt: '', status: 1 })
const rules = { name: [{ required: true, message: '请输入模板名称', trigger: 'blur' }], contentPrompt: [{ required: true, message: '请输入内容提示词', trigger: 'blur' }] }

const loadData = async () => {
  loading.value = true
  try {
    const res = await api.get('/content-templates', { params: { page: pagination.page, pageSize: pagination.pageSize } })
    tableData.value = res.data.list
    pagination.total = res.data.total
  } catch (error) { ElMessage.error('加载失败') }
  finally { loading.value = false }
}

const loadProducts = async () => {
  try {
    const res = await api.get('/products')
    products.value = res.data.list || []
  } catch (error) { console.error('加载产品失败') }
}

const handleAdd = () => { Object.assign(form, { id: null, name: '', productIds: [], businessType: '', metaTitle: '', metaDescription: '', keywordPrompt: '', contentPrompt: '', conclusionPrompt: '', status: 1 }); dialogTitle.value = '新增模板'; dialogVisible.value = true }
const handleEdit = (row) => { Object.assign(form, { id: row.id, name: row.name, productIds: row.productIds || [], businessType: row.businessType, metaTitle: row.metaTitle, metaDescription: row.metaDescription, keywordPrompt: row.keywordPrompt, contentPrompt: row.contentPrompt, conclusionPrompt: row.conclusionPrompt, status: row.status }); dialogTitle.value = '编辑模板'; dialogVisible.value = true }
const handleDelete = async (row) => {
  try { await ElMessageBox.confirm('确定删除?', '提示', { type: 'warning' }); await api.delete(`/content-templates/${row.id}`); ElMessage.success('删除成功'); loadData() }
  catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') }
}
const handleSetDefault = async (row) => {
  try { await api.put(`/content-templates/${row.id}/default`); ElMessage.success('设置成功'); loadData() }
  catch (error) { ElMessage.error('设置失败') }
}
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const data = { name: form.name, productIds: form.productIds, businessType: form.businessType, metaTitle: form.metaTitle, metaDescription: form.metaDescription, keywordPrompt: form.keywordPrompt, contentPrompt: form.contentPrompt, conclusionPrompt: form.conclusionPrompt, status: form.status }
        form.id ? await api.put(`/content-templates/${form.id}`, data) : await api.post('/content-templates', data)
        ElMessage.success('操作成功'); dialogVisible.value = false; loadData()
      } catch (error) { ElMessage.error(error.message || '操作失败') }
    }
  })
}
onMounted(() => { loadData(); loadProducts() })
</script>

<style scoped>
.page-container { padding: 20px }
.card-header { display: flex; justify-content: space-between; align-items: center }
</style>

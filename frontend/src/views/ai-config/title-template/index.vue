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
        <el-table-column prop="productNames" label="关联产品" width="150">
          <template #default="{ row }">
            <span v-if="row.productNames && row.productNames.length > 0">{{ row.productNames.join(', ') }}</span>
            <span v-else class="text-gray">未关联</span>
          </template>
        </el-table-column>
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
        <el-form-item label="关联产品">
          <el-select v-model="form.productIds" placeholder="请选择产品（支持多选）" style="width: 100%" multiple>
            <el-option v-for="p in products" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
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

const loading = ref(false), tableData = ref([]), pagination = reactive({ page: 1, pageSize: 10, total: 0 }), dialogVisible = ref(false), dialogTitle = ref(''), formRef = ref(), products = ref([])
const form = reactive({ id: null, name: '', productIds: [], businessType: '', titlePrompt: '', status: 1 })
const rules = { name: [{ required: true, message: '请输入模板名称', trigger: 'blur' }], titlePrompt: [{ required: true, message: '请输入标题提示词', trigger: 'blur' }] }

const loadData = async () => { loading.value = true; try { const res = await api.get('/title-templates', { params: { page: pagination.page, pageSize: pagination.pageSize } }); tableData.value = res.data.list; pagination.total = res.data.total } catch (error) { ElMessage.error('加载失败') } finally { loading.value = false } }

const loadProducts = async () => {
  try {
    const res = await api.get('/products')
    products.value = res.data.list || []
  } catch (error) { console.error('加载产品失败') }
}

const handleAdd = () => { Object.assign(form, { id: null, name: '', productIds: [], businessType: '', titlePrompt: '', status: 1 }); dialogTitle.value = '新增模板'; dialogVisible.value = true }
const handleEdit = (row) => { Object.assign(form, { id: row.id, name: row.name, productIds: row.productIds || [], businessType: row.businessType, titlePrompt: row.titlePrompt, status: row.status }); dialogTitle.value = '编辑模板'; dialogVisible.value = true }
const handleDelete = async (row) => { try { await ElMessageBox.confirm('确定删除?', '提示', { type: 'warning' }); await api.delete(`/title-templates/${row.id}`); ElMessage.success('删除成功'); loadData() } catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') } }
const handleSetDefault = async (row) => { try { await api.put(`/title-templates/${row.id}/default`); ElMessage.success('设置成功'); loadData() } catch (error) { ElMessage.error('设置失败') } }
const handleSubmit = async () => { 
  if (!formRef.value) return; 
  await formRef.value.validate(async (valid) => { 
    if (valid) { 
      try { 
        const data = { name: form.name, productIds: form.productIds, businessType: form.businessType, titlePrompt: form.titlePrompt, status: form.status }
        form.id ? await api.put(`/title-templates/${form.id}`, data) : await api.post('/title-templates', data); 
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

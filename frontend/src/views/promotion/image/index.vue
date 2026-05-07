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
        <el-table-column prop="url" label="图片" width="140">
          <template #default="{ row }">
            <div class="image-wrapper">
              <el-image :src="row.url" style="width: 80px; height: 60px" fit="cover" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="positionType" label="插入位置" width="100">
          <template #default="{ row }">
            <span>{{ getPositionTypeLabel(row.positionType) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="products" label="关联产品" width="150">
          <template #default="{ row }">
            <span v-if="row.products && row.products.length > 0">{{ row.products.map(p => p.name).join(', ') }}</span>
            <span v-else style="color: #909399">未关联</span>
          </template>
        </el-table-column>
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

    <!-- 编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="图片" prop="url">
          <div class="upload-section">
            <el-input v-model="form.url" placeholder="请输入图片URL或点击上传" style="width: 300px" />
            <el-upload action="/api/images/upload" :show-file-list="false" :on-success="handleUploadSuccess" :on-error="handleUploadError" :headers="{ Authorization: 'Bearer ' + token }" name="file">
              <el-button type="primary" style="margin-left: 10px">本地上传</el-button>
            </el-upload>
          </div>
          <div v-if="form.url" class="image-preview">
            <img :src="form.url" />
          </div>
        </el-form-item>
        <el-form-item label="插入位置" prop="positionType">
          <el-select v-model="form.positionType" style="width: 100%">
            <el-option label="自动" value="auto" />
            <el-option label="开头之前" value="before_first" />
            <el-option label="结尾之后" value="after_last" />
            <el-option label="指定段落" value="custom" />
          </el-select>
        </el-form-item>
        <template v-if="form.positionType === 'custom'">
          <el-form-item label="段落号">
            <el-input-number v-model="form.positionValue" :min="1" style="width: 100px" />
          </el-form-item>
          <el-form-item label="插入方式">
            <el-select v-model="form.positionMode" style="width: 100%">
              <el-option label="段前" value="before" />
              <el-option label="段后" value="after" />
            </el-select>
          </el-form-item>
        </template>
        <el-form-item label="关联产品" prop="productIds">
          <el-select v-model="form.productIds" multiple style="width: 100%" placeholder="请选择关联产品">
            <el-option v-for="product in productList" :key="product.id" :label="product.name" :value="product.id" />
          </el-select>
          <span v-if="productList.length === 0" style="color: #909399; font-size: 12px;">暂无产品，请先在产品管理中添加</span>
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
import { useUserStore } from '@/stores/user'

const loading = ref(false)
const tableData = ref([])
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()
const productList = ref([])
const userStore = useUserStore()
const token = userStore.token
const form = reactive({ id: null, url: '', positionType: 'auto', positionValue: 1, positionMode: 'before', productIds: [], status: 1 })
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

const loadProducts = async () => {
  try {
    const res = await api.get('/products', { params: { pageSize: 100 } })
    productList.value = res.data.list || []
  } catch (error) { ElMessage.error('加载产品列表失败') }
}

const handleAdd = () => { 
  Object.assign(form, { id: null, url: '', positionType: 'auto', positionValue: 1, positionMode: 'before', productIds: [], status: 1 })
  dialogTitle.value = '新增图片'
  dialogVisible.value = true 
}

const handleEdit = (row) => { 
  const productIds = row.products ? row.products.map(p => p.id) : []
  Object.assign(form, { id: row.id, url: row.url, positionType: row.positionType, positionValue: row.positionValue, positionMode: row.positionMode || 'before', productIds: productIds, status: row.status })
  dialogTitle.value = '编辑图片'
  dialogVisible.value = true 
}

const handleDelete = async (row) => {
  try { 
    await ElMessageBox.confirm('确定删除?', '提示', { type: 'warning' })
    await api.delete(`/images/${row.id}`)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) { 
    if (error !== 'cancel') ElMessage.error('删除失败') 
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try { 
        form.id ? await api.put(`/images/${form.id}`, form) : await api.post('/images', form)
        ElMessage.success('操作成功')
        dialogVisible.value = false
        loadData()
      } catch (error) { ElMessage.error(error.message || '操作失败') }
    }
  })
}

const handleUploadSuccess = (res) => {
  if (res.code === 200) {
    form.url = res.data.url
    ElMessage.success('上传成功')
  } else {
    ElMessage.error(res.msg || '上传失败')
  }
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

const getPositionTypeLabel = (type) => {
  const map = {
    'auto': '自动',
    'before_first': '开头',
    'after_last': '结尾',
    'custom': '段落'
  }
  return map[type] || type
}

onMounted(() => { 
  loadData() 
  loadProducts() 
})
</script>

<style scoped>
.page-container { padding: 20px }
.card-header { display: flex; justify-content: space-between; align-items: center }

.upload-section {
  display: flex;
  align-items: center;
}

.image-preview {
  margin-top: 10px;
  max-width: 300px;
}

.image-preview img {
  max-width: 100%;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.image-wrapper {
  position: relative;
  display: inline-block;
}
</style>
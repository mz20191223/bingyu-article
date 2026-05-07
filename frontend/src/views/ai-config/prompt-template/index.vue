<template>
  <div class="app-container">
    <div class="search-bar">
      <el-input v-model="searchForm.name" placeholder="模板名称" clearable class="search-input" @keyup.enter="handleSearch" />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button type="success" @click="handleAdd">新增模板</el-button>
    </div>

    <el-table :data="tableData" border :loading="loading">
      <el-table-column label="模板名称" prop="name" />
      <el-table-column label="关联产品">
        <template #default="{ row }">
          <span v-if="row.product_names && row.product_names.length > 0">{{ row.product_names.join(', ') }}</span>
          <span v-else class="text-gray">无</span>
        </template>
      </el-table-column>
      <el-table-column label="状态">
        <template #default="{ row }">
          <el-tag :type="row.status === 0 ? 'success' : 'danger'">
            {{ row.status === 0 ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="默认">
        <template #default="{ row }">
          <el-tag v-if="row.is_default === 1" type="primary">默认</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" prop="create_time" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button link @click="handleEdit(row)">编辑</el-button>
            <el-button link @click="handleSetDefault(row)" v-if="row.is_default !== 1">设为默认</el-button>
            <el-button link @click="handleDelete(row)" v-if="row.status === 0">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      :current-page="pagination.page"
      :page-size="pagination.size"
      :total="pagination.total"
      @current-change="handlePageChange"
      layout="total, prev, pager, next, jumper"
    />

    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="模板名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入模板名称" />
        </el-form-item>
        <el-form-item label="关联产品" prop="product_ids">
          <el-select v-model="form.product_ids" multiple placeholder="请选择产品（可选）">
            <el-option v-for="product in productOptions" :key="product.value" :label="product.label" :value="product.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="提示词内容" prop="prompt_content">
          <el-input v-model="form.prompt_content" type="textarea" :rows="8" placeholder="请输入提示词内容，使用{keywords}作为关键词占位符" />
        </el-form-item>
        <el-form-item label="设为默认">
          <el-switch v-model="form.is_default" />
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
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const loading = ref(false)
const tableData = ref([])
const searchForm = reactive({ name: '' })
const pagination = reactive({ page: 1, size: 10, total: 0 })
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const productOptions = ref([])

const form = reactive({
  id: null,
  name: '',
  business_type: '',
  required_paragraphs: 5,
  product_ids: [],
  prompt_content: '',
  conclusion_text: '',
  is_default: 0
})

const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchData()
}

const fetchData = async () => {
  loading.value = true
  try {
    const result = await request.get('/prompt-templates', {
      params: {
        page: pagination.page,
        size: pagination.size,
        name: searchForm.name
      }
    })
    if (result.code === 200) {
      tableData.value = result.data.list
      pagination.total = result.data.total
    }
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

const fetchProducts = async () => {
  try {
    const result = await request.get('/products')
    if (result.code === 200) {
      productOptions.value = result.data.list.map(p => ({ value: p.id, label: p.name }))
    }
  } catch (error) {
    console.error('获取产品失败:', error)
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增提示词模板'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑提示词模板'
  isEdit.value = true
  form.id = row.id
  form.name = row.name
  form.business_type = row.business_type
  form.required_paragraphs = row.required_paragraphs
  form.product_ids = row.product_ids || []
  form.prompt_content = row.prompt_content
  form.conclusion_text = row.conclusion_text
  form.is_default = row.is_default
  dialogVisible.value = true
}

const handleSetDefault = async (row) => {
  try {
    const result = await request.put(`/prompt-templates/default/${row.id}`)
    if (result.code === 200) {
      ElMessage.success('设置默认成功')
      fetchData()
    }
  } catch (error) {
    console.error('设置默认失败:', error)
    ElMessage.error('设置默认失败')
  }
}

const handleDelete = async (row) => {
  try {
    const result = await request.delete(`/prompt-templates/${row.id}`)
    if (result.code === 200) {
      ElMessage.success('删除成功')
      fetchData()
    }
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}

const resetForm = () => {
  form.id = null
  form.name = ''
  form.business_type = ''
  form.required_paragraphs = 5
  form.product_ids = []
  form.prompt_content = ''
  form.conclusion_text = ''
  form.is_default = 0
}

const handleSubmit = async () => {
  if (!form.name) {
    ElMessage.warning('请输入模板名称')
    return
  }
  if (!form.prompt_content) {
    ElMessage.warning('请输入提示词内容')
    return
  }

  try {
    const result = isEdit.value 
      ? await request.put(`/prompt-templates/${form.id}`, form)
      : await request.post('/prompt-templates', form)
    
    if (result.code === 200) {
      ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
      dialogVisible.value = false
      fetchData()
    }
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  }
}

onMounted(() => {
  fetchData()
  fetchProducts()
})
</script>

<style scoped>
.app-container {
  padding: 20px;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  width: 200px;
}

.text-gray {
  color: #999;
}
</style>
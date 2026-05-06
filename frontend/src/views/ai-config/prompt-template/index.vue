<template>
  <div class="prompt-template">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>提示词模板管理</span>
          <el-button type="primary" @click="openDialog()">新增模板</el-button>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="模板名称" />
        <el-table-column prop="productNames" label="关联产品" width="200">
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
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'info'">{{ row.status === 0 ? '启用' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
            <el-button link type="warning" v-if="row.isDefault !== 1" @click="setDefault(row.id)">设为默认</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="fetchData"
        @size-change="fetchData"
        style="margin-top: 20px"
      />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑模板' : '新增模板'" width="800px" destroy-on-close>
      <el-form :model="form" label-width="100px">
        <el-form-item label="模板名称" required>
          <el-input v-model="form.name" placeholder="请输入模板名称" />
        </el-form-item>
        <el-form-item label="关联产品">
          <el-select v-model="form.productIds" placeholder="请选择产品（支持多选）" style="width: 100%" multiple clearable>
            <el-option v-for="p in products" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="业务类型">
          <el-input v-model="form.businessType" placeholder="请输入业务类型" />
        </el-form-item>
        <el-form-item label="提示词内容" required>
          <el-input v-model="form.promptContent" type="textarea" :rows="12" placeholder="请输入完整的提示词内容，支持变量：{keyword}、{keywords}" />
        </el-form-item>
        <el-form-item label="段落数量">
          <el-input-number v-model="form.requiredParagraphs" :min="1" :max="20" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio :label="0">启用</el-radio>
            <el-radio :label="1">禁用</el-radio>
          </el-radio-group>
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
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

const tableData = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const products = ref([])
const dialogVisible = ref(false)

const form = reactive({
  id: null,
  name: '',
  productIds: [],
  businessType: '',
  promptContent: '',
  requiredParagraphs: 5,
  status: 1
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await request.get('/prompt-templates', { params: { page: page.value, pageSize: pageSize.value } })
    if (res.code === 200) {
      tableData.value = res.data.list || []
      total.value = res.data.total || 0
    }
  } catch (e) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const fetchProducts = async () => {
  try {
    const res = await request.get('/products/all')
    if (res.code === 200) {
      products.value = res.data || []
    }
  } catch (e) {
    console.error(e)
  }
}

const openDialog = (row) => {
  if (row) {
    Object.assign(form, {
      id: row.id,
      name: row.name,
      productIds: row.productIds || [],
      businessType: row.businessType,
      promptContent: row.promptContent,
      requiredParagraphs: row.requiredParagraphs || 5,
      status: row.status
    })
  } else {
    Object.assign(form, {
      id: null,
      name: '',
      productIds: [],
      businessType: '',
      promptContent: '',
      requiredParagraphs: 5,
      status: 1
    })
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.name || !form.promptContent) {
    ElMessage.warning('请填写必填项')
    return
  }
  try {
    const res = form.id
      ? await request.put(`/prompt-templates/${form.id}`, form)
      : await request.post('/prompt-templates', form)
    if (res.code === 200) {
      ElMessage.success(form.id ? '更新成功' : '创建成功')
      dialogVisible.value = false
      fetchData()
    }
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确认删除该模板?', '警告', { type: 'warning' })
    .then(async () => {
      try {
        const res = await request.delete(`/prompt-templates/${id}`)
        if (res.code === 200) {
          ElMessage.success('删除成功')
          fetchData()
        }
      } catch (e) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {})
}

const setDefault = async (id) => {
  try {
    const res = await request.put(`/prompt-templates/${id}/default`)
    if (res.code === 200) {
      ElMessage.success('设置成功')
      fetchData()
    }
  } catch (e) {
    ElMessage.error('设置失败')
  }
}

onMounted(() => {
  fetchData()
  fetchProducts()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.text-gray {
  color: #999;
}
</style>

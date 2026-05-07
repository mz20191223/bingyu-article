<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>草稿管理</span>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="草稿名称" show-overflow-tooltip />
        <el-table-column prop="draftCount" label="草稿条数" width="100" align="center">
          <template #default="{ row }">
            <el-tag type="info">{{ row.draftCount || 0 }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column prop="updateTime" label="更新时间" width="180" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="info" link @click="handleView(row)">查看</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        style="margin-top: 20px; justify-content: flex-end"
        @change="loadData"
      />
    </el-card>

    <el-dialog v-model="viewDialogVisible" title="草稿详情" width="800px">
      <div v-if="currentDraft" class="draft-detail">
        <p><strong>草稿名称：</strong>{{ currentDraft.name }}</p>
        <p><strong>包含条数：</strong>{{ currentDraft.draftCount || 0 }}</p>
        <el-divider />
        <div v-if="draftItems.length > 0">
          <div v-for="(item, index) in draftItems" :key="index" class="draft-item">
            <h4>条目 {{ index + 1 }}</h4>
            <p><strong>标题：</strong>{{ item.title || '无' }}</p>
            <p><strong>内容：</strong>{{ item.content ? item.content.substring(0, 100) + '...' : '无' }}</p>
            <el-divider v-if="index < draftItems.length - 1" />
          </div>
        </div>
        <div v-else>
          <pre>{{ currentDraft.data }}</pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const tableData = ref([])
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })

const viewDialogVisible = ref(false)
const currentDraft = ref(null)
const draftItems = ref([])

const loadData = async () => {
  loading.value = true
  try {
    const res = await api.get('/drafts', {
      params: { page: pagination.page, pageSize: pagination.pageSize }
    })
    const list = res.data.list || []
    list.forEach(item => {
      try {
        const dataObj = JSON.parse(item.data)
        if (Array.isArray(dataObj)) {
          item.draftCount = dataObj.length
        } else if (dataObj.items && Array.isArray(dataObj.items)) {
          item.draftCount = dataObj.items.length
        } else {
          item.draftCount = 1
        }
      } catch {
        item.draftCount = 1
      }
    })
    tableData.value = list
    pagination.total = res.data.total || 0
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleEdit = (row) => {
  router.push({ path: '/article/publish', query: { draftId: row.id } })
}

const handleView = (row) => {
  currentDraft.value = row
  try {
    const dataObj = JSON.parse(row.data)
    if (Array.isArray(dataObj)) {
      draftItems.value = dataObj
    } else if (dataObj.items && Array.isArray(dataObj.items)) {
      draftItems.value = dataObj.items
    } else {
      draftItems.value = [dataObj]
    }
  } catch {
    draftItems.value = []
  }
  viewDialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该草稿吗？', '提示', { type: 'warning' })
    await api.delete(`/drafts/${row.id}`)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.draft-detail p {
  margin: 8px 0;
}
.draft-item {
  padding: 10px 0;
}
</style>
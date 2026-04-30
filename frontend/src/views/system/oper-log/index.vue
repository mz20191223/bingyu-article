<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <span>操作日志</span>
      </template>
      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="operId" label="ID" width="80" />
        <el-table-column prop="title" label="操作模块" />
        <el-table-column prop="operName" label="操作人" width="120" />
        <el-table-column prop="operUrl" label="请求地址" show-overflow-tooltip />
        <el-table-column prop="operIp" label="操作IP" width="120" />
        <el-table-column prop="operTime" label="操作时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'danger'">{{ row.status === 0 ? '正常' : '异常' }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" layout="total, prev, pager, next" style="margin-top: 20px; justify-content: flex-end" @change="loadData" />
    </el-card>
  </div>
</template>
<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/api'
import { ElMessage } from 'element-plus'
const loading = ref(false), tableData = ref([]), pagination = reactive({ page: 1, pageSize: 10, total: 0 })
const loadData = async () => { loading.value = true; try { const res = await api.get('/logs/oper', { params: { page: pagination.page, pageSize: pagination.pageSize } }); tableData.value = res.data.list; pagination.total = res.data.total } catch (error) { ElMessage.error('加载失败') } finally { loading.value = false } }
onMounted(() => { loadData() })
</script>
<style scoped>.page-container { padding: 20px }</style>

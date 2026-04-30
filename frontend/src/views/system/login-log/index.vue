<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <span>登录日志</span>
      </template>
      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="infoId" label="ID" width="80" />
        <el-table-column prop="userName" label="登录账号" />
        <el-table-column prop="ipaddr" label="IP地址" width="140" />
        <el-table-column prop="loginLocation" label="登录地点" />
        <el-table-column prop="browser" label="浏览器" width="100" />
        <el-table-column prop="os" label="操作系统" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === '0' ? 'success' : 'danger'">{{ row.status === '0' ? '成功' : '失败' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="msg" label="提示消息" />
        <el-table-column prop="loginTime" label="登录时间" width="180" />
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
const loadData = async () => { loading.value = true; try { const res = await api.get('/logs/login', { params: { page: pagination.page, pageSize: pagination.pageSize } }); tableData.value = res.data.list; pagination.total = res.data.total } catch (error) { ElMessage.error('加载失败') } finally { loading.value = false } }
onMounted(() => { loadData() })
</script>
<style scoped>.page-container { padding: 20px }</style>

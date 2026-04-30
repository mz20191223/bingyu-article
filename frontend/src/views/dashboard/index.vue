<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #409EFF">
            <el-icon><Goods /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.productCount }}</div>
            <div class="stat-label">产品数量</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #67C23A">
            <el-icon><Picture /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.imageCount }}</div>
            <div class="stat-label">图片数量</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #E6A23C">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.keywordCount }}</div>
            <div class="stat-label">关键词数量</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #F56C6C">
            <el-icon><Upload /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.publishCount }}</div>
            <div class="stat-label">发布记录</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card class="quick-actions">
          <template #header>
            <span>快捷操作</span>
          </template>
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="action-item" @click="$router.push('/publish/article')">
                <el-icon size="32"><Upload /></el-icon>
                <span>发布文章</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="action-item" @click="$router.push('/business/product')">
                <el-icon size="32"><Goods /></el-icon>
                <span>管理产品</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="action-item" @click="$router.push('/publish/record')">
                <el-icon size="32"><List /></el-icon>
                <span>查看记录</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="action-item" @click="$router.push('/publish/website')">
                <el-icon size="32"><Link /></el-icon>
                <span>网站配置</span>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const stats = ref({
  productCount: 0,
  imageCount: 0,
  keywordCount: 0,
  publishCount: 0
})

const loadStats = async () => {
  try {
    const [productRes, imageRes, keywordRes, recordRes] = await Promise.all([
      api.get('/products', { params: { pageSize: 1 } }),
      api.get('/images', { params: { pageSize: 1 } }),
      api.get('/keywords', { params: { pageSize: 1 } }),
      api.get('/records', { params: { pageSize: 1 } })
    ])
    stats.value = {
      productCount: productRes.data.total || 0,
      imageCount: imageRes.data.total || 0,
      keywordCount: keywordRes.data.total || 0,
      publishCount: recordRes.data.total || 0
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
  margin-right: 20px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.quick-actions {
  margin-top: 20px;
}

.action-item {
  text-align: center;
  padding: 30px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
}

.action-item:hover {
  background: #f5f7fa;
}

.action-item .el-icon {
  color: #409EFF;
  margin-bottom: 10px;
}

.action-item span {
  display: block;
  color: #606266;
  font-size: 14px;
}
</style>

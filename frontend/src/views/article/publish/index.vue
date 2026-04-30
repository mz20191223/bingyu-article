<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>文章发布</span>
        </div>
      </template>

      <el-steps :active="currentStep" finish-status="success" style="margin-bottom: 30px">
        <el-step title="选择配置" />
        <el-step title="生成内容" />
        <el-step title="发布文章" />
      </el-steps>

      <div v-show="currentStep === 0">
        <el-form label-width="120px">
          <el-form-item label="选择产品">
            <el-select v-model="form.productId" placeholder="请选择产品" style="width: 400px">
              <el-option v-for="p in products" :key="p.id" :label="p.name" :value="p.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="目标网站">
            <el-checkbox-group v-model="form.websiteIds">
              <el-checkbox v-for="w in websites" :key="w.id" :label="w.id">{{ w.name }}</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="内容模板">
            <el-select v-model="form.contentTemplateId" placeholder="请选择内容模板" style="width: 400px">
              <el-option v-for="t in contentTemplates" :key="t.id" :label="t.name" :value="t.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="标题模板">
            <el-select v-model="form.titleTemplateId" placeholder="请选择标题模板" style="width: 400px">
              <el-option v-for="t in titleTemplates" :key="t.id" :label="t.name" :value="t.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="AI模型">
            <el-select v-model="form.modelId" placeholder="请选择AI模型" style="width: 400px">
              <el-option v-for="m in models" :key="m.id" :label="m.name" :value="m.id" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="nextStep" :disabled="!canNext">下一步（使用AI生成）</el-button>
            <el-button @click="goToManualInput">直接录入（手动编写）</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-show="currentStep === 1">
        <el-form label-width="120px">
          <el-form-item label="文章标题">
            <el-input v-model="article.title" type="textarea" :rows="2" style="width: 600px" placeholder="请输入文章标题（可手动输入或点击AI生成）" />
          </el-form-item>
          <el-form-item label="文章内容">
            <el-input v-model="article.content" type="textarea" :rows="15" style="width: 600px" placeholder="请输入文章内容（可手动输入或点击AI生成）" />
          </el-form-item>
          <el-form-item>
            <el-button @click="currentStep = 0">上一步</el-button>
            <el-button type="primary" @click="generateArticle" :loading="generating">AI生成</el-button>
            <el-button type="success" @click="goToPublish">发布文章</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-show="currentStep === 2">
        <el-result icon="success" title="发布成功" sub-title="文章已成功发布到目标平台">
          <template #extra>
            <el-button type="primary" @click="currentStep = 0">继续发布</el-button>
            <el-button @click="$router.push('/publish/record')">查看记录</el-button>
          </template>
        </el-result>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

const currentStep = ref(0)
const generating = ref(false)

const form = reactive({
  productId: null,
  websiteIds: [],
  contentTemplateId: null,
  titleTemplateId: null,
  modelId: null
})

const article = reactive({
  title: '',
  content: ''
})

const products = ref([])
const websites = ref([])
const contentTemplates = ref([])
const titleTemplates = ref([])
const models = ref([])

const canNext = computed(() => {
  return form.productId && form.websiteIds.length > 0
})

const loadData = async () => {
  try {
    const [pRes, wRes, cRes, tRes, mRes] = await Promise.all([
      api.get('/products', { params: { pageSize: 100, status: 0 } }),
      api.get('/websites', { params: { pageSize: 100, status: 0 } }),
      api.get('/content-templates', { params: { pageSize: 100, status: 0 } }),
      api.get('/title-templates', { params: { pageSize: 100, status: 0 } }),
      api.get('/models', { params: { pageSize: 100, status: 0 } })
    ])
    products.value = pRes.data.list || []
    websites.value = wRes.data.list || []
    contentTemplates.value = cRes.data.list || []
    titleTemplates.value = tRes.data.list || []
    models.value = mRes.data.list || []
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

const nextStep = () => {
  currentStep.value = 1
}

const goToManualInput = () => {
  currentStep.value = 1
  ElMessage.info('请在下方输入文章标题和内容')
}

const generateArticle = async () => {
  generating.value = true
  try {
    const res = await api.post('/publish/generate', {
      productId: form.productId,
      websiteIds: form.websiteIds,
      contentTemplateId: form.contentTemplateId,
      titleTemplateId: form.titleTemplateId,
      modelId: form.modelId
    })
    article.title = res.data.title
    article.content = res.data.content
    ElMessage.success('生成成功')
  } catch (error) {
    ElMessage.error(error.message || '生成失败')
  } finally {
    generating.value = false
  }
}

const goToPublish = async () => {
  if (!article.title || !article.content) {
    ElMessage.warning('请输入文章标题和内容（可手动输入或点击AI生成）')
    return
  }
  try {
    await api.post('/publish/submit', {
      productId: form.productId,
      websiteIds: form.websiteIds,
      title: article.title,
      content: article.content,
      modelId: form.modelId,
      titleTemplateId: form.titleTemplateId,
      contentTemplateId: form.contentTemplateId
    })
    currentStep.value = 2
    ElMessage.success('发布成功')
  } catch (error) {
    ElMessage.error(error.message || '发布失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.card-header {
  font-weight: 600;
  font-size: 16px;
}
</style>

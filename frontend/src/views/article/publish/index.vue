<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>文章发布</span>
          <el-button type="success" @click="showImportDialog = true">导入Excel</el-button>
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

    <el-dialog v-model="showImportDialog" title="导入Excel" width="900px">
      <div style="margin-bottom: 20px">
        <el-link type="primary" :href="'/api/templates/download'" target="_blank">下载模板文件</el-link>
      </div>
      <el-upload
        ref="uploadRef"
        class="upload-demo"
        drag
        :auto-upload="false"
        :limit="1"
        accept=".xlsx"
        :on-change="handleFileChange"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">拖拽文件到此处 或 <em>点击选择文件</em></div>
        <template #tip>
          <div class="el-upload__tip">只能上传xlsx文件，建议不超过10MB</div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="showImportDialog = false">取消</el-button>
        <el-button type="primary" @click="importExcel" :loading="importing">确认导入</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showPreviewDialog" title="导入预览" width="1000px">
      <el-table :data="importList" border style="width: 100%">
        <el-table-column prop="productName" label="产品" width="100" />
        <el-table-column prop="title" label="标题" width="180" show-overflow-tooltip />
        <el-table-column prop="websites" label="目标网站" width="200" />
        <el-table-column prop="paragraphs" label="段落数" width="80" align="center" />
        <el-table-column prop="status" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.error" type="danger">错误</el-tag>
            <el-tag v-else type="success">正常</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="error" label="错误信息" show-overflow-tooltip />
      </el-table>
      <div style="margin-top: 20px; text-align: right;">
        <el-tag style="margin-right: 20px">共 {{ importList.length }} 篇，错误 {{ errorCount }} 篇</el-tag>
        <el-button @click="showPreviewDialog = false">取消</el-button>
        <el-button type="primary" @click="startBatchPublish" :loading="publishing">确认发布</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import api from '@/api'
import { ElMessage } from 'element-plus'
import * as XLSX from 'xlsx'

const currentStep = ref(0)
const generating = ref(false)
const importing = ref(false)
const publishing = ref(false)
const showImportDialog = ref(false)
const showPreviewDialog = ref(false)
const uploadRef = ref(null)
const selectedFile = ref(null)
const importList = ref([])

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

const errorCount = computed(() => importList.value.filter(i => i.error).length)

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

const handleFileChange = (file) => {
  selectedFile.value = file.raw
}

const importExcel = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请选择文件')
    return
  }

  importing.value = true
  try {
    const data = await selectedFile.value.arrayBuffer()
    const workbook = XLSX.read(data)
    const sheetName = workbook.SheetNames[0]
    const worksheet = workbook.Sheets[sheetName]
    const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 })

    if (jsonData.length < 2) {
      ElMessage.error('Excel文件内容为空')
      return
    }

    const headers = jsonData[0]
    const websiteIndexMap = {}
    headers.forEach((h, i) => {
      if (i >= 3 && h) {
        websiteIndexMap[h] = i
      }
    })

    const productMap = {}
    products.value.forEach(p => productMap[p.name] = p.id)

    const websiteMap = {}
    websites.value.forEach(w => websiteMap[w.name] = w.id)

    const rows = []
    for (let i = 1; i < jsonData.length; i++) {
      const row = jsonData[i]
      if (!row || row.length === 0 || !row[0]) continue

      const productName = row[0]
      const title = row[1]
      const content = row[2]

      if (!productName || !title || !content) {
        rows.push({ productName, title, content, error: '产品、标题、内容不能为空' })
        continue
      }

      const productId = productMap[productName]
      if (!productId) {
        rows.push({ productName, title, content, error: `产品"${productName}"不存在` })
        continue
      }

      const selectedWebsites = []
      for (const [siteName, idx] of Object.entries(websiteIndexMap)) {
        const val = row[idx]
        if (val === '是') {
          const siteId = websiteMap[siteName]
          if (siteId) {
            selectedWebsites.push({ id: siteId, name: siteName })
          }
        }
      }

      if (selectedWebsites.length === 0) {
        rows.push({ productName, title, content, error: '未选择任何目标网站' })
        continue
      }

      const paragraphs = content.split('\n\n').filter(p => p.trim())
      rows.push({
        productId,
        productName,
        title,
        content,
        websites: selectedWebsites,
        paragraphs: paragraphs.length
      })
    }

    importList.value = rows
    showImportDialog.value = false
    showPreviewDialog.value = true
    uploadRef.value?.clearFiles()
  } catch (error) {
    console.error('Import error:', error)
    ElMessage.error('导入失败: ' + error.message)
  } finally {
    importing.value = false
  }
}

const startBatchPublish = async () => {
  const validList = importList.value.filter(i => !i.error)
  if (validList.length === 0) {
    ElMessage.warning('没有可发布的文章')
    return
  }

  publishing.value = true
  let successCount = 0
  let failCount = 0

  for (const item of validList) {
    try {
      for (const website of item.websites) {
        await api.post('/publish/submit', {
          productId: item.productId,
          websiteIds: [website.id],
          title: item.title,
          content: item.content,
          modelId: form.modelId,
          titleTemplateId: form.titleTemplateId,
          contentTemplateId: form.contentTemplateId
        })
        successCount++
      }
    } catch (error) {
      failCount++
      console.error(`发布失败 [${item.title}]:`, error)
    }
  }

  publishing.value = false
  showPreviewDialog.value = false
  ElMessage.success(`发布完成: 成功 ${successCount} 篇, 失败 ${failCount} 篇`)
  currentStep.value = 2
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

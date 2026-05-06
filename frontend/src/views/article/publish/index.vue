<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>文章发布</span>
          <el-radio-group v-model="mode" @change="handleModeChange" style="margin-right: 20px">
            <el-radio-button value="direct">直接录入</el-radio-button>
            <el-radio-button value="excel">导入Excel</el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <div v-show="mode === 'direct'">
        <el-table :data="tableData" border style="width: 100%" v-loading="tableLoading">
          <el-table-column label="产品" width="150">
            <template #default="{ row, $index }">
              <el-select v-model="row.productId" placeholder="请选择产品" @change="handleProductChange($index)">
                <el-option v-for="p in products" :key="p.id" :label="p.name" :value="p.id" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="目标网站" width="250">
            <template #default="{ row }">
              <el-select v-model="row.websiteIds" placeholder="请选择网站" multiple collapse-tags collapse-tags-limit="2">
                <el-option v-for="w in websites" :key="w.id" :label="w.name" :value="w.id" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="AI生成" width="100">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="handleGenerate(row)" :loading="row.generating" :disabled="!row.productId">
                AI生成
              </el-button>
            </template>
          </el-table-column>
          <el-table-column label="标题">
            <template #default="{ row }">
              <el-input v-model="row.title" placeholder="请输入标题（不超过100字符）" maxlength="100" show-word-limit />
            </template>
          </el-table-column>
          <el-table-column label="内容" width="250">
            <template #default="{ row }">
              <el-input v-model="row.content" type="textarea" :rows="1" placeholder="请输入或粘贴内容" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80" fixed="right">
            <template #default="{ $index }">
              <el-button type="danger" size="small" link @click="handleDeleteRow($index)">删除</el-button>
            </template>
          </el-table-column>
          <el-table-column label="发布进度" width="200" fixed="right">
            <template #default="{ row }">
              <div v-if="row.publishStatus" class="publish-status">
                <span v-if="row.publishStatus === 'pending'" class="status-pending">○ 待发布</span>
                <span v-else-if="row.publishStatus === 'publishing'" class="status-publishing">
                  <el-icon class="is-loading"><Loading /></el-icon> {{ row.publishMsg || '发布中...' }}
                </span>
                <span v-else-if="row.publishStatus === 'success'" class="status-success">✓ {{ row.publishMsg }}</span>
                <span v-else-if="row.publishStatus === 'failed'" class="status-failed">
                  <el-tooltip :content="row.errorMsg || '发布失败'" placement="top">
                    <span>✗ {{ row.publishMsg }}</span>
                  </el-tooltip>
                </span>
              </div>
              <span v-else class="status-pending">○ 待发布</span>
            </template>
          </el-table-column>
        </el-table>

        <div style="margin-top: 20px; display: flex; justify-content: space-between;">
          <el-button type="primary" @click="handleAddRow">+ 添加一行</el-button>
          <el-button type="success" size="large" @click="handlePublishAll" :loading="publishingAll">发布全部</el-button>
        </div>

        <div v-if="publishSummary" style="margin-top: 20px;">
          <el-alert :type="publishSummary.type" :title="publishSummary.title" :description="publishSummary.desc" show-icon :closable="false" />
        </div>
      </div>

      <div v-show="mode === 'excel'">
        <div style="margin-bottom: 20px">
          <el-link type="primary" :href="'/api/publish/templates/download'" target="_blank">下载模板文件</el-link>
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
        <div style="margin-top: 20px">
          <el-button @click="mode = 'direct'">取消</el-button>
          <el-button type="primary" @click="handleImportExcel" :loading="importing">确认导入</el-button>
        </div>
      </div>
    </el-card>

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
import { UploadFilled, Loading } from '@element-plus/icons-vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as XLSX from 'xlsx'

const mode = ref('direct')
const tableData = ref([])
const tableLoading = ref(false)
const publishingAll = ref(false)
const publishSummary = ref(null)
const showPreviewDialog = ref(false)
const importing = ref(false)
const publishing = ref(false)
const uploadRef = ref(null)
const selectedFile = ref(null)
const importList = ref([])

const products = ref([])
const websites = ref([])

const errorCount = computed(() => importList.value.filter(i => i.error).length)

const loadData = async () => {
  try {
    const [pRes, wRes] = await Promise.all([
      api.get('/products', { params: { pageSize: 100, status: 0 } }),
      api.get('/websites', { params: { pageSize: 100, status: 0 } })
    ])
    products.value = pRes.data.list || []
    websites.value = wRes.data.list || []
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

const handleProductChange = (index) => {
  console.log('Product changed at index:', index)
}

const handleAddRow = () => {
  tableData.value.push({
    id: Date.now(),
    productId: null,
    websiteIds: [],
    title: '',
    content: '',
    generating: false,
    publishStatus: 'pending',
    publishMsg: '',
    errorMsg: ''
  })
}

const handleDeleteRow = (index) => {
  tableData.value.splice(index, 1)
}

const handleGenerate = async (row) => {
  if (!row.productId) {
    ElMessage.warning('请先选择产品')
    return
  }

  row.generating = true
  row.generatingMsg = '正在获取模板...'

  try {
    row.generatingMsg = '正在调用AI生成...'

    const res = await api.post('/publish/generate', {
      productId: row.productId,
      websiteIds: row.websiteIds.length > 0 ? row.websiteIds : []
    })

    if (res.code === 200 && res.data) {
      row.title = res.data.title || ''
      row.content = res.data.content || ''
      ElMessage.success('生成成功')
    } else {
      ElMessage.error(res.msg || '生成失败')
    }
  } catch (error) {
    console.error('Generate error:', error)
    ElMessage.error(error.message || '生成失败')
  } finally {
    row.generating = false
    row.generatingMsg = ''
  }
}

const validateRow = (row) => {
  if (!row.productId) {
    return '请选择产品'
  }
  if (!row.websiteIds || row.websiteIds.length === 0) {
    return '请选择目标网站'
  }
  if (!row.title) {
    return '请输入标题'
  }
  if (row.title.length > 100) {
    return '标题不超过100字符'
  }
  if (!row.content) {
    return '请输入内容'
  }
  return null
}

const handlePublishAll = async () => {
  const validRows = tableData.value.filter(row => row.productId && row.title && row.content)
  if (validRows.length === 0) {
    ElMessage.warning('没有可发布的文章')
    return
  }

  const errors = tableData.value.map((row, index) => {
    const error = validateRow(row)
    return error ? { index: index + 1, error } : null
  }).filter(e => e)

  if (errors.length > 0) {
    ElMessageBox.confirm(
      `有 ${errors.length} 行数据不完整，是否只发布有效的 ${validRows.length} 行？`,
      '提示',
      { type: 'warning' }
    ).then(() => {
      confirmPublish(validRows)
    }).catch(() => {})
  } else {
    confirmPublish(validRows)
  }
}

const confirmPublish = async (validRows) => {
  try {
    await ElMessageBox.confirm(
      `即将发布 ${validRows.length} 篇文章到目标网站，确认继续？`,
      '确认发布',
      { type: 'warning' }
    )
    doPublishAll(validRows)
  } catch {
  }
}

const doPublishAll = async (rows) => {
  publishingAll.value = true
  publishSummary.value = null

  let successCount = 0
  let failCount = 0

  for (const row of rows) {
    row.publishStatus = 'publishing'
    row.publishMsg = '准备发布...'

    try {
      for (let i = 0; i < row.websiteIds.length; i++) {
        const websiteId = row.websiteIds[i]
        const website = websites.value.find(w => w.id === websiteId)
        row.publishMsg = `正在发布到${website?.name || '网站'}...`

        const res = await api.post('/publish/submit', {
          productId: row.productId,
          websiteIds: [websiteId],
          title: row.title,
          content: row.content
        })

        if (res.code === 200) {
          row.publishMsg = `${website?.name || '网站'}发布成功`
          row.publishStatus = 'success'
          successCount++
        } else {
          row.publishStatus = 'failed'
          row.errorMsg = res.msg || '发布失败'
          row.publishMsg = `${website?.name || '网站'}失败`
          failCount++
        }
      }
    } catch (error) {
      row.publishStatus = 'failed'
      row.errorMsg = error.message || '发布失败'
      row.publishMsg = '发布失败'
      failCount++
    }

    await new Promise(resolve => setTimeout(resolve, 500))
  }

  publishingAll.value = false
  publishSummary.value = {
    type: failCount > 0 ? 'warning' : 'success',
    title: `发布完成：成功 ${successCount} 篇，失败 ${failCount} 篇`,
    desc: ''
  }
}

const handleModeChange = () => {
  if (mode.value === 'excel') {
    ElMessageBox.confirm('切换到导入模式将清空当前录入数据，是否继续？', '提示', {
      type: 'warning'
    }).then(() => {
      tableData.value = []
      publishSummary.value = null
    }).catch(() => {
      mode.value = 'direct'
    })
  }
}

const handleFileChange = (file) => {
  selectedFile.value = file.raw
}

const handleImportExcel = async () => {
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
    showPreviewDialog.value = false
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
          content: item.content
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
}

const initTable = () => {
  if (tableData.value.length === 0) {
    const defaultProduct = products.value.find(p => p.isDefault === 1) || products.value[0]
    const defaultWebsites = websites.value.filter(w => w.isDefault === 1)
    const selectedWebsites = defaultWebsites.length > 0 ? defaultWebsites.map(w => w.id) : (websites.value[0] ? [websites.value[0].id] : [])
    tableData.value.push({
      id: Date.now(),
      productId: defaultProduct?.id || null,
      websiteIds: selectedWebsites,
      title: '',
      content: '',
      generating: false,
      publishStatus: 'pending',
      publishMsg: '',
      errorMsg: ''
    })
  }
}

onMounted(async () => {
  await loadData()
  initTable()
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
.publish-status {
  font-size: 13px;
}
.status-pending {
  color: #909399;
}
.status-publishing {
  color: #409eff;
  display: flex;
  align-items: center;
  gap: 4px;
}
.status-success {
  color: #67c23a;
}
.status-failed {
  color: #f56c6c;
  cursor: pointer;
}
</style>
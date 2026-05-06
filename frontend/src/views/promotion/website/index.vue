<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>网站配置</span>
          <el-button type="primary" @click="handleAdd">新增网站</el-button>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="网站名称" />
        <el-table-column prop="code" label="网站标识" width="120" />
        <el-table-column prop="loginUrl" label="登录URL" show-overflow-tooltip />
        <el-table-column prop="publishUrl" label="发布URL" show-overflow-tooltip />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'info'">{{ row.status === 0 ? '启用' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="isDefault" label="发布默认" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.isDefault === 1" type="warning">默认</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" layout="total, prev, pager, next" style="margin-top: 20px; justify-content: flex-end" @change="loadData" />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="150px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="网站名称" prop="name"><el-input v-model="form.name" placeholder="请输入网站名称" /></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="网站标识" prop="code"><el-input v-model="form.code" placeholder="如: yomowoo, uuuhao, hxm18" /></el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="登录URL"><el-input v-model="form.loginUrl" placeholder="请输入登录URL" /></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="发布URL"><el-input v-model="form.publishUrl" placeholder="请输入发布URL" /></el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名"><el-input v-model="form.username" placeholder="请输入登录用户名" /></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="密码"><el-input v-model="form.password" type="password" placeholder="请输入登录密码" /></el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="Cookie"><el-input v-model="form.cookie" type="textarea" :rows="2" placeholder="请输入Cookie（可选）" /></el-form-item>

        <el-divider content-position="left">登录选择器配置</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名选择器"><el-input v-model="form.usernameSelector" placeholder="如: input[name=name]" /></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="密码选择器"><el-input v-model="form.passwordSelector" placeholder="如: input[name=password]" /></el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="登录按钮选择器"><el-input v-model="form.loginButtonSelector" placeholder="如: a[data-type=sign]" /></el-form-item>

        <el-divider content-position="left">发布选择器配置</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="标题选择器"><el-input v-model="form.titleSelector" placeholder="如: input[name=Title]" /></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="内容选择器"><el-input v-model="form.contentSelector" placeholder="如: #editor_Content" /></el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类选择器"><el-input v-model="form.categorySelector" placeholder="如: select[name=CateID]" /></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="发布按钮选择器"><el-input v-model="form.publishButtonSelector" placeholder="如: a[data-type=postedt]" /></el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="状态"><el-switch v-model="form.status" :active-value="0" :inactive-value="1" /></el-form-item>
        <el-form-item label="发布默认"><el-switch v-model="form.isDefault" :active-value="1" :inactive-value="0" /></el-form-item>
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

const loading = ref(false), tableData = ref([]), pagination = reactive({ page: 1, pageSize: 10, total: 0 }), dialogVisible = ref(false), dialogTitle = ref(''), formRef = ref()
const form = reactive({ 
  id: null, 
  name: '', 
  code: '', 
  loginUrl: '', 
  publishUrl: '', 
  username: '', 
  password: '', 
  cookie: '',
  usernameSelector: '',
  passwordSelector: '',
  loginButtonSelector: '',
  titleSelector: '',
  contentSelector: '',
  categorySelector: '',
  publishButtonSelector: '',
  status: 1,
  isDefault: 0 
})
const rules = { 
  name: [{ required: true, message: '请输入网站名称', trigger: 'blur' }], 
  code: [{ required: true, message: '请输入网站标识', trigger: 'blur' }] 
}

const loadData = async () => { loading.value = true; try { const res = await api.get('/websites', { params: { page: pagination.page, pageSize: pagination.pageSize } }); tableData.value = res.data.list; pagination.total = res.data.total } catch (error) { ElMessage.error('加载失败') } finally { loading.value = false } }
const handleAdd = () => { Object.assign(form, { id: null, name: '', code: '', loginUrl: '', publishUrl: '', username: '', password: '', cookie: '', usernameSelector: '', passwordSelector: '', loginButtonSelector: '', titleSelector: '', contentSelector: '', categorySelector: '', publishButtonSelector: '', status: 1, isDefault: 0 }); dialogTitle.value = '新增网站'; dialogVisible.value = true }
const handleEdit = async (row) => { try { const res = await api.get(`/websites/${row.id}`); if (res && res.data) { Object.assign(form, { id: res.data.id, name: res.data.name, code: res.data.code, loginUrl: res.data.loginUrl || '', publishUrl: res.data.publishUrl || '', username: res.data.username || '', password: res.data.password || '', cookie: res.data.cookie || '', usernameSelector: res.data.usernameSelector || '', passwordSelector: res.data.passwordSelector || '', loginButtonSelector: res.data.loginButtonSelector || '', titleSelector: res.data.titleSelector || '', contentSelector: res.data.contentSelector || '', categorySelector: res.data.categorySelector || '', publishButtonSelector: res.data.publishButtonSelector || '', status: res.data.status, isDefault: res.data.isDefault || 0 }); dialogTitle.value = '编辑网站'; dialogVisible.value = true } else { ElMessage.error('获取网站详情失败') } } catch (error) { ElMessage.error('获取网站详情失败') } }
const handleDelete = async (row) => { try { await ElMessageBox.confirm('确定删除?', '提示', { type: 'warning' }); await api.delete(`/websites/${row.id}`); ElMessage.success('删除成功'); loadData() } catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') } }
const handleSubmit = async () => { 
  if (!formRef.value) return; 
  await formRef.value.validate(async (valid) => { 
    if (valid) { 
      try { 
        const data = { 
          name: form.name, 
          code: form.code, 
          loginUrl: form.loginUrl, 
          publishUrl: form.publishUrl, 
          username: form.username, 
          password: form.password, 
          cookie: form.cookie,
          usernameSelector: form.usernameSelector,
          passwordSelector: form.passwordSelector,
          loginButtonSelector: form.loginButtonSelector,
          titleSelector: form.titleSelector,
          contentSelector: form.contentSelector,
          categorySelector: form.categorySelector,
          publishButtonSelector: form.publishButtonSelector,
          status: form.status,
          isDefault: form.isDefault
        }; 
        form.id ? await api.put(`/websites/${form.id}`, data) : await api.post('/websites', data); 
        ElMessage.success('操作成功'); 
        dialogVisible.value = false; 
        loadData() 
      } catch (error) { ElMessage.error(error.message || '操作失败') } 
    } 
  }) 
}
onMounted(() => { loadData() })
</script>

<style scoped>
.page-container { padding: 20px }
.card-header { display: flex; justify-content: space-between; align-items: center }
</style>

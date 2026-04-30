<template>
  <el-container class="main-layout">
    <el-aside width="200px" class="sidebar">
      <div class="logo">
        <span>冰鱼发布系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <template v-for="menu in parentMenus" :key="menu.path">
          <el-sub-menu :index="menu.path" v-if="hasChildren(menu.menuId)">
            <template #title>
              <el-icon><component :is="getIcon(menu.icon)" /></el-icon>
              <span>{{ menu.menuName }}</span>
            </template>
            <el-menu-item
              v-for="child in getChildren(menu.menuId)"
              :key="child.path"
              :index="child.path"
            >
              <span>{{ child.menuName }}</span>
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item :key="menu.path" :index="menu.path" v-else>
            <el-icon><component :is="getIcon(menu.icon)" /></el-icon>
            <span>{{ menu.menuName }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><User /></el-icon>
              <span>{{ userStore.userInfo.nickname || userStore.userInfo.username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { User, Monitor, Setting, Document, Goods, MagicStick } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const iconMap = {
  Monitor,
  Setting,
  Document,
  Goods,
  MagicStick
}

const getIcon = (iconName) => {
  return iconMap[iconName] || Document
}

const menus = computed(() => {
  return userStore.menus.filter(m => m.path)
})

const parentMenus = computed(() => {
  return menus.value.filter(m => m.menuType === 'M')
})

const hasChildren = (parentId) => {
  return menus.value.some(m => m.parentId === parentId)
}

const getChildren = (parentId) => {
  return menus.value.filter(m => m.parentId === parentId && m.menuType === 'C')
}

const handleCommand = (command) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.main-layout {
  height: 100%;
}

.sidebar {
  background-color: #304156;
}

.logo {
  height: 50px;
  line-height: 50px;
  text-align: center;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  background-color: #2b3a4a;
}

.sidebar-menu {
  border-right: none;
  height: calc(100% - 50px);
}

.header {
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 10px;
}

.user-info span {
  margin-left: 5px;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
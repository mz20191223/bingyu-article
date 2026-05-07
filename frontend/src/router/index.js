import { createRouter, createWebHashHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue')
  },
  {
    path: '/',
    component: () => import('@/layout/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue')
      },
      {
        path: 'system/user',
        name: 'User',
        component: () => import('@/views/system/user/index.vue')
      },
      {
        path: 'system/role',
        name: 'Role',
        component: () => import('@/views/system/role/index.vue')
      },
      {
        path: 'system/dept',
        name: 'Dept',
        component: () => import('@/views/system/dept/index.vue')
      },
      {
        path: 'system/login-log',
        name: 'LoginLog',
        component: () => import('@/views/system/login-log/index.vue')
      },
      {
        path: 'system/oper-log',
        name: 'OperLog',
        component: () => import('@/views/system/oper-log/index.vue')
      },
      {
        path: 'article/publish',
        name: 'Publish',
        component: () => import('@/views/article/publish/index.vue')
      },
      {
        path: 'article/record',
        name: 'Record',
        component: () => import('@/views/article/record/index.vue')
      },
      {
        path: 'article/draft',
        name: 'Draft',
        component: () => import('@/views/article/draft/index.vue')
      },
      {
        path: 'promotion/product',
        name: 'Product',
        component: () => import('@/views/promotion/product/index.vue')
      },
      {
        path: 'promotion/image',
        name: 'Image',
        component: () => import('@/views/promotion/image/index.vue')
      },
      {
        path: 'promotion/website',
        name: 'Website',
        component: () => import('@/views/promotion/website/index.vue')
      },
      {
        path: 'ai-config/keyword',
        name: 'Keyword',
        component: () => import('@/views/ai-config/keyword/index.vue')
      },
      {
        path: 'ai-config/model',
        name: 'Model',
        component: () => import('@/views/ai-config/model/index.vue')
      },
      {
        path: 'ai-config/prompt-template',
        name: 'PromptTemplate',
        component: () => import('@/views/ai-config/prompt-template/index.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const token = userStore.token

  try {
    if (to.path !== '/login' && !token) {
      next('/login')
    } else if (to.path === '/login' && token) {
      // 如果已登录但菜单数据为空，先获取菜单数据
      if (userStore.menus.length === 0) {
        await userStore.getUserInfo()
      }
      next('/')
    } else if (to.path !== '/login' && token && userStore.menus.length === 0) {
      // 已登录但菜单数据为空，先获取菜单数据
      await userStore.getUserInfo()
      next()
    } else {
      next()
    }
  } catch (error) {
    console.error('Router guard error:', error)
    if (to.path !== '/login') {
      next('/login')
    } else {
      next()
    }
  }
})

export default router
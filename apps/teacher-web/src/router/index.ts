import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true }
    },
    {
      path: '/',
      name: 'Layout',
      component: () => import('@/layouts/MainLayout.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: '/dashboard',
          name: 'Dashboard',
          component: () => import('@/views/DashboardView.vue'),
          meta: { title: '工作台' }
        },
        {
          path: '/questions',
          name: 'Questions',
          component: () => import('@/views/QuestionsView.vue'),
          meta: { title: '学生提问' }
        },
        {
          path: '/questions/:id',
          name: 'QuestionDetail',
          component: () => import('@/views/QuestionsView.vue'),
          meta: { title: '提问详情' }
        },
        {
          path: '/approval',
          name: 'Approval',
          component: () => import('@/views/ApprovalView.vue'),
          meta: { title: '空教室审批' }
        },
        {
          path: '/knowledge',
          name: 'Knowledge',
          component: () => import('@/views/KnowledgeView.vue'),
          meta: { title: '知识库管理' }
        },
        {
          path: '/analytics',
          name: 'Analytics',
          component: () => import('@/views/AnalyticsView.vue'),
          meta: { title: '数据看板' }
        },
        {
          path: '/profile',
          name: 'Profile',
          component: () => import('@/views/ProfileView.vue'),
          meta: { title: '个人中心' }
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFoundView.vue')
    }
  ]
})

// 路由守卫
router.beforeEach((to, from) => {
  const userStore = useUserStore()

  // [联调阶段] 已关闭开发模式自动模拟登录，确保走真实后端鉴权
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 学术智治系统`
  } else {
    document.title = '学术智治系统'
  }

  // 公开页面直接放行
  if (to.meta.public) {
    // 已登录用户访问登录页，重定向到首页
    if (userStore.isLoggedIn && to.path === '/login') {
      return '/dashboard'
    }
    return
  }

  // 需要登录的页面
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return '/login'
  }
})

export default router

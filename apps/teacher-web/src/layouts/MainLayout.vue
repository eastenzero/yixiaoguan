<template>
  <div class="layout-container">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <!-- Logo 区域 -->
      <div class="sidebar-header">
        <div class="logo-icon hover-scale">
          <el-icon :size="26" color="#FFFFFF"><School /></el-icon>
        </div>
        <div class="logo-text">
          <div class="logo-title font-display">学术智治系统</div>
          <div class="logo-subtitle">Faculty Intelligence</div>
        </div>
      </div>

      <!-- 菜单区域 -->
      <nav class="sidebar-menu">
        <div
          v-for="item in menuItems"
          :key="item.path"
          class="menu-item"
          :class="{ active: currentRoute === item.path }"
          @click="handleMenuClick(item)"
        >
          <div class="menu-icon-wrapper">
            <el-icon :size="20">
              <component :is="item.icon" />
            </el-icon>
          </div>
          <span class="menu-title">{{ item.title }}</span>
        </div>
      </nav>

      <!-- 新建任务按钮 -->
      <div class="sidebar-action">
        <el-button type="primary" class="new-task-btn" :icon="Plus">
          新建任务
        </el-button>
      </div>

      <!-- 底部操作区 -->
      <div class="sidebar-footer">
        <div class="menu-item" @click="handleMenuClick({ path: '/profile' })">
          <div class="menu-icon-wrapper">
            <el-icon :size="20"><User /></el-icon>
          </div>
          <span class="menu-title">个人中心</span>
        </div>
        <div class="menu-item logout" @click="handleLogout">
          <div class="menu-icon-wrapper">
            <el-icon :size="20"><SwitchButton /></el-icon>
          </div>
          <span class="menu-title">退出登录</span>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="main-wrapper">
      <!-- 顶部导航栏 -->
      <header class="header">
        <div class="header-left">
          <template v-if="showBack">
            <el-icon class="back-btn" :size="20" @click="router.back()">
              <ArrowLeft />
            </el-icon>
            <span class="page-title font-display">{{ pageTitle }}</span>
          </template>
          <template v-else>
            <div class="breadcrumb">
              <span class="breadcrumb-main font-display">学院智能助手</span>
              <el-divider direction="vertical" />
              <span class="breadcrumb-sub">{{ pageTitle }}</span>
            </div>
          </template>
        </div>
        
        <div class="header-center">
          <el-input
            v-model="searchQuery"
            placeholder="搜索学生、文件或申请..."
            :prefix-icon="Search"
            class="header-search"
            clearable
          />
        </div>
        
        <div class="header-right">
          <el-badge :value="wsStore.unreadCount" :hidden="!wsStore.hasUnread" class="header-icon" type="danger">
            <el-icon :size="20" @click="handleNotificationClick"><Bell /></el-icon>
          </el-badge>
          <el-icon class="header-icon" :size="20" @click="toggleWsTest" :class="{ active: wsStore.isConnected }">
            <component :is="wsStore.isConnected ? 'Connection' : 'Link'" />
          </el-icon>
          <el-icon class="header-icon" :size="20"><Setting /></el-icon>
          <div class="user-info">
            <el-avatar :size="36" :src="userStore.userInfo?.avatar" class="user-avatar">
              {{ userStore.userInfo?.nickName?.charAt(0) || '张' }}
            </el-avatar>
            <div class="user-meta">
              <span class="user-name">{{ userStore.userInfo?.nickName || '张教授' }}</span>
              <span class="user-dept">计算机学院</span>
            </div>
          </div>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox, ElMessage, ElNotification } from 'element-plus'
import {
  School,
  Grid,
  ChatDotRound,
  Checked,
  Collection,
  DataLine,
  User,
  SwitchButton,
  ArrowLeft,
  Bell,
  Setting,
  Search,
  Plus,
  Link,
  Cpu as Connection
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useWebsocketStore } from '@/stores/websocket'
import { logout as logoutApi } from '@/api/auth'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const wsStore = useWebsocketStore()

const searchQuery = ref('')

const currentRoute = computed(() => route.path)

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/dashboard': '工作台概览 / Dashboard',
    '/questions': '今日提问列表',
    '/approval': '空教室审批',
    '/knowledge': '知识库管理',
    '/analytics': '数据看板',
    '/profile': '个人中心'
  }
  return titles[route.path] || '审批详情'
})

const showBack = computed(() => {
  return route.path !== '/dashboard' && route.path !== '/questions' && 
         route.path !== '/approval' && route.path !== '/knowledge' && 
         route.path !== '/analytics'
})

const menuItems = [
  { path: '/dashboard', title: '工作台', icon: Grid },
  { path: '/questions', title: '学生提问', icon: ChatDotRound },
  { path: '/approval', title: '空教室审批', icon: Checked },
  { path: '/knowledge', title: '知识库管理', icon: Collection },
  { path: '/analytics', title: '数据看板', icon: DataLine }
]

const handleMenuClick = (item: { path: string }) => {
  router.push(item.path)
}

/**
 * 切换 WebSocket 测试连接
 */
const toggleWsTest = () => {
  if (wsStore.isConnected) {
    wsStore.disconnectAll()
    ElMessage.info('WebSocket 已断开')
  } else {
    // 使用会话 ID 1 进行测试
    wsStore.initTestConnection(1)
  }
}

/**
 * 点击通知图标
 */
const handleNotificationClick = () => {
  if (wsStore.notifications.length === 0) {
    ElMessage.info('暂无新通知')
    return
  }
  
  // 标记所有为已读
  wsStore.markAllAsRead()
  
  // 显示最新通知
  const latest = wsStore.notifications[0]
  if (latest) {
    ElNotification({
      title: latest.title,
      message: latest.content,
      type: latest.type
    })
  }
}

const handleLogout = () => {
  ElMessageBox.confirm(
    '确定要退出登录吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      // 断开所有 WebSocket
      wsStore.disconnectAll()
      await logoutApi()
    } finally {
      userStore.logout()
      router.push('/login')
      ElMessage.success('已退出登录')
    }
  })
}
</script>

<style scoped lang="scss">
.layout-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: var(--surface);
}

// ========================================
// 侧边栏
// ========================================
.sidebar {
  width: var(--sidebar-width);
  height: 100%;
  background-color: var(--sidebar-bg);
  border-right: 1px solid var(--sidebar-border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

// Logo 区域
.sidebar-header {
  height: 80px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #5B21B6 0%, #7C3AED 100%);
  flex-shrink: 0;

  .logo-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(4px);
    transition: transform var(--transition-normal);

    &:hover {
      transform: scale(1.05);
    }
  }

  .logo-text {
    color: #fff;
  }

  .logo-title {
    font-size: 16px;
    font-weight: 800;
    line-height: 1.4;
    letter-spacing: 0.5px;
  }

  .logo-subtitle {
    font-size: 10px;
    opacity: 0.8;
    line-height: 1.2;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
}

// 菜单区域
.sidebar-menu {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  margin-bottom: 4px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-normal);
  color: var(--text-secondary);
  position: relative;

  &:hover {
    background-color: var(--surface-low);
    color: var(--primary-color);
  }

  &.active {
    background-color: var(--primary-bg);
    color: var(--primary-color);
    font-weight: 700;
    border-right: 3px solid var(--primary-color);

    .menu-icon-wrapper {
      background-color: rgba(124, 58, 237, 0.1);
    }
  }

  &.logout {
    color: var(--error);

    &:hover {
      background-color: var(--error-container);
    }

    .menu-icon-wrapper {
      background-color: var(--error-container);
    }
  }

  .menu-icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 9px;
    background-color: transparent;
    transition: all var(--transition-fast);
  }

  .menu-title {
    font-size: 14px;
    font-weight: 500;
  }
}

// 新建任务按钮
.sidebar-action {
  padding: 16px 12px;
  border-top: 1px solid var(--sidebar-border);

  .new-task-btn {
    width: 100%;
    height: 44px;
    font-size: 14px;
    font-weight: 700;
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-container) 100%);
    border: none;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3);
    transition: all var(--transition-normal);

    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
    }

    &:active {
      transform: scale(0.98);
    }
  }
}

// 底部操作区
.sidebar-footer {
  padding: 12px;
  border-top: 1px solid var(--sidebar-border);
}

// ========================================
// 主内容区
// ========================================
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

// 顶部导航栏
.header {
  height: var(--header-height);
  background-color: var(--header-bg);
  border-bottom: 1px solid var(--sidebar-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 200px;

  .back-btn {
    cursor: pointer;
    color: var(--text-secondary);
    transition: all var(--transition-fast);
    padding: 4px;
    border-radius: 6px;

    &:hover {
      color: var(--text-primary);
      background-color: var(--surface-low);
    }
  }

  .page-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
  }

  .breadcrumb {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;

    .breadcrumb-main {
      font-weight: 800;
      color: var(--text-primary);
    }

    .breadcrumb-sub {
      color: var(--text-secondary);
      font-weight: 400;
    }

    :deep(.el-divider) {
      margin: 0;
      border-color: var(--sidebar-border);
    }
  }
}

.header-center {
  flex: 1;
  max-width: 400px;
  margin: 0 40px;

  .header-search {
    :deep(.el-input__wrapper) {
      border-radius: 20px;
      background-color: var(--surface-low);
      box-shadow: none !important;
      padding: 0 16px;
      height: 40px;
      transition: all var(--transition-normal);

      &:hover {
        background-color: var(--surface-high);
      }

      &.is-focus {
        background-color: #fff;
        box-shadow: 0 0 0 1px var(--primary-color) inset !important;
      }
    }

    :deep(.el-input__inner) {
      font-size: 14px;
    }

    :deep(.el-input__icon) {
      color: var(--text-tertiary);
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;

  .header-icon {
    cursor: pointer;
    color: var(--text-secondary);
    transition: all var(--transition-fast);
    padding: 8px;
    border-radius: 10px;

    &:hover {
      color: var(--text-primary);
      background-color: var(--surface-low);
      transform: scale(1.05);
    }
    
    &.active {
      color: var(--primary-color);
      background-color: var(--primary-bg);
    }
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    padding: 6px 12px 6px 6px;
    border-radius: 24px;
    transition: all var(--transition-fast);
    margin-left: 8px;

    &:hover {
      background-color: var(--surface-low);
    }

    .user-avatar {
      background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-container) 100%);
      color: #fff;
      font-size: 14px;
      font-weight: 600;
      transition: transform var(--transition-fast);
    }

    &:hover .user-avatar {
      transform: scale(1.05);
    }

    .user-meta {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .user-name {
      font-size: 14px;
      color: var(--text-primary);
      font-weight: 600;
    }

    .user-dept {
      font-size: 12px;
      color: var(--text-tertiary);
    }
  }
}

// 页面内容
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px 28px;
}
</style>

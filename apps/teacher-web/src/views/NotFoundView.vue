<template>
  <div class="not-found">
    <div class="not-found-content">
      <div class="error-icon">
        <el-icon :size="80" color="#0D9488"><Warning /></el-icon>
      </div>
      <h1 class="error-code">404</h1>
      <h2 class="error-title">页面未找到</h2>
      <p class="error-desc">抱歉，您访问的页面不存在或已被移除</p>
      <div class="error-actions">
        <el-button type="primary" size="large" @click="router.push('/dashboard')">
          <el-icon><HomeFilled /></el-icon>
          返回首页
        </el-button>
        <el-button size="large" @click="router.back()">
          <el-icon><ArrowLeft /></el-icon>
          返回上一页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Warning, HomeFilled, ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()
</script>

<style scoped lang="scss">
.not-found {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--content-bg);
}

.not-found-content {
  text-align: center;
  padding: 40px;

  .error-icon {
    width: 120px;
    height: 120px;
    background: var(--primary-bg);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 24px;
  }

  .error-code {
    font-size: 80px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin-bottom: 8px;
  }

  .error-title {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 12px;
  }

  .error-desc {
    font-size: 15px;
    color: var(--text-secondary);
    margin-bottom: 32px;
  }

  .error-actions {
    display: flex;
    gap: 16px;
    justify-content: center;

    .el-button {
      border-radius: var(--radius-md);
      padding: 0 28px;
      height: 48px;
      font-weight: 500;

      .el-icon {
        margin-right: 6px;
      }
    }
  }
}
</style>

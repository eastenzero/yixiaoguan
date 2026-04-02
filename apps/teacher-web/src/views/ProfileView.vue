<template>
  <div class="profile-page">
    <!-- 个人信息卡片 -->
    <div class="profile-header-card">
      <div class="profile-main">
        <el-avatar :size="80" :src="userStore.userInfo?.avatar" class="profile-avatar">
          {{ userStore.userInfo?.nickName?.charAt(0) || '张' }}
        </el-avatar>
        <div class="profile-info">
          <h2 class="profile-name">{{ userStore.userInfo?.nickName || '张教授' }}</h2>
          <p class="profile-dept">{{ userStore.userInfo?.deptName || '计算机学院' }}</p>
          <div class="profile-meta">
            <span class="meta-item">
              <el-icon><User /></el-icon>
              教师工号：T2021001
            </span>
            <span class="meta-item">
              <el-icon><Message /></el-icon>
              {{ userStore.userInfo?.email || 'zhang@example.edu.cn' }}
            </span>
            <span class="meta-item">
              <el-icon><Phone /></el-icon>
              {{ userStore.userInfo?.phonenumber || '138****8888' }}
            </span>
          </div>
        </div>
      </div>
      <div class="profile-actions">
        <el-button type="primary" :icon="Edit">编辑资料</el-button>
        <el-button :icon="Lock">修改密码</el-button>
      </div>
    </div>

    <!-- 内容双栏 -->
    <div class="profile-content">
      <!-- 左侧：基本信息 -->
      <div class="content-card">
        <div class="card-header">
          <h3 class="card-title">
            <el-icon><Document /></el-icon>
            基本信息
          </h3>
        </div>
        <div class="card-body">
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">用户名</span>
              <span class="info-value">{{ userStore.userInfo?.userName || 'zhangprof' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">真实姓名</span>
              <span class="info-value">{{ userStore.userInfo?.nickName || '张教授' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">所属学院</span>
              <span class="info-value">计算机学院</span>
            </div>
            <div class="info-item">
              <span class="info-label">职称</span>
              <span class="info-value">教授</span>
            </div>
            <div class="info-item">
              <span class="info-label">研究方向</span>
              <span class="info-value">人工智能、机器学习</span>
            </div>
            <div class="info-item">
              <span class="info-label">入职时间</span>
              <span class="info-value">2018-09-01</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：数据统计 -->
      <div class="stats-column">
        <div class="content-card">
          <div class="card-header">
            <h3 class="card-title">
              <el-icon><DataLine /></el-icon>
              本月工作统计
            </h3>
          </div>
          <div class="card-body">
            <div class="mini-stats">
              <div class="mini-stat">
                <div class="mini-value">156</div>
                <div class="mini-label">处理提问</div>
              </div>
              <div class="mini-stat">
                <div class="mini-value">42</div>
                <div class="mini-label">审批申请</div>
              </div>
              <div class="mini-stat">
                <div class="mini-value">28</div>
                <div class="mini-label">知识入库</div>
              </div>
            </div>
          </div>
        </div>

        <div class="content-card">
          <div class="card-header">
            <h3 class="card-title">
              <el-icon><Setting /></el-icon>
              系统设置
            </h3>
          </div>
          <div class="card-body">
            <div class="setting-list">
              <div class="setting-item">
                <div class="setting-info">
                  <span class="setting-name">消息通知</span>
                  <span class="setting-desc">接收系统推送和邮件通知</span>
                </div>
                <el-switch v-model="settings.notification" active-color="#0D9488" />
              </div>
              <div class="setting-item">
                <div class="setting-info">
                  <span class="setting-name">声音提醒</span>
                  <span class="setting-desc">新消息时播放提示音</span>
                </div>
                <el-switch v-model="settings.sound" active-color="#0D9488" />
              </div>
              <div class="setting-item">
                <div class="setting-info">
                  <span class="setting-name">自动回复</span>
                  <span class="setting-desc">AI置信度&gt;90%时自动回复</span>
                </div>
                <el-switch v-model="settings.autoReply" active-color="#0D9488" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import {
  User,
  Message,
  Phone,
  Edit,
  Lock,
  Document,
  DataLine,
  Setting
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const settings = reactive({
  notification: true,
  sound: true,
  autoReply: false
})
</script>

<style scoped lang="scss">
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
}

// ========================================
// 个人信息卡片
// ========================================
.profile-header-card {
  background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%);
  border-radius: var(--radius-lg);
  padding: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  color: #fff;

  .profile-main {
    display: flex;
    align-items: center;
    gap: 24px;

    .profile-avatar {
      background: rgba(255, 255, 255, 0.2);
      color: #fff;
      font-size: 32px;
      font-weight: 600;
      border: 3px solid rgba(255, 255, 255, 0.3);
    }

    .profile-info {
      .profile-name {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 6px;
      }

      .profile-dept {
        font-size: 15px;
        opacity: 0.9;
        margin-bottom: 12px;
      }

      .profile-meta {
        display: flex;
        gap: 20px;

        .meta-item {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 13px;
          opacity: 0.85;

          .el-icon {
            font-size: 14px;
          }
        }
      }
    }
  }

  .profile-actions {
    display: flex;
    gap: 12px;

    .el-button {
      border-radius: var(--radius-md);

      &:first-child {
        background: #fff;
        color: var(--primary-color);
        border: none;
        font-weight: 600;

        &:hover {
          background: rgba(255, 255, 255, 0.95);
        }
      }

      &:last-child {
        background: rgba(255, 255, 255, 0.15);
        color: #fff;
        border-color: rgba(255, 255, 255, 0.3);

        &:hover {
          background: rgba(255, 255, 255, 0.25);
        }
      }
    }
  }
}

// ========================================
// 内容区域
// ========================================
.profile-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 20px;
}

.content-card {
  background: #fff;
  border-radius: var(--radius-lg);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  overflow: hidden;

  .card-header {
    padding: 18px 24px;
    border-bottom: 1px solid var(--card-border);
    background: #F8FAFC;

    .card-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 15px;
      font-weight: 600;
      color: var(--text-primary);

      .el-icon {
        color: var(--primary-color);
      }
    }
  }

  .card-body {
    padding: 24px;
  }
}

// 基本信息
.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 16px;
    border-bottom: 1px solid #F1F5F9;

    &:last-child {
      padding-bottom: 0;
      border-bottom: none;
    }

    .info-label {
      font-size: 14px;
      color: var(--text-secondary);
    }

    .info-value {
      font-size: 14px;
      color: var(--text-primary);
      font-weight: 500;
    }
  }
}

// 统计列
.stats-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mini-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;

  .mini-stat {
    text-align: center;
    padding: 16px;
    background: #F8FAFC;
    border-radius: var(--radius-md);

    .mini-value {
      font-size: 28px;
      font-weight: 700;
      color: var(--primary-color);
      margin-bottom: 4px;
    }

    .mini-label {
      font-size: 13px;
      color: var(--text-secondary);
    }
  }
}

// 设置列表
.setting-list {
  display: flex;
  flex-direction: column;
  gap: 20px;

  .setting-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 20px;
    border-bottom: 1px solid #F1F5F9;

    &:last-child {
      padding-bottom: 0;
      border-bottom: none;
    }

    .setting-info {
      .setting-name {
        display: block;
        font-size: 14px;
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 4px;
      }

      .setting-desc {
        font-size: 12px;
        color: var(--text-tertiary);
      }
    }
  }
}

// 响应式
@media (max-width: 992px) {
  .profile-header-card {
    flex-direction: column;
    gap: 24px;
    text-align: center;

    .profile-main {
      flex-direction: column;

      .profile-meta {
        flex-wrap: wrap;
        justify-content: center;
      }
    }
  }

  .profile-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 576px) {
  .profile-header-card {
    padding: 24px;

    .profile-info {
      .profile-meta {
        flex-direction: column;
        gap: 8px;
      }
    }
  }

  .mini-stats {
    grid-template-columns: 1fr;
  }
}
</style>

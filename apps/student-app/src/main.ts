import { createSSRApp } from 'vue'
import { pinia } from './stores'
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)
  
  // 挂载 Pinia
  app.use(pinia)
  
  // 初始化用户状态
  import('./stores/user').then(({ useUserStore }) => {
    const userStore = useUserStore()
    userStore.init()
  })
  
  return {
    app
  }
}

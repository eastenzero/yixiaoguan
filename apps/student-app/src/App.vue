<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import './styles/theme.scss';
import './styles/utilities.scss';

onLaunch(() => {
  console.log("App Launch");
});
onShow(() => {
  console.log("App Show");
});
onHide(() => {
  console.log("App Hide");
});
</script>

<style lang="scss">
@import '@/styles/theme.scss';
/* CSS 变量定义 - 与 theme.scss 同步 */
:root {
  --color-primary: #{$primary};
}

/* 全局基础样式 */
page {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #F5F5F9;
  color: #1A1C1E;
}

/* 移除按钮默认样式 */
button {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font: inherit;
  color: inherit;
}

button::after {
  border: none;
}

/* 通用点击效果 */
.hover-effect {
  opacity: 0.7;
  transition: opacity 0.2s;
}
</style>

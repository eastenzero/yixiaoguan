<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import './styles/theme.scss';
import './styles/global.scss';

onLaunch(() => {
  console.log("Teacher App Launch");
});
onShow(() => {
  console.log("Teacher App Show");
});
onHide(() => {
  console.log("Teacher App Hide");
});
</script>

<style lang="scss">
@import '@/styles/theme.scss';

:root {
  --color-primary: #{$primary};
}

page {
  font-family: 'Manrope', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: $surface;
  color: $on-surface;
  -webkit-tap-highlight-color: transparent;
}

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

.hover-effect {
  opacity: 0.7;
  transition: opacity 0.2s;
}
</style>

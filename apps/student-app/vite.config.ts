import { defineConfig } from "vite";
import uni from "@dcloudio/vite-plugin-uni";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [uni()],
  server: {
    port: 5174,
    host: true,
    proxy: {
      // ── RuoYi 原生认证路由（无 /api/v1 前缀，需 strip /api）──
      // 必须放在通用 /api 规则之前，否则会被通用规则先匹配
      '/api/login': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '') // /api/login → /login
      },
      '/api/logout': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '') // /api/logout → /logout
      },
      '/api/captchaImage': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '') // /api/captchaImage → /captchaImage
      },
      '/api/getInfo': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '') // /api/getInfo → /getInfo
      },
      // ── AI 服务（必须在通用 /api 之前）──
      '/api/chat': {
        target: 'http://192.168.100.165:8000',
        changeOrigin: true
        // 路径不变：/api/chat → localhost:8000/api/chat
      },
      // ── 业务后端（通用规则，路径不变）──
      '/api': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true
        // 路径原样转发：/api/v1/xxx → localhost:8080/api/v1/xxx
      }
    }
  }
});


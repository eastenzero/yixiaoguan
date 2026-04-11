import { defineConfig } from "vite";
import uni from "@dcloudio/vite-plugin-uni";

export default defineConfig({
  plugins: [uni()],
  server: {
    port: 5175,
    host: true,
    proxy: {
      '/api/login': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/api/logout': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/api/captchaImage': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/api/getInfo': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/api/chat': {
        target: 'http://192.168.100.165:8000',
        changeOrigin: true
      },
      '/api': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true
      }
    }
  }
});

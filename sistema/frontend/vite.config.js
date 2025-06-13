import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    https: {
      key: fs.readFileSync(path.resolve(__dirname, './key.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, './cert.pem'))
    },
    proxy: {
      '/api': {
        target: 'https://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})

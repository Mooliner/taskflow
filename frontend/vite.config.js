import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'  // <-- Afegeix això

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),  // <-- Aquí li dius que @ és src
    },
  },
})

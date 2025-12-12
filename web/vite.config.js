import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import crossOriginIsolation from "vite-plugin-cross-origin-isolation";
// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    crossOriginIsolation()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    fs: {
      allow: [
        // Allow serving files from one level up to the project root
        '..',
        // Allow serving files from D:/datasets
        'D:/datasets'
      ]
    }
  }
})

import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  if (command === 'build' && mode === 'production' && !env.VITE_API_URL) {
    throw new Error('Set VITE_API_URL to the shared account backend before building.')
  }
  const proxy = { '/api': { target: env.VITE_DEV_API_TARGET || 'http://localhost:8001', changeOrigin: true } }
  return { plugins: [react()], server: { proxy }, preview: { proxy } }
})

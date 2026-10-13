import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  // The site talks to the backend at VITE_API_URL. A production build without
  // it would request /api from the static host, which has no backend.
  if (command === 'build' && mode === 'production' && !env.VITE_API_URL) {
    console.warn('\n[warning] VITE_API_URL is not set: this build will not reach a backend.\n')
  }

  // Development (and `vite preview`): /api is forwarded to the local backend,
  // so the browser needs no CORS setup and no backend address.
  const proxy = {
    '/api': {
      target: env.VITE_DEV_API_TARGET || 'http://localhost:8000',
      changeOrigin: true,
    },
  }

  return {
    plugins: [react()],
    server: { proxy },
    preview: { proxy },
  }
})

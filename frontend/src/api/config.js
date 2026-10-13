// Where the backend lives. This is the only place that decides it.
//
//  - Production build: VITE_API_URL, e.g. https://your-backend.example.com
//    (set in the hosting dashboard; it is baked in at build time).
//  - Development: leave it unset. Requests go to the relative path /api and
//    the Vite dev server forwards them to the local backend (see vite.config.js).
const configured = (import.meta.env.VITE_API_URL || '').trim().replace(/\/+$/, '')

if (!configured && import.meta.env.PROD) {
  console.error('VITE_API_URL was not set when this site was built; API requests will fail.')
}

export const API_BASE_URL = `${configured}/api`

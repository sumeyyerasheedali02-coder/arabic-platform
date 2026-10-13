// One Vercel deployment, two independent applications and asset bundles.
import { spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { loadEnv } from 'vite'

const frontend = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const tracking = path.join(frontend, 'tracking')
const output = path.join(frontend, 'dist', 'grades')
// Preview deployments may not inherit production-only Vercel variables.
// This public backend is the shared platform API, never a credential.
const environment = { ...loadEnv('production', frontend, 'VITE_'), ...process.env }
environment.VITE_API_URL ||= 'https://adaptable-solace-production-e226.up.railway.app'
if (!existsSync(path.join(tracking, 'package-lock.json'))) {
  throw new Error('The independent tracking application must be present inside the build root.')
}
function run(script, args, cwd) {
  const result = spawnSync(process.execPath, [script, ...args], { cwd, stdio: 'inherit', env: environment })
  if (result.error) throw result.error
  if (result.status !== 0) process.exit(result.status || 1)
}

run(path.join(frontend, 'node_modules/vite/bin/vite.js'), ['build'], frontend)
// Vercel currently installs the frontend package only. Install the second app's
// locked dependencies explicitly; no source or generated bundles are duplicated.
if (process.env.CI || process.env.VERCEL || !existsSync(path.join(tracking, 'node_modules/vite/bin/vite.js'))) {
  run(process.env.npm_execpath, ['ci', '--include=dev', '--no-audit', '--no-fund'], tracking)
}
run(path.join(tracking, 'node_modules/vite/bin/vite.js'), [
  'build', '--base', '/grades/', '--outDir', output, '--emptyOutDir',
], tracking)

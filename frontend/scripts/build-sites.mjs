// One Vercel deployment, two independent applications and asset bundles.
import { spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const frontend = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const tracking = path.resolve(frontend, '../tracking')
const output = path.join(frontend, 'dist', 'grades')
if (!existsSync(path.join(tracking, 'package-lock.json'))) {
  throw new Error('The tracking application must be present alongside frontend in the checkout.')
}
function run(script, args, cwd) {
  const result = spawnSync(process.execPath, [script, ...args], { cwd, stdio: 'inherit', env: process.env })
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

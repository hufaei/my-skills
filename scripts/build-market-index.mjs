#!/usr/bin/env node
/**
 * Build `market-index.json`: a plugin market index in format 1, so DeepSeek
 * Harness can list this repository from its Discover page.
 *
 * This is a release artifact, not a source file. A git source pins one exact
 * 40-hex commit, and the commit it names must already contain this bundle
 * (`package.json`, `index.js`, `cordis.patch.yml`), so generate it from a ref
 * that has the plugin, then commit the result on that same ref:
 *
 *   node scripts/build-market-index.mjs                # HEAD
 *   node scripts/build-market-index.mjs --ref v1.0.0   # a tag or commit
 *
 * The file is intentionally not tracked until that first release.
 */

import { execFileSync } from 'node:child_process'
import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = dirname(dirname(fileURLToPath(import.meta.url)))
const args = process.argv.slice(2)
const refIndex = args.indexOf('--ref')
const ref = refIndex === -1 ? 'HEAD' : args[refIndex + 1]

function fail(message) {
  console.error(`build-market-index: ${message}`)
  process.exit(1)
}

if (ref === undefined || ref === '') fail('--ref needs a value')

const git = (...argv) => {
  try {
    return execFileSync('git', argv, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim()
  } catch (error) {
    const detail = String(error.stderr ?? error.message).split('\n')[0].trim()
    fail(`git ${argv.join(' ')} failed: ${detail}`)
  }
}

const manifest = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'))
const commit = git('rev-parse', '--verify', `${ref}^{commit}`)
if (!/^[0-9a-f]{40}$/u.test(commit)) fail(`${ref} did not resolve to one commit: ${commit}`)
if (!git('ls-tree', '--name-only', commit, '--', 'index.js').includes('index.js')) {
  fail(`${ref} (${commit}) does not contain index.js, so it cannot be a bundle source`)
}

const repository = normalizeRepository(git('config', '--get', 'remote.origin.url'))
const publishTimestamp = Number(git('show', '-s', '--format=%ct', commit))
// Normalize newlines so the same icon yields the same base64 on any checkout.
const svg = readFileSync(join(root, 'icon.svg'), 'utf8').replace(/\r\n?/gu, '\n')
const icon = `data:image/svg+xml;base64,${Buffer.from(svg, 'utf8').toString('base64')}`

const index = {
  format: 1,
  title: { en: 'My Skills', zh: '我的技能库' },
  description: {
    en: 'Personal skill corpus published as a DeepSeek Harness bundle.',
    zh: '把个人技能库发布为 DeepSeek Harness 插件包。',
  },
  metadata: {
    categories: {
      skills: { title: { en: 'Skills', zh: '技能' } },
    },
    labels: {
      'first-party': { title: { en: 'First-party', zh: '自有' } },
    },
    sortKeys: {
      skills: { title: { en: 'Skill count', zh: '技能数量' }, order: 'desc' },
    },
  },
  plugins: [
    {
      name: manifest.name,
      title: { en: 'My Skills', zh: '我的技能库' },
      description: {
        en: manifest.description,
        zh: '把本仓库的 SKILL.md 技能目录发布为 DeepSeek Harness 技能，模型可按需调用。',
      },
      icon,
      author: 'hufaei',
      homepage: manifest.homepage,
      repository: { url: repository },
      metadata: {
        category: 'skills',
        keywords: ['skills', 'prompt', 'workflow'],
        labels: ['first-party'],
      },
      versions: [
        {
          version: manifest.version,
          publishTimestamp,
          source: { type: 'git', url: repository, commit },
        },
      ],
    },
  ],
}

assertIndex(index)

const file = join(root, 'market-index.json')
writeFileSync(file, `${JSON.stringify(index, null, 2)}\n`)
console.log(`build-market-index: wrote ${file} for ${manifest.name}@${manifest.version} at ${commit.slice(0, 12)}`)

/** `git@host:owner/repo.git` and `git+https://…` both collapse to a canonical https repository URL. */
function normalizeRepository(url) {
  const scp = /^git@([^/:]+):(.+)$/u.exec(url)
  const https = scp === null ? url.replace(/^git\+/u, '') : `https://${scp[1]}/${scp[2]}`
  const normalized = https.replace(/\.git$/u, '').replace(/\/+$/u, '')
  let parsed
  try {
    parsed = new URL(normalized)
  } catch {
    fail(`remote origin is not a usable repository URL: ${url}`)
  }
  if (parsed.protocol !== 'https:' || parsed.href !== normalized) {
    fail(`remote origin must be a canonical https URL, got: ${url}`)
  }
  return normalized
}

/** Refuse to write an index the market loader would reject. */
function assertIndex(candidate) {
  if (candidate.format !== 1) fail('format must be 1')
  const plugin = candidate.plugins[0]
  if (!/^[a-z0-9][a-z0-9._-]*$/u.test(plugin.name)) fail(`invalid plugin name: ${plugin.name}`)
  const version = plugin.versions[0]
  if (!/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/u.test(version.version)) fail(`invalid version: ${version.version}`)
  if (!Number.isInteger(version.publishTimestamp) || version.publishTimestamp >= 1e11) {
    fail(`publishTimestamp must be unix seconds: ${version.publishTimestamp}`)
  }
  const source = version.source
  if (source.type !== 'git') fail(`unsupported source type: ${source.type}`)
  if (!/^[0-9a-f]{40}$/u.test(source.commit)) fail(`commit must be 40 lowercase hex: ${source.commit}`)
  const url = new URL(source.url)
  if (url.protocol !== 'https:' || url.href !== source.url || url.search !== '' || url.hash !== '') {
    fail(`source URL must be a canonical https URL without query or fragment: ${source.url}`)
  }
  if (url.pathname.split('/').filter(Boolean).length < 2) fail(`source URL needs owner and repository: ${source.url}`)
  if (source.url.endsWith('.tar.gz')) fail('source URL must not end with .tar.gz')
  const match = /^data:image\/svg\+xml;base64,([A-Za-z0-9+/=]+)$/u.exec(plugin.icon)
  if (match === null) fail('icon must be a base64 svg data URL')
  const iconBytes = Buffer.from(match[1], 'base64')
  if (iconBytes.length === 0 || iconBytes.length > 32768) fail(`icon must be 1..32768 bytes, got ${iconBytes.length}`)
}

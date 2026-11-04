#!/usr/bin/env node
/**
 * Build `market-index.json`: a plugin market index in format 1, so DeepSeek
 * Harness can list this repository from its Discover page.
 *
 * A git source pins one exact 40-hex commit, so the index is a release
 * artifact: regenerate it for the ref you want the market to offer.
 *
 *   node scripts/build-market-index.mjs                 # current HEAD
 *   node scripts/build-market-index.mjs --ref v1.0.0    # a tag or branch
 */

import { execFileSync } from 'node:child_process'
import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = dirname(dirname(fileURLToPath(import.meta.url)))
const args = process.argv.slice(2)
const refIndex = args.indexOf('--ref')
const ref = refIndex === -1 ? 'HEAD' : args[refIndex + 1]

if (ref === undefined) {
  console.error('build-market-index: --ref needs a value')
  process.exit(1)
}

const git = (...argv) => execFileSync('git', argv, { cwd: root, encoding: 'utf8' }).trim()

const manifest = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'))
const commit = git('rev-parse', ref)
if (!/^[0-9a-f]{40}$/u.test(commit)) {
  console.error(`build-market-index: ${ref} did not resolve to one commit: ${commit}`)
  process.exit(1)
}

const repository = normalizeRepository(git('remote', 'get-url', 'origin'))
const publishTimestamp = Number(git('show', '-s', '--format=%ct', commit))
const icon = `data:image/svg+xml;base64,${readFileSync(join(root, 'icon.svg')).toString('base64')}`

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
      'synced-upstream': { title: { en: 'Synced upstream', zh: '上游同步' } },
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
        keywords: ['skills', 'prompt', 'workflow', '中文'],
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

const file = join(root, 'market-index.json')
writeFileSync(file, `${JSON.stringify(index, null, 2)}\n`)
console.log(`build-market-index: wrote ${file} for ${manifest.name}@${manifest.version} at ${commit.slice(0, 12)}`)

/** `git@github.com:owner/repo.git` and `git+https://…` both collapse to a canonical https repository URL. */
function normalizeRepository(url) {
  const scp = /^git@([^:]+):(.+)$/.exec(url)
  const https = scp === null ? url.replace(/^git\+/u, '') : `https://${scp[1]}/${scp[2]}`
  return https.replace(/\.git$/u, '').replace(/\/+$/u, '')
}

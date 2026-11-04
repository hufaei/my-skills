import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, isAbsolute, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

/**
 * Host plugin: publish this repository's SKILL.md corpus as runtime skills.
 *
 * Each `<root>/<skill>/SKILL.md` becomes one `ctx.skills` runtime registration,
 * with the skill's own directory as its resource base so relative references
 * (`references/*.md`, `agents/*.yaml`) resolve for the model.
 */

const PACKAGE_ROOT = dirname(fileURLToPath(import.meta.url))
const PROVIDER = 'my-skills'
const SKILL_NAME = /^[a-z0-9]+(?:-[a-z0-9]+)*$/
const DEFAULT_ROOTS = ['skills', 'synced']
const TOP_KEY = /^([A-Za-z][A-Za-z0-9_-]*):(?:[ \t]+(.*))?$/
const BLOCK_MARKER = /^([|>])([+-]?)(\d*)$/

export const name = 'my-skills'
export const inject = ['skills']

/** Resolve the row config into explicit settings; any value the row omits keeps its default. */
function normalizeConfig(config) {
  const source = config !== null && typeof config === 'object' ? config : {}
  const declared = Array.isArray(source.roots)
    ? source.roots.filter((root) => typeof root === 'string' && root.trim() !== '')
    : undefined
  const includeSynced = source.includeSynced !== false
  const roots = declared ?? DEFAULT_ROOTS.filter((root) => includeSynced || root !== 'synced')
  return {
    roots: roots.map((root) => ({ root, path: isAbsolute(root) ? root : resolve(PACKAGE_ROOT, root) })),
    maxSkills: Number.isInteger(source.maxSkills) && source.maxSkills > 0 ? source.maxSkills : 0,
  }
}

/**
 * Read one SKILL.md into frontmatter fields and body.
 * Handles plain scalars, quoted scalars, and `|`/`>` block scalars; nested
 * mappings are skipped because only name and description are needed.
 */
function parseSkillFile(source) {
  // Normalize line endings first: `.` and `$` never match a bare `\r`, which
  // would silently drop every CRLF-authored field.
  const text = source.includes('\r') ? source.replace(/\r\n?/gu, '\n') : source
  if (!text.startsWith('---')) return undefined
  const open = text.indexOf('\n')
  if (open === -1) return undefined
  const close = /\n---[ \t]*(?:\r?\n|$)/.exec(text.slice(open))
  if (close === null) return undefined
  const fields = readMapping(text.slice(open + 1, open + close.index))
  const body = text.slice(open + close.index + close[0].length).trim()
  return { fields, body }
}

/** Read the small subset of YAML frontmatter the skill catalog needs. */
function readMapping(raw) {
  const lines = raw.split(/\r?\n/)
  const fields = new Map()
  let index = 0
  while (index < lines.length) {
    const line = lines[index]
    if (/^\s/.test(line) || line.trim() === '' || line.trimStart().startsWith('#')) {
      index += 1
      continue
    }
    const match = TOP_KEY.exec(line)
    if (match === null) {
      index += 1
      continue
    }
    const key = match[1]
    const inline = (match[2] ?? '').trim()
    index += 1
    const marker = BLOCK_MARKER.exec(inline)
    if (marker !== null) {
      const collected = []
      while (index < lines.length && (lines[index].trim() === '' || /^\s/.test(lines[index]))) {
        collected.push(lines[index])
        index += 1
      }
      fields.set(key, foldBlock(collected, marker[1] === '>'))
      continue
    }
    if (inline !== '') {
      fields.set(key, unquote(inline))
      continue
    }
    // No inline value: either a nested mapping (skipped) or an indented continuation.
    const collected = []
    let nested = false
    while (index < lines.length && (lines[index].trim() === '' || /^\s/.test(lines[index]))) {
      if (TOP_KEY.test(lines[index].trimStart()) && /^\s+\S/.test(lines[index])) nested = true
      collected.push(lines[index])
      index += 1
    }
    if (!nested) {
      const joined = collected.map((part) => part.trim()).filter(Boolean).join(' ')
      if (joined !== '') fields.set(key, unquote(joined))
    }
  }
  return fields
}

/** Join an indented block scalar, folding newlines to spaces for a one-line summary. */
function foldBlock(lines, folded) {
  const body = lines.filter((line, position) => !(position === 0 && line.trim() === ''))
  const indents = body.filter((line) => line.trim() !== '').map((line) => /^\s*/.exec(line)[0].length)
  const indent = indents.length === 0 ? 0 : Math.min(...indents)
  const text = body.map((line) => line.slice(indent)).join('\n').trim()
  return folded ? text.replace(/\s*\n\s*/g, ' ') : text.replace(/\s*\n\s*/g, ' ')
}

function unquote(value) {
  const trimmed = value.trim()
  if (trimmed.length >= 2 && ((trimmed.startsWith('"') && trimmed.endsWith('"')) || (trimmed.startsWith("'") && trimmed.endsWith("'")))) {
    return trimmed.slice(1, -1)
  }
  return trimmed
}

/** Yield every readable skill under one root, in directory-name order. */
function discover(settings, warn) {
  const found = []
  for (const { root, path } of settings.roots) {
    if (!existsSync(path) || !statSync(path).isDirectory()) {
      warn(`skill root "${root}" is missing at ${path}`)
      continue
    }
    for (const entry of readdirSync(path).sort()) {
      const directory = join(path, entry)
      if (!statSync(directory).isDirectory()) continue
      const file = join(directory, 'SKILL.md')
      if (!existsSync(file)) continue
      found.push({ root, directory, file })
    }
  }
  return found
}

export function apply(ctx, config) {
  const settings = normalizeConfig(config)
  const warn = (message) => ctx.logger.warn(`my-skills: ${message}`)
  const registered = new Set()

  for (const { directory, file } of discover(settings, warn)) {
    if (settings.maxSkills !== 0 && registered.size >= settings.maxSkills) break
    let parsed
    try {
      parsed = parseSkillFile(readFileSync(file, 'utf8'))
    } catch (error) {
      warn(`cannot read ${file}: ${String(error)}`)
      continue
    }
    if (parsed === undefined) {
      warn(`${file} has no frontmatter; skipped`)
      continue
    }
    const name = parsed.fields.get('name') ?? dirname(file).split(/[\\/]/).pop()
    const description = parsed.fields.get('description')
    if (name === undefined || !SKILL_NAME.test(name)) {
      warn(`${file} declares a name that is not kebab-case; skipped`)
      continue
    }
    if (description === undefined || description === '') {
      warn(`${file} declares no description; skipped`)
      continue
    }
    if (registered.has(name)) {
      warn(`duplicate skill "${name}" at ${file}; kept the first`)
      continue
    }
    try {
      // `register` binds the disposer to this plugin's fiber, so unloading the
      // row removes exactly the skills it added.
      ctx.skills.register({
        name,
        description,
        whenToUse: parsed.fields.get('whenToUse'),
        content: parsed.body,
        path: file,
        source: 'bundled',
        provider: PROVIDER,
        resourceBase: { kind: 'directory', path: directory },
        invocation: { modelInvocable: true, userInvocable: true },
      })
      registered.add(name)
    } catch (error) {
      warn(`cannot register "${name}": ${String(error)}`)
    }
  }

  ctx.logger.info(`my-skills: registered ${registered.size} skill(s) from ${settings.roots.length} root(s)`)
}

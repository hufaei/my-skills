import { readdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, isAbsolute, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

/**
 * Host plugin: publish this repository's SKILL.md corpus as runtime skills.
 *
 * Each `<root>/<skill>/SKILL.md` becomes one `ctx.skills` runtime registration,
 * with the skill's own directory as its resource base so relative references
 * (`references/*.md`, `agents/*.yaml`) resolve for the model.
 *
 * The frontmatter reader below is deliberately narrow: `name`, `description`,
 * `whenToUse`, and the two invocation switches. It follows the shipped
 * filesystem provider's rules for the fields it does read, and skips a skill
 * rather than guessing when a value has the wrong shape.
 */

const PACKAGE_ROOT = dirname(fileURLToPath(import.meta.url))
const PROVIDER = 'my-skills'
const SKILL_NAME = /^[a-z0-9]+(?:-[a-z0-9]+)*$/u
const DEFAULT_ROOTS = ['skills', 'synced']
const TOP_KEY = /^([A-Za-z][A-Za-z0-9_-]*):(?:[ \t]+(.*))?$/u
const BLOCK_MARKER = /^([|>])([+-]?)(\d*)$/u
const SEQUENCE_ITEM = /^-(?:[ \t]|$)/u
const NESTED_KEY = /^[A-Za-z][A-Za-z0-9_-]*:/u
const TRUE_WORDS = new Set(['true', 'yes', 'on'])
const FALSE_WORDS = new Set(['false', 'no', 'off'])
/** Keys the shipped provider rejects: these spellings silently changed meaning. */
const LEGACY_INVOCATION_KEYS = [
  ['disableModelInvocation', 'disable-model-invocation'],
  ['modelInvocable', 'disable-model-invocation'],
  ['userInvocable', 'user-invocable'],
]

export const name = 'my-skills'
export const inject = ['skills']

/** Resolve the row config into explicit settings; any value the row omits keeps its default. */
function normalizeConfig(config) {
  const source = config !== null && typeof config === 'object' ? config : {}
  const declared = Array.isArray(source.roots)
    ? source.roots.filter((root) => typeof root === 'string' && root.trim() !== '')
    : []
  const includeSynced = source.includeSynced !== false
  const roots = declared.length > 0
    ? declared
    : DEFAULT_ROOTS.filter((root) => includeSynced || root !== 'synced')
  return {
    roots: roots.map((root) => ({ root, path: isAbsolute(root) ? root : resolve(PACKAGE_ROOT, root) })),
    // An explicit empty `roots` array would otherwise publish nothing at all.
    ignoredEmptyRoots: Array.isArray(source.roots) && declared.length === 0,
    maxSkills: Number.isInteger(source.maxSkills) && source.maxSkills > 0 ? source.maxSkills : 0,
  }
}

/**
 * Read one SKILL.md into frontmatter fields and body.
 * Comment lines, nested mappings, and sequence values are skipped so a field
 * only ever holds a scalar string.
 */
function parseSkillFile(source) {
  // Normalize line endings first: `.` and `$` never match a bare `\r`, which
  // would silently drop every CRLF-authored field.
  const text = source.includes('\r') ? source.replace(/\r\n?/gu, '\n') : source
  const trimmed = text.startsWith('\uFEFF') ? text.slice(1) : text
  if (!trimmed.startsWith('---')) return undefined
  const open = trimmed.indexOf('\n')
  if (open === -1) return undefined
  const close = /\n---[ \t]*(?:\r?\n|$)/u.exec(trimmed.slice(open))
  if (close === null) return undefined
  return {
    fields: readMapping(trimmed.slice(open + 1, open + close.index)),
    body: trimmed.slice(open + close.index + close[0].length).trim(),
  }
}

/** Read the small subset of YAML frontmatter the skill catalog needs. */
function readMapping(raw) {
  const lines = raw.split('\n')
  const fields = new Map()
  let index = 0
  while (index < lines.length) {
    const line = lines[index]
    if (/^\s/u.test(line) || line.trim() === '' || line.trimStart().startsWith('#')) {
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
    const indented = []
    while (index < lines.length && (lines[index].trim() === '' || /^\s/u.test(lines[index]))) {
      indented.push(lines[index])
      index += 1
    }
    if (BLOCK_MARKER.test(inline)) {
      fields.set(key, readBlock(indented))
      continue
    }
    if (inline !== '') {
      fields.set(key, unquote(inline))
      continue
    }
    const meaningful = indented.filter((part) => part.trim() !== '')
    if (meaningful.length === 0) continue
    // A sequence or a nested mapping is not a scalar; leave the key unset
    // rather than joining its parts into a plausible-looking string.
    if (SEQUENCE_ITEM.test(meaningful[0].trimStart()) || NESTED_KEY.test(meaningful[0].trimStart())) continue
    fields.set(key, unquote(meaningful.map((part) => part.trim()).join(' ')))
  }
  return fields
}

/**
 * Read an indented block scalar as one summary line.
 * The catalog shows a single line, so `|` and `>` collapse identically here.
 */
function readBlock(lines) {
  const body = lines.filter((line, position) => !(position === 0 && line.trim() === ''))
  const indents = body.filter((line) => line.trim() !== '').map((line) => /^[ \t]*/u.exec(line)[0].length)
  const indent = indents.length === 0 ? 0 : Math.min(...indents)
  return body.map((line) => line.slice(indent)).join('\n').trim().replace(/\s*\n\s*/gu, ' ')
}

/** Strip YAML scalar quoting, including the escapes those styles allow. */
function unquote(value) {
  const trimmed = value.trim()
  if (trimmed.length >= 2 && trimmed.startsWith('"') && trimmed.endsWith('"')) {
    return trimmed.slice(1, -1).replace(/\\(["\\])/gu, '$1')
  }
  if (trimmed.length >= 2 && trimmed.startsWith("'") && trimmed.endsWith("'")) {
    return trimmed.slice(1, -1).replaceAll("''", "'")
  }
  return trimmed
}

/** Read a YAML boolean the way the shipped provider does, or throw for anything else. */
function booleanField(fields, key) {
  if (!fields.has(key)) return undefined
  const raw = fields.get(key).trim().toLowerCase()
  if (raw === '1' || TRUE_WORDS.has(raw)) return true
  if (raw === '0' || FALSE_WORDS.has(raw)) return false
  throw new TypeError(`frontmatter field "${key}" must be a boolean`)
}

/** Resolve the invocation policy declared by frontmatter. */
function invocationOf(fields) {
  for (const [legacy, canonical] of LEGACY_INVOCATION_KEYS) {
    if (fields.has(legacy)) throw new Error(`frontmatter field "${legacy}" is unsupported; use "${canonical}"`)
  }
  return {
    modelInvocable: booleanField(fields, 'disable-model-invocation') !== true,
    userInvocable: booleanField(fields, 'user-invocable') !== false,
  }
}

/** Yield every skill directory under the configured roots, in name order. */
function discover(settings, warn) {
  const found = []
  for (const { root, path } of settings.roots) {
    let entries
    try {
      if (!statSync(path).isDirectory()) {
        warn(`skill root "${root}" is not a directory: ${path}`)
        continue
      }
      entries = readdirSync(path)
    } catch (error) {
      warn(`cannot read skill root "${root}" at ${path}: ${String(error)}`)
      continue
    }
    for (const entry of entries.sort()) {
      const directory = join(path, entry)
      let isDirectory = false
      try {
        isDirectory = statSync(directory).isDirectory()
      } catch {
        continue
      }
      if (!isDirectory) continue
      found.push({ root, directory, file: join(directory, 'SKILL.md') })
    }
  }
  return found
}

export function apply(ctx, config) {
  const settings = normalizeConfig(config)
  const warn = (message) => ctx.logger.warn(`my-skills: ${message}`)
  const registered = new Set()

  if (settings.ignoredEmptyRoots) warn(`"roots" was empty; falling back to ${DEFAULT_ROOTS.join(', ')}`)

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
    const name = parsed.fields.get('name') ?? directory.split(/[\\/]/u).pop()
    const description = parsed.fields.get('description')
    if (!SKILL_NAME.test(name)) {
      warn(`${file} declares a name that is not kebab-case; skipped`)
      continue
    }
    if (typeof description !== 'string' || description === '') {
      warn(`${file} declares no string description; skipped`)
      continue
    }
    let invocation
    try {
      invocation = invocationOf(parsed.fields)
    } catch (error) {
      warn(`${file} has an invalid invocation policy: ${String(error)}; skipped`)
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
        source: 'runtime',
        provider: PROVIDER,
        resourceBase: { kind: 'directory', path: directory },
        invocation,
      })
      registered.add(name)
    } catch (error) {
      warn(`cannot register "${name}": ${String(error)}`)
    }
  }

  ctx.logger.info(`my-skills: registered ${registered.size} skill(s) from ${settings.roots.length} root(s)`)
}

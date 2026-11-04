# 作为 DeepSeek Harness 插件使用

本仓库同时是一个 DeepSeek Harness（DSH）插件包：仓库根就是包根，
`package.json` 的 `dsh.bundle.patch` 指向 `cordis.patch.yml`，`index.js` 把
`skills/` 与 `synced/` 下的每个 `SKILL.md` 注册成 Harness 技能。

安装后在同一个 profile 里，这些技能对模型可见、可按需加载，正文与
`references/`、`agents/` 等相对资源都以各自技能目录为基准解析。

## 仓库结构中的 DSH 部分

| 路径 | 作用 |
|---|---|
| `package.json` | 包身份；`dsh.bundle.patch` 声明 bundle，`dsh.install` 声明三种拉取方式 |
| `cordis.patch.yml` | 往 profile 的入口列表插入一行 `my-skills` |
| `index.js` | Host 插件：扫描技能目录并注册到 `skills` 服务 |
| `locale/en.json`、`locale/zh.json` | 插件面板显示的标题与说明 |
| `icon.svg` | 插件图标 |
| `market-index.json` | format 1 插件市场索引，供 Discover 页面收录 |
| `scripts/build-market-index.mjs` | 重新生成上面的索引 |

`dsh.bundle` 是 DSH 判定"这是一个插件包"的唯一依据；`dsh.install`
（tarball / zip / git 三个地址）是给安装器和自更新流程读取的下载线索。
包内不声明 `engines.dsh`，因此不对运行时版本设限；若要显式限定，只能写
`engines.dsh`（如 `">=0.2.1-rc.0"`），`dshTarget`、`dshTargets` 不是 DSH 读取的字段。

## 安装

仓库不在 npm 上，用 git 地址安装。DSH 把 `github:owner/repo` 交给 pnpm，
装完校验 `dsh.bundle` 存在，再把包名加入当前 profile 的 bundle 选择。

```powershell
# Windows 桌面版 CLI（未加入 PATH 时用完整路径）
& "$env:LOCALAPPDATA\Programs\DeepSeek Harness\resources\runtime\cli\bin\dsh.cmd" `
  plugin --profile desktop add github:hufaei/my-skills
```

等价地，在会话里让 Harness 自己装：`plugin_manager` 的 `install_bundle`，
`target` 传 `github:hufaei/my-skills`。两种方式做的是同一件事。

固定到某个提交或标签（推荐，行为最确定）：

```powershell
& "$env:LOCALAPPDATA\Programs\DeepSeek Harness\resources\runtime\cli\bin\dsh.cmd" `
  plugin --profile desktop add "github:hufaei/my-skills#v1.0.0"
```

## 验证

- `plugin_manager` 的 `list_bundles` 应出现 `dsh-my-skills`，`list_plugins`
  中出现 `my-skills` 行且 `enabled` 为真。
- 会话技能目录里应出现 44 个 `jl-*` 技能（9 个 `skills/`、35 个 `synced/`）。
- 插件面板里该行的标题是 `我的技能库` / `My Skills`，图标为本仓库 `icon.svg`。

## 更新

仓库内容变化后，DSH 不会自动跟随；按确定性从高到低选一种：

1. 换一个 ref 重装（最确定，spec 变了 pnpm 必然重新解析）：

   ```powershell
   dsh plugin --profile desktop add "github:hufaei/my-skills#<新tag或commit>"
   ```

2. 让 pnpm 重新解析同名 git 依赖：

   ```powershell
   dsh plugin --profile desktop update dsh-my-skills
   ```

3. 先卸载再安装：`plugin_manager` 的 `remove_bundle` 之后重新 `install_bundle`。

装完核对 `~/.dsh/profiles/desktop/package.json` 里 `dependencies` 记录的
spec，以及 `node_modules/dsh-my-skills/package.json` 的 `version`。
替换已安装包需要重启 Harness 才会加载新的 JavaScript 模块。

## 配置

`cordis.patch.yml` 里的行 config 由 `index.js` 读取：

| 键 | 默认 | 含义 |
|---|---|---|
| `roots` | `[skills, synced]` | 要扫描的技能根目录，相对包根；也可写绝对路径 |
| `includeSynced` | `true` | 未显式写 `roots` 时，是否带上 `synced/` |
| `maxSkills` | 不限 | 注册数量上限，用于临时收窄技能目录 |

只发布自建技能：把 `cordis.patch.yml` 的 `roots` 改成 `[skills]`，或在
profile 的用户层覆盖同一行的 `config`（`config` 是整体替换，需重述每个键）。

单个技能不合规时不会拖垮插件：名字不是 kebab-case、缺 `description`、
没有 frontmatter 的目录会被跳过并留下一条警告，其余技能照常注册。

## 卸载

`plugin_manager` 的 `remove_bundle`，`target` 传 `dsh-my-skills`。它同时
移除依赖与 bundle 选择，插件行随之消失，技能一并注销。

## 插件市场索引

`market-index.json` 是 format 1 索引，托管在仓库里即可被 Discover 页面收录：

```text
https://raw.githubusercontent.com/hufaei/my-skills/main/market-index.json
```

索引的 git source 必须钉一个 40 位提交，所以它是发布产物而不是源文件：改了
技能或版本之后重新生成并提交。

```powershell
node scripts/build-market-index.mjs                # 当前 HEAD
node scripts/build-market-index.mjs --ref v1.0.1   # 某个 tag 或分支
```

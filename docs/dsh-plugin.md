# 作为 DeepSeek Harness 插件使用

本仓库同时是一个 DeepSeek Harness（DSH）插件包：仓库根就是包根，
`package.json` 的 `dsh.bundle.patch` 指向 `cordis.patch.yml`，`index.js` 把
`skills/` 与 `synced/` 下的每个 `SKILL.md` 注册成 Harness 技能。

安装后在同一个 profile 里，这些技能对模型可见、可按需加载，正文与
`references/`、`agents/` 等相对资源都以各自技能目录为基准解析。

## 仓库结构中的 DSH 部分

| 路径 | 作用 |
|---|---|
| `package.json` | 包身份；`dsh.bundle.patch` 是唯一的识别依据 |
| `cordis.patch.yml` | 往 profile 的入口列表插入一行 `my-skills` |
| `index.js` | Host 插件：扫描技能目录并注册到 `skills` 服务 |
| `locale/en.json`、`locale/zh.json` | 插件面板显示的标题与说明 |
| `icon.svg` | 插件图标 |
| `scripts/build-market-index.mjs` | 生成市场索引；未发布前仓库里没有 `market-index.json` |

## 识别机制

DSH 判定"这是一个插件包"只看 `package.json` 里有没有 `dsh.bundle` 对象。
没有它就只当普通依赖装进来，并在日志里留一条
`declares no dsh.bundle — installed as a plain dependency, not a profile layer`，
整个包层不生效。

包内不声明 `engines.dsh`，因此不对运行时版本设限。要显式限定范围只能用
`engines.dsh`；`dshTarget`、`dshTargets` 不是 DSH 读取的字段（实测写入后
兼容判定仍返回空）。

## 安装

仓库不在 npm 上，用 git 地址安装。DSH 把 `github:owner/repo` 交给 pnpm，
装完读 `dsh.bundle`、加载 patch，并把包名加入当前 profile 的 bundle 选择。

```powershell
# Windows 桌面版自带 CLI；独立安装的 npm dsh 会拒绝操作 desktop profile
& "$env:LOCALAPPDATA\Programs\DeepSeek Harness\resources\runtime\cli\bin\dsh.cmd" `
  plugin --profile desktop add github:hufaei/my-skills
```

等价地，在会话里让 Harness 自己装：`plugin_manager` 的 `install_bundle`，
`target` 传 `github:hufaei/my-skills`。两种方式做的是同一件事。

固定版本（推荐，行为最确定）。本仓库现有 tag `v0.1.0`、`v0.2.0` 属于技能
仓库本身，早于插件包，不包含 `package.json`；按版本安装要先给含插件的提交
打 tag，或者直接钉 40 位提交：

```powershell
& "$env:LOCALAPPDATA\Programs\DeepSeek Harness\resources\runtime\cli\bin\dsh.cmd" `
  plugin --profile desktop add "github:hufaei/my-skills#<40 位 commit>"
```

## 验证

- `plugin_manager` 的 `list_bundles` 应出现 `dsh-my-skills`，`list_plugins`
  中出现 `my-skills` 行且 `enabled` 为真。
- 会话技能目录里应出现 45 个 `jl-*` 技能（9 个 `skills/`、36 个 `synced/`）。
- 插件面板里该行的标题是 `我的技能库` / `My Skills`，图标为本仓库 `icon.svg`。

`jl-archify` 随包提供渲染脚本，按 Harness 的前置字段规则允许模型和用户调用。
运行渲染脚本需要 Node.js 18 或更高版本。

## 更新

仓库内容变化后，DSH 不会自动跟随；按确定性从高到低选一种：

1. 换一个 ref 重装（最确定，spec 变了 pnpm 必然重新解析）：

   ```powershell
   dsh plugin --profile desktop add "github:hufaei/my-skills#<新 commit 或 tag>"
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
| `roots` | `[skills, synced]` | 要扫描的技能根目录，相对包根；也可写绝对路径。空数组会被忽略并回退默认值 |
| `includeSynced` | `true` | 未显式写 `roots` 时，是否带上 `synced/` |
| `maxSkills` | 不限 | 注册数量上限，用于临时收窄技能目录 |

只发布自建技能：把 `cordis.patch.yml` 的 `roots` 改成 `[skills]`，或在
profile 的用户层覆盖同一行的 `config`（`config` 是整体替换，需重述每个键）。

单个技能的容错行为与官方文件系统 provider 对齐，出问题只跳过该技能并留一条
警告，不影响其余技能：

- 缺 `name`/`description`、`name` 不是 kebab-case、`description` 是序列或嵌套
  映射而非标量：跳过。
- `disable-model-invocation: true` 关掉模型调用，`user-invocable: false` 关掉
  用户调用；写成非布尔值：跳过。
- 用了已废弃的 `disableModelInvocation`、`modelInvocable`、`userInvocable`：
  跳过并提示改用规范键。
- 技能目录或根目录读不了：只警告，不中断插件加载。

## 卸载

`plugin_manager` 的 `remove_bundle`，`target` 传 `dsh-my-skills`。它同时
移除依赖与 bundle 选择，插件行随之消失，技能一并注销。

## 插件市场索引

`market-index.json` 是 format 1 索引，托管在仓库里即可被 Discover 页面收录。
它是**发布产物而不是源文件**：git source 必须钉一个 40 位提交，而那个提交
必须已经包含本插件包，否则市场会装出一个没有 `dsh.bundle` 的空壳。所以顺序
只能是：先合并插件代码，再在同一个 ref 上生成索引并单独提交。

```powershell
# 在已包含 index.js / cordis.patch.yml 的提交上运行
node scripts/build-market-index.mjs                 # 当前 HEAD
node scripts/build-market-index.mjs --ref v1.0.0    # 某个 tag 或提交
```

脚本会拒绝不合格的输入：ref 解析不到、目标提交里没有 `index.js`、remote 不是
规范 https 地址、以及任何会被市场加载器拒绝的字段（提交不是 40 位 hex、URL
带 query、图标超过 32 KiB 等）。

生成后把索引文件推到默认分支，再把它加入 Discover 的索引列表：

```text
https://raw.githubusercontent.com/hufaei/my-skills/main/market-index.json
```

# my-skills

JL 的个人 Codex Skill 仓库。这里同时保存自建 Skill 和经过来源记录的上游
Skill 完整副本；克隆仓库并运行安装脚本后，即可在 Codex 中使用统一的
`jl-*` 名称。

仓库是本机安装内容的唯一来源：`skills/` 可以直接维护，`synced/` 只能通过
同步脚本从固定上游重新生成。当前包含 21 个 Skill，其中 7 个自建、14 个
上游同步。

## 特点

- **开箱即用：** 上游 Skill 已完整保存在仓库中，安装不依赖额外 Skill 仓库。
- **统一命名：** 所有 Skill 使用 `jl-` 前缀，避免与其他本机 Skill 重名。
- **按需调用：** 完整工程工作流不会套在每个小任务上；显式调用后先形成计划
  并等待执行口令，再自动选择代理、TDD 和隔离方式，避免例行选择打断。
- **可追溯同步：** 上游地址、源路径、固定提交、内容 SHA-256、许可证和机械
  转换规则记录在 [`sources.yaml`](sources.yaml)。
- **安全安装：** 安装脚本生成独立的全局副本；发现未受管理的同名内容或本机
  修改时会拒绝覆盖。

## 安装

### 安装方式与目录映射

仓库是唯一编辑源，Codex 的全局 Skill 目录是由安装脚本生成的本机副本：

```text
my-skills/skills/jl-<name>  ─┐
                             ├─复制→ ~/.codex/skills/jl-<name>
my-skills/synced/jl-<name>  ─┘
```

`skills/` 保存本仓库直接维护的 Skill，`synced/` 保存从上游生成的完整副本；
两者都会安装。不要把 `skills/` 或 `synced/` 整个目录嵌套复制到全局目录，
每个 `jl-*` 必须直接位于 `~/.codex/skills/` 下。设置了 `CODEX_HOME` 时，目标
改为 `$CODEX_HOME/skills/`。

在 Windows PowerShell 中，默认目标是 `$HOME\.codex\skills\jl-<name>`，通常
对应 `C:\Users\<用户名>\.codex\skills\jl-<name>`；设置 `CODEX_HOME` 后改为
`$env:CODEX_HOME\skills\jl-<name>`。

安装后，全局目录中的每个 `jl-*` 都是独立副本，不依赖仓库路径。可以移动或
删除克隆，但全局副本不应手工修改；请在仓库中修改后重新运行安装脚本。

### 让 Codex 安装

在新的 Codex 任务中说：

```text
安装或更新 https://github.com/hufaei/my-skills：按照仓库 README，把 skills/ 和 synced/ 下的全部 jl-* 直接复制到 Codex 全局 Skill 目录，不要创建软链接。
```

### 在新电脑上手动安装

需要 Git 和 Python 3。下面把仓库克隆到便于后续更新的位置。

#### macOS/Linux

```bash
mkdir -p ~/.local/share
git clone https://github.com/hufaei/my-skills.git ~/.local/share/my-skills
cd ~/.local/share/my-skills
python3 scripts/install.py --dry-run
python3 scripts/install.py
```

#### Windows PowerShell

```powershell
$repoPath = Join-Path $HOME "my-skills"
git clone https://github.com/hufaei/my-skills.git $repoPath
Set-Location $repoPath
py -3 .\scripts\install.py --dry-run
py -3 .\scripts\install.py
```

如果系统没有 `py` 启动器，但 `python` 指向 Python 3，请把 `py -3` 替换为
`python`。

安装脚本把 `skills/` 和 `synced/` 下的每个 `jl-*` 目录完整复制到
`$CODEX_HOME/skills/`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills/`。
`--dry-run` 只预览，不修改本机。安装器会安装新增 Skill、更新自己管理且没有
本机改动的旧副本，并把内容相同的旧安装纳入管理；遇到未受管理的同名内容或
手工修改过的全局副本时会列出冲突并停止。

安装后新开一个 Codex 任务，让 Skill 清单重新加载。

### 更新本机内容

全局副本不会自动跟随仓库变化。拉取仓库更新后，重新运行安装脚本同步新增和
变更的 Skill：

macOS/Linux：

```bash
cd ~/.local/share/my-skills
git pull --ff-only
python3 scripts/install.py
```

Windows PowerShell：

```powershell
Set-Location (Join-Path $HOME "my-skills")
git pull --ff-only
py -3 .\scripts\install.py
```

如果实际克隆位置不是 `~/.local/share/my-skills`，请进入自己的仓库目录再执行。
安装完成后可以删除仓库；以后更新时重新克隆并运行相同命令即可。为了让
`git pull --ff-only` 更方便，也可以长期保留这份克隆。

安装器使用跨平台 Python 文件 API，不创建软链接，也不依赖 Bash。部分
`synced/` 上游 Skill 自带 `.sh` 辅助脚本；在 Windows 使用这些特定功能时需要
Git Bash 或 WSL。没有实际运行相应脚本时，不应声称它们已经过原生 PowerShell
验证。

## 调用策略

完整工作流和大多数组件只在显式选择或使用 `$jl-*` 调用时加载：

```text
$jl-engineering-orchestra <需求与验收标准>
```

Orchestra 调用后只进行只读检查、方案讨论和计划输出。用户查看计划并明确回复
`执行` 后才会修改仓库、创建分支或 Worktree、安装依赖、分配实施代理或执行
发布操作；`可以`、`继续` 或对方案表示认可不会越过执行门禁。

以下 5 个低误触 Skill 允许根据明确的自然语言请求自动调用：

- `jl-clean-branches`：清理已合并分支或 Worktree。
- `jl-sync-skills`：检查或同步 Skill 上游更新。
- `jl-doc-steward`：创建、更新或审查指定工程文档。
- `jl-lean-tests`：明确要求设计、编写、精简或审查测试。
- `jl-prompt-architect`：明确进行 Prompt Engineering，或编写、审查供 AI
  模型、Agent、工具或 Runtime 使用的提示词。

完整 Orchestra、ChatGPT Pro 协作流和所有 `synced/` 工作流组件仍要求显式
`$jl-*` 调用，避免普通任务自动进入重流程。

在完整工作流中：

- 默认使用多代理执行；需求明确、影响局部且风险较低的简单修改由当前任务
  直接完成。
- 任务复杂度主要依据耦合、未知量、契约与运行风险、可逆性和验证范围判断；
  预计或实际 Diff、文件数量和 Review 工作量也参与判断，但权重较低。
- 全新功能开发默认采用 TDD；调整现有功能、接口或页面，以及缺陷修复、兼容
  和重构，默认不走 TDD。两种情况都使用 `jl-lean-tests` 控制测试信号，避免
  无意义回归、精确文案和纯覆盖率测试膨胀。
- Worktree 按隔离需要自动选择；普通任务使用适当的现有分支或功能分支，只在
  并发实施需要隔离、用户明确指定或仓库状态无法安全处理时使用或询问。
- 当前任务负责统筹、分发、Review 和验收；所有文档判断与同步统一交给
  `jl-doc-steward`，再由它按文档类型调用仓库内固定版本的专用 Skill。

## 自建 Skill

这些 Skill 由本仓库直接维护，可以根据实际使用反馈持续调整。

| Skill | 用途 |
| --- | --- |
| `jl-engineering-orchestra` | 手动启动先计划、再按执行口令实施和验收的工程工作流 |
| `jl-chatgpt-pro-conductor` | 本地 Codex 实施，网页版 ChatGPT Pro 统筹并最终 Review |
| `jl-lean-tests` | 只为真实故障和稳定契约编写精简测试 |
| `jl-clean-branches` | 扫描远程合并状态并安全清理分支和 Worktree |
| `jl-sync-skills` | 汇总上游变化并按用户选择更新同步 Skill |
| `jl-doc-steward` | 创建、同步、审查核心工程文档和 Agent 指令文档 |
| `jl-prompt-architect` | 设计、撰写和审查可直接使用的分层 AI 提示词与 Runtime 契约 |

## 上游同步 Skill

这些目录是完整上游 Skill 的生成副本。同步过程只执行清单声明的机械转换：
添加 `jl-` 前缀、改写已纳入仓库的 Skill 依赖，并生成 Codex UI 元数据。

| 本地 Skill | 上游 | 角色 |
| --- | --- | --- |
| `jl-brainstorming` | Superpowers `brainstorming` | 独立深度设计流程 |
| `jl-writing-plans` | Superpowers `writing-plans` | 独立详细计划流程 |
| `jl-executing-plans` | Superpowers `executing-plans` | 独立按计划执行 |
| `jl-test-driven-development` | Superpowers `test-driven-development` | 可选 TDD |
| `jl-using-git-worktrees` | Superpowers `using-git-worktrees` | 可选隔离 |
| `jl-requesting-code-review` | Superpowers `requesting-code-review` | 发起审查 |
| `jl-receiving-code-review` | Superpowers `receiving-code-review` | 处理反馈 |
| `jl-verification-before-completion` | Superpowers `verification-before-completion` | 完成验证 |
| `jl-readme-blueprint-generator` | GitHub Awesome Copilot `readme-blueprint-generator` | README |
| `jl-architecture-decision-records` | ECC `architecture-decision-records` | ADR |
| `jl-clean-ddd-hexagonal` | robust-skills `clean-ddd-hexagonal` | DDD、整洁架构与六边形架构 |
| `jl-subagent-driven-development` | Superpowers 同名 Skill | 结构化多代理实施 |
| `jl-finishing-a-development-branch` | Superpowers 同名 Skill | 分支收尾 |
| `jl-dispatching-parallel-agents` | Superpowers 同名 Skill | 独立任务并行分发 |

不要直接修改 `synced/`。需要长期定制时，新建自建 Skill；需要跟进上游时，
使用 `jl-sync-skills` 和同步脚本。

Orchestra 在聊天中完成轻量设计和 Plan，不强制调用会写入设计/计划文件并设置
额外确认门禁的完整 Superpowers 流程。需要深度设计或可持久化详细计划时，仍可
单独调用 `jl-brainstorming`、`jl-writing-plans` 等同步 Skill。

## 常用用法

所有组件都可以脱离完整工作流单独使用：

```text
$jl-brainstorming 把这个想法收敛成设计
$jl-lean-tests 为这次改动设计少而有效的测试
$jl-clean-branches 清理这个仓库已合并的分支和 Worktree
$jl-readme-blueprint-generator 更新 README
$jl-architecture-decision-records 记录这个架构决定
$jl-clean-ddd-hexagonal 设计或审查复杂业务后端的架构边界
$jl-doc-steward 同步这次代码改动影响的项目文档
$jl-prompt-architect 为这个 Agent 设计 system、tool 和 recovery 提示词
$jl-sync-skills 检查上游更新
```

`jl-clean-ddd-hexagonal` 适合复杂业务规则、长期维护、多个入口或外部适配器，
以及需要修复领域层反向依赖基础设施的后端。简单 CRUD、一次性原型或没有真实
业务不变量的项目不应使用完整架构。

`jl-doc-steward` 管理 README、ADR、API、架构、设计/RFC、CHANGELOG、
CONTRIBUTING/DEVELOPMENT、AGENTS.md 和 CLAUDE.md。README 和 ADR 分别复用
仓库内固定版本的专用 Skill，其余文档按实际代码和配置取证后更新。

## 仓库结构

```text
my-skills/
├── skills/                 # 自建、可直接维护的 Skill
├── synced/                 # 由同步脚本生成的上游完整副本
├── licenses/               # 第三方许可证副本
├── scripts/install.py      # 安装或更新全局 Skill 独立副本
├── scripts/sync_skills.py  # 检查和重新生成同步 Skill
├── sources.yaml            # 来源、版本、哈希和转换清单
└── THIRD_PARTY_NOTICES.md  # 第三方归属说明
```

## 同步上游

先检查全部来源：

```bash
python3 scripts/sync_skills.py check --json
```

`jl-sync-skills` 会解释提交变化、文件迁移、行为变化和兼容性影响，再让用户选择
同步全部、部分或跳过。选定后，底层脚本按名称更新：

```bash
python3 scripts/sync_skills.py apply jl-brainstorming
```

脚本发现同步目录存在人工改动时会拒绝覆盖。同步只更新工作树和
[`sources.yaml`](sources.yaml)，不会自动提交、打标签或推送。

## 第三方来源

- [obra/superpowers](https://github.com/obra/superpowers)
- [github/awesome-copilot](https://github.com/github/awesome-copilot)
- [affaan-m/ECC](https://github.com/affaan-m/ECC)
- [ccheney/robust-skills](https://github.com/ccheney/robust-skills)

许可证和归属说明见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。

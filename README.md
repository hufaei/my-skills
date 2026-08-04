# my-skills

JL 的个人 Codex Skill 仓库。这里同时保存自建 Skill 和经过来源记录的上游
Skill 完整副本；克隆仓库并运行安装脚本后，即可在 Codex 中使用统一的
`jl-*` 名称。

仓库是本机安装内容的唯一来源：`skills/` 可以直接维护，`synced/` 只能通过
同步脚本从固定上游重新生成。当前包含 20 个 Skill，其中 6 个自建、14 个
上游同步。

## 特点

- **开箱即用：** 上游 Skill 已完整保存在仓库中，安装不依赖额外 Skill 仓库。
- **统一命名：** 所有 Skill 使用 `jl-` 前缀，避免与其他本机 Skill 重名。
- **按需调用：** 完整工程工作流不会套在每个小任务上；TDD 和 Worktree 也由
  用户决定是否采用。
- **可追溯同步：** 上游地址、源路径、固定提交、内容 SHA-256、许可证和机械
  转换规则记录在 [`sources.yaml`](sources.yaml)。
- **安全安装：** 安装脚本只创建软链接，不覆盖已有目录或指向其他位置的链接。

## 安装

### 让 Codex 安装

在新的 Codex 任务中说：

```text
安装 https://github.com/hufaei/my-skills，并按照仓库 README 创建本机 Skill 链接。
```

### 手动安装

将仓库克隆到一个不会移动的目录，然后在仓库根目录运行：

```bash
python3 scripts/install.py
```

安装脚本把 `skills/` 和 `synced/` 下的每个 `jl-*` 目录软链接到
`$CODEX_HOME/skills/`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills/`。
可以先预览操作：

```bash
python3 scripts/install.py --dry-run
```

安装后新开一个 Codex 任务，让 Skill 清单重新加载。软链接只是一条本机入口，
完整内容仍保存在这个仓库中；移动或删除仓库会让链接失效。

### 更新本机内容

已有软链接会直接读取仓库中的最新内容。拉取更新后，只需在新增了 Skill 时
重新运行安装脚本，为新目录补建链接：

```bash
git pull --ff-only
python3 scripts/install.py
```

## 调用策略

完整工作流和大多数组件只在显式选择或使用 `$jl-*` 调用时加载：

```text
$jl-engineering-orchestra <需求与验收标准>
```

`jl-clean-branches` 和 `jl-sync-skills` 还支持明确的自然语言请求，例如“清理已
合并分支”或“检查 Skill 上游更新”。同步过来的 Skill 均通过 Codex UI 元数据
禁止隐式调用。

在完整工作流中：

- 是否采用 TDD 由用户决定；需要时使用 `jl-lean-tests` 控制测试信号，避免
  无意义回归、精确文案和纯覆盖率测试膨胀。
- 是否创建 Worktree 由用户决定；不创建时就在当前仓库使用普通功能分支。
- 当前任务负责统筹、分发、Review 和验收，实施任务可以按需交给多个代理或
  会话。

## 自建 Skill

这些 Skill 由本仓库直接维护，可以根据实际使用反馈持续调整。

| Skill | 用途 |
| --- | --- |
| `jl-engineering-orchestra` | 手动启动完整工程设计、实施、审查和验收工作流 |
| `jl-chatgpt-pro-conductor` | 本地 Codex 实施，网页版 ChatGPT Pro 统筹并最终 Review |
| `jl-lean-tests` | 只为真实故障和稳定契约编写精简测试 |
| `jl-clean-branches` | 扫描远程合并状态并安全清理分支和 Worktree |
| `jl-sync-skills` | 汇总上游变化并按用户选择更新同步 Skill |
| `jl-doc-steward` | 创建、同步、审查核心工程文档和 Agent 指令文档 |

## 上游同步 Skill

这些目录是完整上游 Skill 的生成副本。同步过程只执行清单声明的机械转换：
添加 `jl-` 前缀、改写已纳入仓库的 Skill 依赖，并生成 Codex UI 元数据。

| 本地 Skill | 上游 | 角色 |
| --- | --- | --- |
| `jl-brainstorming` | Superpowers `brainstorming` | 设计 |
| `jl-writing-plans` | Superpowers `writing-plans` | 计划 |
| `jl-executing-plans` | Superpowers `executing-plans` | 执行 |
| `jl-test-driven-development` | Superpowers `test-driven-development` | 可选 TDD |
| `jl-using-git-worktrees` | Superpowers `using-git-worktrees` | 可选隔离 |
| `jl-requesting-code-review` | Superpowers `requesting-code-review` | 发起审查 |
| `jl-receiving-code-review` | Superpowers `receiving-code-review` | 处理反馈 |
| `jl-verification-before-completion` | Superpowers `verification-before-completion` | 完成验证 |
| `jl-readme-blueprint-generator` | GitHub Awesome Copilot `readme-blueprint-generator` | README |
| `jl-architecture-decision-records` | ECC `architecture-decision-records` | ADR |
| `jl-clean-ddd-hexagonal` | robust-skills `clean-ddd-hexagonal` | DDD、整洁架构与六边形架构 |
| `jl-subagent-driven-development` | Superpowers 同名 Skill | 工作流依赖 |
| `jl-finishing-a-development-branch` | Superpowers 同名 Skill | 工作流依赖 |
| `jl-dispatching-parallel-agents` | Superpowers 同名 Skill | 工作流依赖 |

不要直接修改 `synced/`。需要长期定制时，新建自建 Skill；需要跟进上游时，
使用 `jl-sync-skills` 和同步脚本。

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
├── scripts/install.py      # 创建本机 Skill 软链接
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

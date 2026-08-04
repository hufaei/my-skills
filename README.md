# my-skills

JL 的个人 Codex Skill 仓库。仓库本身是唯一内容来源：自建 Skill 保存在
`skills/`，由上游生成的完整副本保存在 `synced/`，安装时统一链接到 Codex
的用户 Skill 目录。

## 一句话安装

在新的 Codex 任务中说：

```text
安装 https://github.com/hufaei/my-skills，并按照仓库 README 创建本机 Skill 链接。
```

也可以手动克隆到一个不会移动的目录，然后运行：

```bash
python3 scripts/install.py
```

脚本会把每个 `jl-*` 目录软链接到 `$CODEX_HOME/skills/`；未设置
`CODEX_HOME` 时使用 `~/.codex/skills/`。它不会覆盖已有目录或指向其他
位置的链接。安装后新开一个 Codex 任务，确保 Skill 清单重新加载。

软链接只是本机快捷入口，完整内容仍只有仓库里一份。移动或删除仓库会让
链接失效，重新运行安装脚本即可报告问题。

## 自建 Skill

这些 Skill 由本仓库直接维护，可以按个人使用反馈继续修改。

| Skill | 用途 |
| --- | --- |
| `jl-engineering-orchestra` | 手动启动完整工程设计、实施、审查和验收工作流 |
| `jl-chatgpt-pro-conductor` | 本地 Codex 实施，网页版 ChatGPT Pro 统筹并最终 Review |
| `jl-lean-tests` | 只为真实故障和稳定契约编写精简测试 |
| `jl-clean-branches` | 扫描远程合并状态并安全清理分支和 Worktree |
| `jl-sync-skills` | 汇总上游变化并按用户选择更新同步 Skill |

## 上游同步 Skill

这些目录是完整上游 Skill 的生成副本，只保留机械转换：添加 `jl-` 前缀、
把已纳入仓库的 Skill 依赖改为 `jl-*`，并生成默认禁止隐式调用的 Codex UI
元数据。不要直接修改 `synced/`；使用 `jl-sync-skills` 更新。

| 本地 Skill | 上游 | 角色 |
| --- | --- | --- |
| `jl-brainstorming` | Superpowers `brainstorming` | 主要能力 |
| `jl-writing-plans` | Superpowers `writing-plans` | 主要能力 |
| `jl-executing-plans` | Superpowers `executing-plans` | 主要能力 |
| `jl-test-driven-development` | Superpowers `test-driven-development` | 可选 TDD |
| `jl-using-git-worktrees` | Superpowers `using-git-worktrees` | 可选隔离 |
| `jl-requesting-code-review` | Superpowers `requesting-code-review` | 发起审查 |
| `jl-receiving-code-review` | Superpowers `receiving-code-review` | 处理反馈 |
| `jl-verification-before-completion` | Superpowers `verification-before-completion` | 完成验证 |
| `jl-readme-blueprint-generator` | GitHub Awesome Copilot `readme-blueprint-generator` | README |
| `jl-architecture-decision-records` | ECC `architecture-decision-records` | ADR |
| `jl-subagent-driven-development` | Superpowers 同名 Skill | 工作流依赖 |
| `jl-finishing-a-development-branch` | Superpowers 同名 Skill | 工作流依赖 |
| `jl-dispatching-parallel-agents` | Superpowers 同名 Skill | 工作流依赖 |

精确源地址、源路径、提交、生成内容 SHA-256 和转换规则记录在
[`sources.yaml`](sources.yaml)。该文件使用 JSON 语法；JSON 是合法 YAML，
同步脚本因此可以只依赖 Python 标准库。

## 使用

完整工作流不会自动套在每个开发请求上，必须显式调用：

```text
$jl-engineering-orchestra <需求与验收标准>
```

也可以独立使用组件：

```text
$jl-lean-tests 为这次改动设计少而有效的测试
$jl-clean-branches 清理这个仓库已合并的分支和 Worktree
$jl-readme-blueprint-generator 更新 README
$jl-architecture-decision-records 记录这个架构决定
$jl-sync-skills 检查上游更新
```

## 同步上游

`jl-sync-skills` 会先检查并解释变化，再让用户选择同步全部、部分或跳过。
底层固定操作由脚本完成：

```bash
python3 scripts/sync_skills.py check --json
python3 scripts/sync_skills.py apply jl-brainstorming
```

同步目录记录生成内容的 SHA-256。脚本发现人工修改时会拒绝覆盖；需要长期
定制时，应创建新的自建 Skill，而不是给同步副本维护隐藏补丁。同步不会
自动提交、打标签或推送。

## 第三方来源

- [obra/superpowers](https://github.com/obra/superpowers)
- [github/awesome-copilot](https://github.com/github/awesome-copilot)
- [affaan-m/ECC](https://github.com/affaan-m/ECC)

许可证和归属说明见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。

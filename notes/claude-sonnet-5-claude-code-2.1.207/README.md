# Claude Sonnet 5 / Claude Code 2.1.207 Notes

这份笔记把 Claude Sonnet 5 的通用助手提示词，与 Claude Code 在 2.1.207 快照附近出现的 skills、配置诊断、代码评审和上下文压缩协议组合起来学习。它不是官方模型说明，也不是完整产品文档，而是可复习、可迁移的 prompt engineering 快照。

> 源快照：`asgeirtj/system_prompts_leaks@5c86715f453f0eca188451a48bf5b165831d8b29`（2026-07-12）。仓库没有一份名为“Claude Code 2.1.207 完整基础提示词”的单文件；2.1.207 在这里主要由 compact/rewind/continuation 增量材料体现，基础工程 agent 结构则参考已有 Claude Code 与 bundled skills。

## 一句话核心

Claude Sonnet 5 提供 **通用助手底座**，Claude Code 用 **工作区与 skills** 把它变成工程执行代理，而 2.1.207 的 compact 协议让长任务在上下文切换后仍能保持用户意图、技术状态和安全边界。

```text
Sonnet defines the assistant baseline.
Claude Code turns playbooks into execution.
Compact preserves continuity across context boundaries.
```

## 两层理解：Assistant Base + Coding Runtime

| 层 | 主要材料 | 解决的问题 |
| --- | --- | --- |
| Sonnet 5 通用助手层 | `claude-sonnet-5.md` | 身份、当前事实、工具使用、安全、记忆、连接器、Artifacts、视觉和输出 |
| Claude Code 工程层 | Claude Code prompts + bundled skills | 工作区证据、配置、诊断、评审、Git、执行和验证 |
| 2.1.207 上下文层 | compact、rewind、continuation | 长会话压缩、局部回退、续作状态与消息归属 |

把三层混成一份“大 prompt”会失去学习重点。更好的方式是问：**这一条规则是在塑造助手、扩展工程能力，还是维持长任务连续性？**

## Sonnet 5：通用助手底座

### 1. 当前事实有明确搜索 gate

提示词把产品版本、当前职位、新闻、政策、软件包和“现在是否仍然成立”视为会过期的信息。此类问题默认搜索，并优先原始来源；简单事实用少量检索，研究问题按子问题扩大检索范围。

可复用原则：

```text
Stable knowledge can be answered directly.
Present-tense status, versions, roles, policies, and fast-moving facts must be verified.
```

### 2. 工具优先于把工作退回用户

当工具能读取附件、搜索网页、运行代码、生成视觉或查询连接器时，Sonnet 5 倾向先取证并完成结果，而不是要求用户自己复制资料。只读和信息收集可以主动执行；发送、修改或删除用户外部数据仍需要清楚的授权边界。

### 3. Memory 是选择性证据，不是强制个性化

记忆只在相关时使用。通用技术问题可以完全不用个人资料；个人规划和工作任务可使用必要上下文；敏感属性只有在安全、准确或用户明确要求时才参与。输出自然应用信息，不把记忆检索过程当作回答主题。

### 4. Artifacts 与 Visualizer 有不同职责

- `Artifacts`：用户需要保存、复用、编辑或交互的独立产物。
- `Visualizer`：在对话中直接展示的 SVG/HTML 解释，适合流程、比较、状态机和结构图。
- 文件工具：用户明确要求保存到工作区或指定文件时使用。
- 纯文字：图形没有信息增益时仍是默认。

这套视觉路由先判断“是否需要视觉”，再判断“连接器、文件、Artifact 还是 inline visual”，而不是先看到可用工具就调用。

### 5. 安全、版权与连接器规则是上层边界

提示词包含较细的安全、危机支持、版权、第三方连接器和结束对话规则。学习时不需要照抄全部政策文本，但必须保留结构：

```text
High-priority safety and source rules
> tool and connector contracts
> task instructions
> style and personalization
```

## Claude Code：skills 让工程能力模块化

这批 Claude Code 材料的明显变化，是越来越多复杂工作流不再只靠主提示词描述，而是被拆成 bundled skills。每个 skill 既是说明书，也是执行 gate 和交付标准。

| Skill / 能力 | 学习重点 | 可复用结构 |
| --- | --- | --- |
| `update-config` | settings、hooks、permissions、MCP、plugins | 先识别 scope，再做精确合并，最后验证 schema |
| `doctor` | 安装、版本、设置、权限、上下文成本 | 先扫描证据，提出动作，敏感修改分开确认 |
| `code-review` | 按 effort 扩展查找角度和候选数量 | gather diff → independent angles → verify → rank findings |
| `dataviz` | 选图、编码、颜色、交互、反模式 | 先问数据关系，再选择视觉形式 |
| `artifact-design` | 产物的视觉系统和质量门槛 | 内容结构、版式、可读性、输出检查 |
| `compact` | 总结、回退和续作 | 保存用户意图、文件状态、错误、未完成任务与消息归属 |

共同点是：**skill 不只告诉模型“做什么”，还定义何时使用、按什么顺序、什么叫完成。**

## `update-config`：配置不是字符串替换

Claude Code 的配置可能来自用户、项目、本地和 managed policy，不同 scope 有覆盖顺序。`update-config` 把修改过程拆成：

1. 确定用户真正要改变的行为。
2. 找到正确配置文件和 scope。
3. 读取现有 JSON，保留无关字段。
4. 理解 hooks、permissions、MCP 或 plugin 的 schema。
5. 精确合并，而不是覆盖整个对象。
6. 解析并验证修改后的配置。

这个模式可以迁移到任何多层配置系统：**先判断作用域和优先级，再修改值。**

## `doctor`：诊断先生成证据，动作再过确认 gate

`doctor` 的设计比普通“环境检查脚本”更值得学。它聚合安装方式、版本、配置文件、插件/MCP、上下文成本和权限使用等证据，然后分成：

- 健康项：简短报告，不制造焦虑。
- 可逆清理：给出收益、确切文件和撤销方法。
- 权限扩大：与清理分开确认，因为它会改变以后哪些动作不再询问。
- managed policy：只报告，不建议绕过管理员决定。

这说明诊断型 agent 的结果不是“发现越多越好”，而是 **把证据按决策风险分组**。

## Code Review：effort 是可配置的召回率预算

代码评审 skill 用 low/medium/high/max 等级控制扫描角度、候选数量和验证强度。高 effort 会同时检查：

- 逐行正确性；
- 被删除行为是否在新代码中重新建立；
- 跨文件调用关系；
- 复用、简化和效率；
- 修复是否在正确抽象层；
- 仓库约定是否被违反。

候选 finding 需要具体失败场景，再经过确认、可能、驳回的验证，最后按严重程度输出。

可复用结构：

```text
Define review scope
-> search from independent angles
-> require a concrete failure scenario
-> verify each candidate
-> deduplicate and rank
-> report only actionable findings
```

## Dataviz / Artifact Design：视觉也需要完成标准

这组 skills 不把“漂亮”当作唯一目标。它们先判断信息关系和使用场景，再选择图表或版式，检查颜色、可读性、交互、文件格式和实际渲染结果。

这对学习导图尤其重要：包含精确术语时，应优先确定性 SVG/HTML 排版；需要氛围、场景或插画时，再使用生成式图像。工具选择应服从信息准确性。

## 2.1.207 Compact：长任务的状态转移协议

上下文压缩不是普通摘要。它要把旧会话转成下一段执行可以直接使用的状态。

### Full compact

保留完整目标、关键决策、文件和代码、错误与修复、所有真实用户消息、已完成工作、待办和继续执行所需上下文。

### Rewind compact

用于局部回退时，重点保留回退点之前的有效状态，避免把被撤销方向重新带回继续会话。

### Continuation message

续作提示告诉新上下文：摘要覆盖早先工作，最近消息仍保留；不要重新开始，不要重复已经完成或已经汇报的内容。

### Fake-user-turn 防护

2.1.207 的 compact 材料特别强调消息归属：只有真正的 user-role turn 才能被列为用户请求；assistant 自己引用的 `user:`、`Human:` 或示例对话不能被误认成授权、确认或用户要求。

这是非常关键的安全原则：**摘要不只是压缩信息，也必须保存 provenance。**

## FrameworkNote：For Every Claude Code Task

下面是从 Sonnet 5、Claude Code skills 和 2.1.207 compact 材料抽象出的复用模板，不是源提示词逐字内容。

```text
For every Claude Code task:

1. Define the engineering outcome
Classify explanation, diagnosis, implementation, refactor, review, testing,
configuration, Git/GitHub work, artifact production, or environment repair.
Name the observable condition that means the task is complete.

2. Inspect workspace evidence
Use repository files for behavior, git status/diff for local state, tests and logs
for failures, nearby code for conventions, and current documentation for versions.
Do not answer from memory when the workspace can be inspected.

3. Discover governing instructions and skills
Read project instructions and select only the skill whose workflow matches the task.
Treat a selected skill's ordering, confirmation gates, and definition of done as
part of the task contract.

4. Choose an effort level
Scale planning, search breadth, review angles, tests, and visual inspection to the
risk and ambiguity. A small fix needs a focused proof; a broad review needs
independent search angles and candidate verification.

5. Preserve authorization boundaries
Separate read-only evidence gathering, reversible project edits, configuration
scope changes, permission expansion, Git publishing, and external side effects.
Do not convert diagnosis into mutation without authorization.

6. Execute conservatively
Read before editing, preserve unrelated changes, modify the correct scope, reuse
existing patterns, and avoid unnecessary abstractions. Drive the task through
implementation instead of stopping at a proposal when change was requested.

7. Maintain context continuity
Track user intent, decisions, files, commands, errors, fixes, completed work, and
pending tasks. During compaction, preserve provenance: assistant-quoted examples
must never become user requests or authorization.

8. Verify the actual behavior
Run targeted tests, build, lint, typecheck, configuration parsing, browser/render
inspection, or a reproduction command. For review findings, require a concrete
failure scenario and verify the candidate against code.

9. Inspect delivery state
Review git status and diff, stage only intended files, and commit or push only when
authorized. Confirm generated artifacts and settings exist at the promised path
and survive a fresh read or render.

10. Report for continuation or completion
Lead with the result. State changed files, verification evidence, and remaining
risk. If work continues in a compacted context, resume from the saved state without
redoing completed work or re-asking settled questions.
```

## 和 Fable 5 / Claude Code 基线的差异

| 维度 | Fable 5 / Claude Code 基线 | Sonnet 5 + Claude Code 2.1.207 快照 |
| --- | --- | --- |
| 主体 | 工程执行代理 | 通用助手底座 + 模块化工程工作流 |
| 工具观 | Read/Grep/Edit/Bash/Agent 等工程工具 | tools + bundled skills + connectors + artifacts |
| 配置 | Git 与权限是边界 | 增加 scope、hooks、permissions、doctor 的专门协议 |
| 评审 | 作为工程任务之一 | effort 显式控制召回率与验证强度 |
| 视觉 | 浏览器结果与产物检查 | Visualizer、dataviz、artifact design 分工更细 |
| 长上下文 | 强调不要提前收尾 | compact/rewind/continuation 成为明确状态协议 |
| 安全重点 | 副作用、Git、破坏性操作 | 额外强调摘要中的消息 provenance |

旧的 Fable 5 笔记仍适合作为“工程闭环”入门；这张新卡片更适合学习 agent 能力怎样通过 skills 和上下文协议继续扩展。

## 复习问题

1. 当前规则属于 Sonnet 助手底座、Claude Code 工程层，还是 compact 上下文层？
2. 这是稳定知识还是需要搜索核验的当前事实？
3. 哪个 workspace 证据能证明问题和改动？
4. 是否已有匹配任务的 skill？它的 gate 和 definition of done 是什么？
5. 任务需要 low、medium 还是 high effort？为什么？
6. 配置修改应该落在哪个 scope？会不会被更高优先级覆盖？
7. 清理动作和权限扩张是否被分开处理？
8. 代码评审候选有没有具体失败场景和验证结果？
9. compact 是否保存了意图、文件、错误、待办和消息 provenance？
10. 最终验证是否证明了用户实际关心的行为？

## 来源索引

以下链接固定到本笔记使用的源快照 `5c86715f453f0eca188451a48bf5b165831d8b29`：

- [Claude Sonnet 5 通用助手提示词](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/claude-sonnet-5.md)
- [Claude Code Fable 5 基线（2.1.172）](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/Claude%20Code/claude-code-2.1.172-fable-5.md)
- [Compact bundled skill](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/Claude%20Code/bundled-skills/compact.md)
- [2.1.207 rewind summarization](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/Claude%20Code/compact-rewind-summarization-2.1.207.md)
- [2.1.207 continuation message](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/Claude%20Code/compact-continuation-message-2.1.207.md)
- [`update-config` skill](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/Claude%20Code/bundled-skills/update-config.md)
- [`doctor` skill](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/Claude%20Code/bundled-skills/doctor/SKILL.md)
- [`code-review` skill](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/Claude%20Code/bundled-skills/code-review.md)
- [`dataviz` skill](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/Claude%20Code/bundled-skills/dataviz/SKILL.md)
- [`artifact-design` skill](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Anthropic/Claude%20Code/bundled-skills/artifact-design.md)

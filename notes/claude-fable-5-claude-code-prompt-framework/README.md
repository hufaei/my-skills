# Claude Fable 5 / Claude Code Prompt Framework Notes

这份笔记用于复习 Claude Fable 5 风格的 Claude Code 系统提示词。它不是官方模型说明，而是基于本地提示词材料压缩出的 prompt engineering 学习模板。

## 一句话核心

GPT-5.5 风格像通用请求路由器；Fable 5 / Claude Code 风格像代码工作区执行代理。它的重点不是回答得像助手，而是把一次工程请求推进到查证、修改、验证和交付。

## 精华版：For Every Claude Code Request

```text
For every Claude Code request:

1. Classify the engineering task
Identify whether the user wants explanation, debugging, implementation, refactor, review, test, Git/GitHub work, tool setup, or repository exploration.

2. Identify the workspace source of truth
Use the right evidence source:
- code behavior -> repository files
- current local state -> git status / git diff
- failures -> test, build, lint, logs, reproduction output
- architecture -> existing patterns and nearby files
- package/API facts -> local docs or current external docs
- UI behavior -> browser/computer observation
Do not answer from memory when the repo or runtime can be inspected.

3. Apply agent boundaries first
Before edits or side effects, check authorization, destructive operations, secrets, private data, file deletion/overwrite risk, publishing/sending/pushing, permission changes, and tool permission failures.
These boundaries override convenience and user-style preference.

4. Decide whether to ask or proceed
Ask only when the missing decision is genuinely the user's or creates material risk.
If the action is reversible and follows from the request, proceed.
Do not stop at "I can do X" when the user asked you to do X.

5. Plan and track proportional to risk
For non-trivial or multi-step coding work, maintain a task list.
For architectural or multi-file changes with real alternatives, plan before editing.
For simple fixes, keep the plan implicit and move.

6. Route tools and agents narrowly
Use the smallest tool that can prove or change the thing:
- Read -> known file
- Grep/Glob/search -> locate symbols/files
- Edit -> precise file change after reading
- Bash -> tests, builds, scripts, git, package commands
- Agent/Explore -> broad repo exploration or parallel independent work
- Skill/slash command -> only when explicitly available
Do not duplicate work already delegated to an agent.

7. Edit conservatively
Read before editing.
Prefer existing files over new files.
Match local style, naming, abstractions, and comment density.
Do not create helper abstractions for one-off work.
Keep changes scoped to the user's request.

8. Verify before claiming success
Run the smallest meaningful verification: targeted test, build, typecheck, lint, reproduction command, browser check, or git diff/status review.
If verification fails, report it and continue fixing when completion is expected.

9. Handle Git and final output
Commit or push only when the user asks.
If committing, inspect status/diff, stage only intended files, and never amend unless explicitly requested.
Final answer starts with the result, then states changed files, verification, and remaining risk.
Do not expose hidden reasoning, raw tool arguments, or irrelevant logs.
```

## 关键点

1. 控制对象变了：Fable 5 / Claude Code 面向代码工作区，不是泛聊天场景。
2. 自治更强：有足够信息就继续做，可逆动作直接推进，真正阻塞或高风险才问用户。
3. 证据更工程化：优先看 repo 文件、git diff/status、测试、构建、日志和浏览器结果。
4. 工具是运行协议：Read、Grep、Edit、Bash、Agent、Plan、Skill 都有明确适用边界。
5. 修改要闭环：读文件、改文件、验证、检查 diff、再汇报，而不是停在建议。
6. Git 是独立边界：commit 和 push 只在用户明确要求时执行。
7. 多 agent 是扩展能力：适合广泛搜索、并行审查和大规模迁移，但不应代替主 agent 的最终判断。

## 和 GPT-5.5 框架的差异

| 维度 | GPT-5.5 风格 | Fable 5 / Claude Code 风格 |
| --- | --- | --- |
| 默认任务 | 任意用户请求 | 软件工程请求 |
| 第一判断 | 事实来源是什么 | 仓库里该查哪里、改哪里、怎么验证 |
| 证据源 | 文件、网页、图片、计算、记忆、浏览器 | repo、git、测试、日志、构建、浏览器、GitHub |
| 工具策略 | 最小必要工具 | 专用工程工具链和子 agent |
| 成功标准 | 给出有证据的回答 | 完成代码改动并验证 |
| 副作用边界 | 发送、删除、发布、付款、权限等 | 额外强调编辑、删除、commit、push、外部发布 |
| 输出形态 | 结果、证据、限制、下一步 | 改了什么、验证了什么、还有什么风险 |

压缩成一句话：

```text
GPT-5.5: route the request to the right source of truth.
Fable 5 / Claude Code: drive the engineering task through workspace evidence, edits, verification, and Git boundaries.
```

## Claude Code 系列提示词演进

### Opus 4.6：代码代理骨架成型

重点已经包括 Claude Code 身份、软件工程任务、任务列表、提问工具、搜索/读取/编辑工具、Git 提交规则和授权安全测试边界。这个阶段的核心是让模型不只是聊天，而是能在代码仓库里做事。

### Opus 4.8：运行时协议更清晰

提示词更像一份 CLI/agent runtime 手册：环境信息、上下文续作、工具说明、Agent 路由和计划模式被组织得更紧凑。这个阶段强调长上下文下继续推进，不要因为会话变长就提前收尾。

### Fable 5：自治执行和交付闭环加强

Fable 5 在 Claude Code 场景里的重点是更强的 agent 行为：能做就做，少问阻塞式问题；对可逆动作保持推进；对破坏性、外部发布、权限、Git 操作保持边界。它把“代码助手”进一步推向“工程执行代理”。

## 复习问题

1. 这个请求是不是工程任务？如果是，仓库里的 source of truth 是什么？
2. 需要解释、定位、修改、验证，还是 Git/GitHub 操作？
3. 这一步是否可逆？是否涉及删除、覆盖、提交、推送或外部发布？
4. 是否需要 task list、plan mode、subagent，还是直接查文件即可？
5. 改动前读过相关文件了吗？
6. 完成后用什么最小验证证明它真的好了？
7. 最终回答是否说清楚了改动、验证和剩余风险？

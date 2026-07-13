# GPT-5.5 Prompt Framework Notes

这份笔记用于复习 GPT-5.5 风格系统提示词的核心框架。它不是官方模型说明，而是一个可复用的 prompt engineering 压缩模板。

> 已按源快照 `asgeirtj/system_prompts_leaks@5c86715f453f0eca188451a48bf5b165831d8b29`（2026-07-12）复核。原有九步模板完整保留；新增内容用于说明它在当前 Codex runtime 中的位置。

## 一句话核心

先找到正确的 source of truth，再应用边界、选择最小工具、合并证据并输出可验证的答案。

## 精华版：For Every User Request

```text
For every user request:

1. Classify the task
Identify the user's goal, required inputs, expected output, and whether the request involves text, files, images, web, code, data, memory, or external actions.

2. Identify the source of truth
Use the right evidence source:
- uploaded/file content -> file retrieval
- latest/current facts -> web/search
- user preferences/context -> memory/context
- calculations/parsing -> code/computation
- visible UI/page state -> browser/computer observation
Do not substitute one source for another.

3. Apply high-priority boundaries
Before final output or any side-effectful action, check safety, privacy, copyright, permission, source authority, and capability limits.
Read-only tools may be used to gather evidence for this judgment.
These boundaries override user preference, persona, and convenience.

4. Decide whether to ask or proceed
Ask only if missing information blocks correct execution or creates material risk.
Otherwise make the narrowest reasonable assumption and continue.

5. Route tools narrowly
Use the smallest necessary tool.
For each tool, obey:
- use when
- do not use when
- preconditions
- post-call result handling

6. Handle side effects
Before sending, deleting, publishing, purchasing, changing permissions, or exposing private data, get explicit user confirmation unless already authorized.

7. Merge evidence
Separate observed facts, tool results, and model inference.
Do not invent unsupported capabilities or facts.
Mention uncertainty when it affects the user's decision.

8. Resolve conflicts
Priority:
system/safety/source-of-truth > tool/API contracts > developer/task rules > persona/style > user preference.

9. Produce final answer
Start with the result or recommendation.
Use the user's requested language and format.
Include only useful evidence, limitations, and next actions.
Do not expose hidden reasoning, raw tool arguments, or irrelevant logs.
```

## 当前快照里的位置

这份九步框架仍然适合作为通用请求路由器。当前 GPT-5.6 / Codex 材料没有推翻它，而是在它外面加上了更完整的工程 runtime：共享工作区、commentary/final 双通道、skills、自治执行、Git 现场保护和专用 artifact 工作流。

可以把两者理解成：

```text
GPT-5.5 = 一次请求的通用判断骨架
GPT-5.6 / Codex = 骨架 + 工作区 + skills + 工具运行时 + 持续交付
```

因此复习顺序建议是：先熟悉本页九步路由，再阅读 [GPT-5.6 / Codex Runtime](../gpt-5.6-codex-runtime/) 理解这些原则怎样进入完整 agent runtime。

## 复习问题

1. 这个请求的 source of truth 是什么？
2. 是否需要工具？如果需要，最小必要工具是什么？
3. 有没有安全、隐私、版权、权限或副作用边界？
4. 缺失信息是否真的阻塞执行？
5. 工具结果如何压缩成证据，而不是直接堆给用户？
6. 如果用户偏好和高优先级规则冲突，谁赢？

## 来源索引

以下链接固定到本笔记复核时使用的源快照 `5c86715f453f0eca188451a48bf5b165831d8b29`：

- [GPT-5.5 Codex 行为提示词](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/OpenAI/Codex/gpt-5.5.md)
- [GPT-5.5 Thinking](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/OpenAI/gpt-5.5-thinking.md)
- [GPT-5.5 Instant](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/OpenAI/gpt-5.5-instant.md)
- [GPT-5.5 API](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/OpenAI/gpt-5.5-api.md)

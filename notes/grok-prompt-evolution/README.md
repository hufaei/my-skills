# Grok Prompt Evolution Notes

这份笔记用于复习本地仓库里的 Grok 系列提示词演进。它不是官方模型说明，而是基于 `grok-3`、`grok-4`、`grok-4.1-beta`、`grok-4.2`、`grok-4.3-beta` 的 prompt engineering 学习整理。

> 已按源快照 `asgeirtj/system_prompts_leaks@5c86715f453f0eca188451a48bf5b165831d8b29`（2026-07-12）复核。本页保留版本演进作为理解工具注册方式的背景，但当前结论以该源快照为准。

## 一句话核心

Grok 的提示词演进主线不是“建立稳定推理链”或“建立工程执行闭环”，而是不断把产品能力塞进系统提示词：X 搜索、网页搜索、代码执行、图片生成/编辑、渲染组件、多 agent、远程沙箱和 skills。

所以它最值得学的是“产品型 AI 如何注册工具和输出组件”；不太值得照抄的是它的整体请求处理结构。

## 版本演进

### Grok 3：轻量产品能力清单

Grok 3 的 prompt 很短，重点是身份、X/web/文件/图片能力、记忆、DeepSearch/think mode、产品访问方式和实时信息判断。

它的问题在于：一边说 `no strict knowledge cutoff`，一边又说优先内部知识、必要时才搜索。这会削弱强制查证意识，模型容易凭印象回答当前事实。

### Grok 4：工具注册表膨胀

Grok 4 开始把工具协议写得很重，包括 XML 风格 function call、code execution、browse page、web search、X search、view image、citation、render。

这一步说明 Grok 想把自己做成强工具模型。优点是能力面广，缺点是工具很多但统一决策链不够清楚：它告诉模型“你有这些工具”，但没有像 GPT-5.5 那样稳定地规定“这个请求的 source of truth 是什么”。

### Grok 4.1 Beta：加硬 policy 壳

Grok 4.1 beta 把 `<policy>` 放到开头，强调犯罪、jailbreak、角色扮演中的犯罪细节、成人/冒犯内容边界等。

这说明它开始补高优先级边界。但边界比较粗，后面又混入争议话题、政治表达、搜索多方来源、数学格式等指令，整体仍然不像一条清晰的执行链。

### Grok 4.2：多 agent 团队实验

Grok 4.2 把 Grok 设定为 team leader，并给它 `chatroom_send` 和 `wait` 来和 Harper、Benjamin、Lucas 协作。

这个版本很有实验感：它试图用多个 agent 提升复杂任务质量。但如果没有清楚的验证、去重和裁决协议，多 agent 可能只是增加上下文和协调成本。

### Grok 4.3 Beta：远程沙箱和 skills 化

Grok 4.3 beta 去掉了 4.2 的 team leader 设定，改成 remote sandbox runtime。它声明 sandbox 不是用户本地电脑，并提供 web/X/image/file/bash/render/skills。

这一步明显往 agent runtime 靠近：能读写文件、跑 bash、处理图片、渲染文件、调用文档类 skills。但它仍然缺少 Claude Code 那种清晰的任务列表、测试验证、Git 边界和完成标准。

## 为什么表现可能不稳

Grok 的问题不是能力少，而是能力太多但调度骨架偏松。

GPT-5.5 的核心是 source-of-truth 路由：先判断事实从哪里来，再调用工具。Claude Code / Fable 5 的核心是工程闭环：查仓库、改文件、验证、处理 Git 边界。Grok 的核心更像产品能力注册：X、web、image、code、render、sandbox、skills 全塞进来。

这会导致三个问题：

1. 对当前事实，搜索触发不够硬。
2. 对复杂工具任务，工具 schema 很详细，但“先后顺序”和“完成标准”不够强。
3. 对多 agent 和争议话题，容易增加协调噪声和风格摇摆。

## 和 GPT-5.5、Claude/Fable 的差异

| 维度 | GPT-5.5 | Claude Code / Fable 5 | Grok |
| --- | --- | --- | --- |
| 核心骨架 | source-of-truth 路由 | 工程执行闭环 | 产品能力和工具注册 |
| 默认任务 | 任意请求 | 软件工程任务 | X/web/多模态/产品型任务 |
| 工具观 | 最小必要工具 | 代码工作区工具链 | 大量工具 schema 和 render 组件 |
| 成功标准 | 有证据的回答 | 改动、验证、交付 | 走对工具并渲染结果 |
| 主要风险 | 过度保守或问太多 | 过度执行或副作用 | 工具多但决策链松 |

压缩成一句话：

```text
GPT-5.5 teaches source routing.
Claude Code / Fable 5 teaches task completion.
Grok teaches product capability registration.
```

## 值得借鉴什么

可以借鉴：

- X/web 搜索作为一等工具能力。
- 工具 schema 写清楚参数、限制和返回方式。
- render components 把引用、图片、文件输出做成 UI 协议。
- 图片生成、图片编辑、文件渲染和文档 skills 的产品化组织方式。
- 远程 sandbox 和用户本地环境之间的边界说明。

不建议照抄：

- `no strict knowledge cutoff` 这种弱化查证边界的写法。
- 只堆工具列表、不写统一请求处理链。
- 多 agent 只有协作通道，没有验证和裁决协议。
- 代码/文件任务只有 read/edit/write/bash，没有测试、Git 和完成标准。

## 可复用模板：For Every Product-Tool Prompt

这不是 Grok 原提示词的逐字模板，而是把其中最值得借鉴的“产品能力注册”压缩成可复用结构。

```text
For every product-tool prompt:

1. Classify the task before selecting a capability.
2. Map current facts to search, social context to the relevant network source,
   code or calculation to execution, and visual output to image/render tools.
3. Keep every tool schema narrow: purpose, required parameters, constraints,
   return shape, and post-call handling.
4. Define an execution order when several tools are needed.
5. Separate sandbox state from the user's local machine and external accounts.
6. Add explicit verification and completion criteria around file/code actions.
7. Treat multi-agent output as candidates that need deduplication and adjudication.
8. Render only the result type that helps the user inspect or reuse the answer.
```

## 复习问题

1. 当前请求真正需要的是 X、web、code、image、render 还是文件能力？
2. 工具 schema 是否说明了用途、参数、限制、返回值和调用后处理？
3. 多个工具之间有没有明确的先后顺序和完成标准？
4. 当前事实的搜索 gate 是否足够硬，还是模型可能凭印象作答？
5. remote sandbox 与用户本地机器、账号和文件的边界是否清楚？
6. 多 agent 结果由谁去重、验证和裁决？
7. 文件/代码任务有没有补上测试、Git 和交付闭环？
8. render 组件是在增加可检查性，还是只是展示产品能力？

## 来源索引

以下链接固定到本笔记使用的源快照 `5c86715f453f0eca188451a48bf5b165831d8b29`：

- [Grok 3](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/xAI/grok-3.md)
- [Grok 4](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/xAI/grok-4.md)
- [Grok 4.1 Beta](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/xAI/grok-4.1-beta.md)
- [Grok 4.2](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/xAI/grok-4.2.md)
- [Grok 4.3 Beta](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/xAI/grok-4.3-beta.md)

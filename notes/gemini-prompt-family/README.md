# Gemini Prompt Family Notes

这份笔记用于复习本地仓库里的 Gemini 3 系列与 Nano Banana 2 API。它不是官方模型说明，而是基于 `gemini-3.1-pro`、`gemini-3.5-flash`、`nano-banana-2-api` 的 prompt engineering 学习整理。

> 已按源快照 `asgeirtj/system_prompts_leaks@5c86715f453f0eca188451a48bf5b165831d8b29`（2026-07-12）复核。正文的三层分工、可复用模板和复习问题完整保留；来源统一改为可在线审查的固定链接。

## 一句话核心

Gemini 这一组最值得学的不是“怎么写一个聊天人格”，而是 **Web 助手如何把一次用户请求路由成文本、图片、交互组件或图像生成任务**。

压缩成一句话：

```text
Gemini Pro teaches orchestration gates.
Gemini Flash teaches Web UI rendering.
Nano Banana teaches image tool contracts.
```

## 三者分工

| 对象 | 角色 | 重点 |
| --- | --- | --- |
| `gemini-3.1-pro` | 完整总控 prompt | 身份、能力隔离、追问策略、用户数据 gate、视觉 gate、Widget gate、版权边界 |
| `gemini-3.5-flash` | Web UI 执行 prompt | Markdown 默认、图片检索、LMDX 组件、工作流、组件语法安全 |
| `nano-banana-2-api` | 图像工具/API 契约 | `image_gen`、`display`、`search`、`image_search` 的参数和调用边界 |

它们不是完全无关的三套东西。更合理的理解是：

```text
Gemini 3.1 Pro = 负责判断和路由
Gemini 3.5 Flash = 负责把回答组织成 Web UI
Nano Banana 2 API = 负责执行图像生成/编辑和展示
```

## Gemini 3.1 Pro：总控架构

`gemini-3.1-pro` 的提示词像一份完整的 Web 助手架构稿。它先定义模型怎样说话，再定义能力信息什么时候能用，然后进入追问、个性化、视觉、交互组件和版权边界。

### 1. 身份和语气层

它不是只写一句 `helpful assistant`，而是把语气冲突写清楚：

- 可以共情，但要以事实纠错。
- 可以贴近用户语气，但不能装作有人类经历。
- 回答要清楚直接，不要僵硬说教。
- LaTeX 只用于正式数学/科学，不用于普通文本装饰。

这个层解决的是“模型像谁说话”。

### 2. 能力说明隔离层

它有一块能力说明，包含 Core Model、付费层、图片、视频、音乐等能力。但关键点是：这块只用于回答“你能做什么”这类能力问题，不能影响普通任务。

这是一个很值得复用的 prompt engineering 技巧。能力说明如果不隔离，模型容易在普通请求里过度展示产品功能。

可复用模板：

```text
Capability information is only for capability questions.
Do not use it to execute unrelated user requests or influence ordinary responses.
```

### 3. 追问策略层

Gemini 把请求分成两类：

- `STRICT COMPLETION`：有明确答案、格式或完成标准的任务，直接完成，不追加菜单式问题。
- `EXPERT GUIDE`：宽泛、模糊或咨询型任务，先给有用回答，再最多问一个能推进问题。

这个设计的重点是：默认完成任务，不滥用澄清问题。

### 4. 用户数据 Gate

这是 3.1 Pro 最有价值的一层。它不是“有用户数据就用”，而是要求用户数据必须先通过 gate：

1. 用户数据是否真的能提升回答质量。
2. 从空上下文开始，只选必要数据。
3. 用户纠正历史优先于旧资料。
4. 不跨领域转移偏好。
5. 不把多个用户资料强行组合成过拟合画像。
6. 不推断或暴露敏感数据。
7. 把选中的用户信息自然融入回答，不说“Based on you...”。

这层的核心原则：

```text
User data is evidence, not decoration.
Use it only when it materially improves the answer.
```

例子：

```text
用户：什么是梯度下降？
结果：不使用用户资料，直接解释概念。

用户：帮我设计一个适合我的机器学习学习路线。
结果：可以使用用户目标、基础、时间偏好，但不能强行加入无关职业、地点或敏感信息。
```

### 5. 视觉 Gate

3.1 Pro 的视觉逻辑不是“回答更好看就配图”，而是：

```text
只有用户明确想学习/理解概念，并且图像能带来信息增量，才触发图像/图解。
```

适合触发：

- 细胞结构
- 有丝分裂阶段
- 机器学习流程
- 物理系统

不适合触发：

- 写邮件
- 生成代码
- 写作文
- 只是抽象建议

这个 gate 的价值是控制多模态滥用。

### 6. Widget Gate

`Interactive Widget Architect` 是 3.1 Pro 最像产品设计的部分。它把模型变成一个 Visual Tutor：能用纯文本解释，也能在合适时生成交互式 JSON Widget。

判断链路是：

```text
先做安全检查
-> 判断交互是否增强理解
-> 排除文本优先场景
-> 选择 Widget archetype
-> 生成 LMDX GenerateWidget
```

适合 Widget 的场景：

- 参数变化会影响结果，例如抛物运动、复利、函数图像。
- 系统过程可探索，例如生态系统、排队模型。
- 数据可筛选排序，例如国家 GDP、元素周期表。

不适合 Widget 的场景：

- 定义、事实、术语。
- 列表。
- 单次计算。
- 纯创作图片或改图。
- 依赖上传文件但无法完整提取内容。

关键学习点：

```text
Do not choose tools first.
Classify whether interactivity helps first.
```

### 7. 版权边界

3.1 Pro 的版权边界很硬：不能输出大段受版权保护文本，不能长篇翻译、改写或逐行复述；应该总结、分析或讨论。用户提供的可见内容可以处理，但范围不能外推。

这层说明：版权/安全边界比用户偏好和回答风格优先级更高。

## Gemini 3.5 Flash：Web UI 执行模板

`gemini-3.5-flash` 不是完全不同的架构，而是把 3.1 Pro 的很多理念压缩成一个更偏 Web 产品执行的 prompt。

它保留了：

- 能力说明隔离。
- 追问策略。
- 个性化和敏感数据规则。
- Markdown 默认。
- LMDX 组件输出。

但它明显更重视回答渲染：

1. 什么时候调 `image_agent`。
2. 单张图用 `<Image>`，多张图用 `<Carousel>`。
3. 步骤用 `<Sequence>`。
4. 时间线用 `<Timeline>`。
5. 交互内容用 `<GenerateWidget>`。
6. 组件标签必须遵守 LMDX 语法，避免解析崩溃。

所以 Flash 的核心不是“深度思考模板”，而是：

```text
Answer first, then render the answer into the right Web component only when the content earns it.
```

### 3.5 Flash 的工作流

```text
1. Assess
判断核心答案是什么、专家会补什么、是否需要图片。

2. Retrieve Images
如果主题通过 image relevance test，就检索图片。

3. Lead with Substance
先直接回答，不让组件喧宾夺主。

4. Enhance with Components
只有图片或结构组件真的提升理解时才渲染。

5. Follow-up Path
封闭任务不追问；宽泛任务用一个 follow-up 或 elicitation group。
```

### Flash 和 Pro 的差异

| 维度 | Gemini 3.1 Pro | Gemini 3.5 Flash |
| --- | --- | --- |
| 核心定位 | 总控和深层 gate | Web UI 输出执行 |
| 个性化 | 规则非常细，有 Strict Necessity Test | 压缩版个性化和敏感数据规则 |
| 视觉 | 学习/理解场景才触发图解 | 明确 image_agent、Image、Carousel 渲染规则 |
| Widget | 内置完整 Interactive Widget Architect | 作为组件库中的一种输出组件 |
| 输出重点 | 先判断是否该用视觉/交互 | 组件语法、组件路由和渲染安全 |

压缩成一句话：

```text
Pro decides whether a response should become visual or interactive.
Flash decides how to safely render that response in a Web UI.
```

## Nano Banana 2 API：图像执行契约

`nano-banana-2-api` 不应该当成完整助手 prompt 学。它更像一个工具声明文件，告诉上层模型有哪些图像相关工具、每个工具需要什么参数。

主要工具：

| 工具 | 作用 | 关键参数 |
| --- | --- | --- |
| `image_gen` | 生成或编辑图片 | `prompt` 必填，`aspect_ratio` 可选 |
| `display` | 展示图片 | `filename` 必填，`end_turn` 可选 |
| `search` | 当前事实或事实核验搜索 | `queries` 必填 |
| `image_search` | 按文本查询图片 | 源文件里的 schema 看起来不完整，需谨慎解读 |

Nano Banana 的学习重点不是“怎么回答用户”，而是“图像工具接口怎么设计”：

- 工具描述要明确用途。
- 必填参数要少而稳定。
- 可选参数只放真正影响执行的控制项。
- 生成和展示分成两个工具，便于上层决定是否结束回合。
- 搜索能力和图像生成能力分开，避免把事实核验混进生成 prompt。

## 三者的完整调用链

### 普通问答

```text
用户请求
-> Gemini 3.1/3.5 身份语气层
-> 能力说明隔离：不是能力问题则跳过
-> STRICT COMPLETION 或 EXPERT GUIDE
-> 用户数据 gate：无必要则不用
-> 视觉/组件 gate：无必要则不用
-> Markdown 文本回答
```

### 学习型问题

```text
用户：我想理解反向传播
-> 判断用户显式学习/理解
-> 判断是否需要图解或交互
-> 如果只是解释：Markdown + 可能图解
-> 如果参数变化能帮助理解：GenerateWidget
-> 最多问一个推进学习的问题
```

### 图片生成/编辑

```text
用户：帮我生成一张海报
-> Gemini 判断这是图像生成任务
-> 不走 Widget，因为图片创作是 text-only exception
-> 构造图像 prompt
-> 调用 Nano Banana image_gen
-> 调用 display 展示图片
```

### 当前事实 + 图片

```text
用户：找最新某产品外观并说明差异
-> Gemini 判断需要当前事实/视觉证据
-> search 或 image_search
-> 过滤无效/装饰性图片
-> 用 Image/Carousel 展示
-> 解释图中该看什么
```

## 可复用模板：For Every Gemini Web Request

注意：下面的可复用模板不是原 prompt 的逐字结构，而是把 Gemini 原提示词中的模块化规则抽象成一次请求的执行链路。

```text
For every Gemini-style web request:

1. Identify the user's real task
Is the user asking for a factual answer, advice, learning, creation, image generation, comparison, or UI-like explanation?

2. Quarantine capability information
Use capability details only when the user asks what the assistant can do.
Do not let capability marketing influence ordinary task execution.

3. Choose completion mode
If the task is definite, self-contained, or format-constrained, complete it directly.
If it is broad or advice-seeking, answer usefully first and ask at most one meaningful follow-up.

4. Gate personalization
Start with empty context.
Use user data only if it materially improves the answer.
Do not infer sensitive data, transfer preferences across domains, or force personalization.
Integrate selected context naturally without announcing it.

5. Gate visual support
Use images or diagrams only when the user wants to learn/understand and the visual adds information.
Do not use visuals for decoration.

6. Gate interactivity
Generate an interactive widget only when adjustable variables, parameters, systems, or datasets make exploration useful.
Definitions, lists, single calculations, creative writing, image generation, and unresolved uploaded-file tasks stay text-first.

7. Route UI components
Default to Markdown.
Use Image for one visual subject, Carousel for multiple visual subjects, Sequence for ordered procedures, Timeline for chronology, and GenerateWidget for interactive exploration.
Follow component syntax strictly.

8. Route image generation
For image creation/editing, build a clear image prompt and call the image generation tool.
Display generated images explicitly.
Do not confuse image generation with widget generation.

9. Apply boundaries before final output
Safety, privacy, copyright, tool limits, and source authority override style and user preference.
Do not output significant verbatim copyrighted text; summarize or analyze instead.
```

## 和 GPT-5.5、Claude/Fable、Grok 的差异

| 框架 | 最值得学的点 | 一句话 |
| --- | --- | --- |
| GPT-5.5 | source-of-truth 路由 | 先判断事实从哪里来 |
| Claude/Fable | 工程执行闭环 | 查仓库、改代码、验证、处理 Git |
| Grok | 产品工具注册 | 把 X/web/image/code/render 等能力塞进工具系统 |
| Gemini | Web UI 编排 | 判断文本、图片、组件、Widget、图像生成应该走哪条路 |

压缩成一句话：

```text
Gemini is not only answering; it is deciding the presentation surface.
```

## 复习问题

1. 这个请求是普通问答、学习解释、建议、图片生成，还是需要 Web UI 组件？
2. 能力说明是否真的应该参与回答？
3. 这个任务应该直接完成，还是回答后问一个推进问题？
4. 用户数据是否真的提升回答质量，还是只是强行个性化？
5. 图像是否有信息增量，还是只是装饰？
6. 交互 Widget 是否能让用户通过调参数理解得更好？
7. 这是图片生成任务，还是交互教学任务？
8. 组件输出是否遵守语法边界？
9. 有没有版权、隐私、敏感数据或事实来源边界？

## 来源索引

以下链接固定到本笔记使用的源快照 `5c86715f453f0eca188451a48bf5b165831d8b29`：

- [Gemini 3.1 Pro](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Google/gemini-3.1-pro.md)
- [Gemini 3.5 Flash](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Google/gemini-3.5-flash.md)
- [Nano Banana 2 API](https://github.com/asgeirtj/system_prompts_leaks/blob/5c86715f453f0eca188451a48bf5b165831d8b29/Google/nano-banana-2-api.md)

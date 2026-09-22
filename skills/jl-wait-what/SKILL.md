---
name: jl-wait-what
description: 当用户明确表示没有理解上一条回复、要求换一种更简单的说法，或询问“现在讲到哪了”时，用中文补足缺失上下文并重新表述上一条回复。只修复当前沟通，不用于首次讲解新主题、普通摘要、翻译，或持续改变后续回复风格。
---

# JL Wait, What

## Contract

Repair the immediately preceding assistant response so the user can understand the
current state and continue. Respond primarily in Chinese. This is a one-response
repair, not a persistent style mode, a new task, or authorization to advance work.

Invoke automatically only when the user is reacting to the preceding assistant
response with clear confusion or asks for that response to be re-pitched, such as
“没懂”“什么意思”“讲简单点”“说人话”“换种说法” or “现在讲到哪了”. The target must
be the assistant's preceding explanation. A request to explain a new concept,
summarize a document, translate text, or teach from scratch is not this skill.

## Re-pitch

1. Identify the specific missing link when the user's wording reveals it; otherwise
   rebuild the previous response from its outcome.
2. Supply only the context needed to connect the conclusion to the user's current
   situation. Use relevant conversation state and established project terminology.
   When a term first appears, explain it in plain Chinese before relying on it.
3. State what is true now, why it matters, and the one next action or decision only
   when work remains. A short answer does not need forced headings; use “现在讲到”
   “为什么” and “下一步” only when they make the explanation easier to scan.
4. If the previous response was inaccurate or overconfident, correct it explicitly
   instead of simplifying the error. Keep material uncertainty visible.

Do not repeat the full conversation, introduce side topics, or continue execution.
Do not treat “继续解释” as approval to edit files, call mutating tools, publish,
merge, deploy, or otherwise advance the underlying task. If the previous response
was waiting on a user decision, restate the exact decision and at most three
meaningfully different options.

# Awesome AI Coding Cost [![Awesome](https://awesome.re/badge-flat2.svg)](https://github.com/sindresorhus/awesome)

> **Codex 额度不够怎么办？GPT-6 Astra 怎么用才不吃 token？配额用完、触发 5 小时限流怎么解决？** 这份清单按你遇到的问题分类，收录能直接落地的方案：推理强度怎么选、哪些开关改一次长期省、子 Agent 编队省额度、token 用量追踪、上下文压缩、多账号配额管理，以及订阅制与按量计费的取舍。
>
> 每条标注 star 数、许可证、最后更新时间，**已停更的项目明确标出**。附一节配置勘误：一份流传较广的编队配置与上游仓库不一致，低档位照抄反而更烧额度。
>
> **Codex / Claude Code quota exhausted? Hit the 5-hour rate limit?** A curated list of quota & cost optimization tools for AI coding agents — **organized by the problem you're hitting**, not by technique. Subagent orchestration, usage tracking, context compression, multi-account management, and subscription vs pay-as-you-go. Every entry carries stars, license, and last-update date.

[English](#english) · 中文（本页）

**关键词**：Codex 额度不够 · Codex 5 小时限流 · Claude Code 配额用完 · Astra 怎么用不吃 token · Astra 消耗太快 · Astra 推理强度怎么选 · reasoning effort · 子 Agent 省额度 · AGENTS.md 精简 · 实验性上下文管理 · token 用量监控 · 上下文压缩 · 多账号配额池 · 订阅 vs 按量计费

---

## 为什么又一个清单

现有的 token 优化清单大多按**技术手段**分类（prompt caching、KV cache、batch API、学术论文）。但开发者真正的处境通常是这样的：

> 「我选了 GPT-6 Astra，跑了两分钟四十秒，5 小时的配额直接归零。活还没干完，额度先空了。」

或者：

> 「Codex 周限额用完了，`/status` 里显示还要等三小时。」
> 「Astra 消耗为什么是 Sol 的四倍？官方标称才 2.5 倍。」
> 「推理强度到底该设哪一档才不吃 token？」
> 「按教程配了子 Agent 编队，额度反而掉得更快。」

这时候需要的不是一份技术综述，是**一个能马上装上去的东西**，以及**哪些方案在什么条件下才真的省**。所以这份清单按痛点分章，每章先说症状，再给可落地的项目和落地前必须知道的前提。

三条收录纪律：

1. **标注最后更新时间**，停更的项目明确写出来——这个赛道两周换一批，一份不筛的清单就是负资产
2. **只收真实项目**，用 `created_at` 对比模型发布日期，排除旧仓库改名蹭热度的（方法见[附录](#附录识别蹭热度的仓库)）
3. **写出已知局限**，不只列优点

数据核实时间：**2026-09-17**。star 数会变，以仓库页面为准。

---

## 目录

- [痛点一：旗舰模型把配额烧穿](#痛点一旗舰模型把配额烧穿)
  - [🔴 编队不必然省额度：wait 轮询是隐藏成本](#-编队不必然省额度wait-轮询是隐藏成本)
  - [控制 wait 开销的四个配置项](#控制-wait-开销的四个配置项)
  - [什么时候**不该**用编队](#什么时候不该用编队)
- [痛点二：推理强度设错，或该开的开关没开](#痛点二推理强度设错或该开的开关没开)
  - [五档推理强度的实际代价](#五档推理强度的实际代价)
  - [⚠️ 一个反直觉情形：更高强度有时总成本更低](#️-一个反直觉情形更高强度有时总成本更低)
  - [三个改一次就长期生效的设置](#三个改一次就长期生效的设置)
- [痛点三：不知道钱花在哪](#痛点三不知道钱花在哪)
- [痛点四：上下文膨胀，越聊越贵](#痛点四上下文膨胀越聊越贵)
- [痛点五：多账号配额分散](#痛点五多账号配额分散)
- [痛点六：计费方式本身选错了](#痛点六计费方式本身选错了)
- [⚠️ 一份流传较广的错误配置](#️-一份流传较广的错误配置)
- [附录：识别蹭热度的仓库](#附录识别蹭热度的仓库)

---

## 痛点一：旗舰模型把配额烧穿

**症状**：把顶级模型设为主模型，让它从头干到尾——包括扫目录、翻源文件、改配置这些机械活。配额消耗集中在最贵的模型上。

**解法**：模型分工编队。贵模型只做拆解、决策、验收；机械活交给便宜模型的子 Agent。

| 项目 | Star | 许可 | 最后更新 | 说明 |
|---|---:|---|---|---|
| [donvito/codex-astra-luna-orchestrator](https://github.com/donvito/codex-astra-luna-orchestrator) | 1444 | Apache-2.0 | 2026-09-16 | Codex 的编队配置。**有四套 profile**（pro / plus / pro-max-2-subagents / plus-max-2-subagents）+ 安装脚本，会先问你是哪个档位。5 个固定子 Agent：explorer / worker / tester / reviewer / researcher |
| [irons163/three-tier-agent-orchestrator](https://github.com/irons163/three-tier-agent-orchestrator) | 50 | — | 2026-09-08 | **三层**而非两层：顶层统筹、中层处理「难但边界清楚」的活、底层做机械活。繁体中文 README，[英文版另有仓库](https://github.com/irons163/three-tier-agent-symphony)。⚠️ 无 LICENSE 文件 |
| [SirRuggie/claude-code-orchestration-kit](https://github.com/SirRuggie/claude-code-orchestration-kit) | 24 | MIT | 2026-09-13 | Claude Code 版的同类思路，一个贵模型统筹 + 五个钉死的便宜子 Agent，直接放 `CLAUDE.md` |

**已停更，不建议用**：

| 项目 | Star | 情况 |
|---|---:|---|
| [DannyMac180/astra-advisor](https://github.com/DannyMac180/astra-advisor) | 220 | **2026-09-04 创建，同日最后更新**。star 数不低但没有后续维护，README 里自己标注了 ChatGPT Work cloud 的 `create_thread` 限制未解决 |

### 📌 落地前必须知道的一件事

**「贵模型当总指挥」这个说法对订阅制的低档位不成立。**

`donvito` 那个项目的 Plus 档配置里，**总指挥根本不是 Astra**：

| 角色 | Plus 档 | Pro 档 |
|---|---|---|
| 总指挥（root） | **GPT-5.6 Luna — max** | GPT-6 Astra — medium |
| 执行子 Agent | GPT-5.6 Luna — medium | GPT-5.6 Luna — max |
| reviewer | GPT-6 Astra — **low** | GPT-6 Astra — low |

仓库注释原文：*"The root runs on GPT-5.6 Luna at maximum reasoning instead of GPT-6 Astra, so the largest thread in an orchestrated session stays on the cheaper model."*

**原因**：编队里 root 线程是上下文最长的那一条。低档位订阅下，光让旗舰模型跑 root 就能把配额吃掉。所以 Plus 档的正确做法是**旗舰只留在 reviewer 位、且推理强度设 low**。

照抄 Pro 档配置的 Plus 用户，会精确复现「配额两分钟清零」这个问题。详见[错误配置那一节](#️-一份流传较广的错误配置)。

### 🔴 编队不必然省额度：wait 轮询是隐藏成本

这是本节最重要的一条，**大多数「编队省额度」的教程没有提**。

**机制**：子 Agent 在后台跑的时候，root 需要知道它们完成了没有。这个等待过程不是免费的——root 会反复轮询子 Agent 状态，**每次轮询都是一次真实的模型调用**。子 Agent 干得越久，root 空转的轮询开销越大。

官方文档对此有明确说明：

> 「子智能体工作流比同类单智能体运行消耗更多 token，因为每个子智能体都会独立执行模型和工具相关工作。」
> —— [Codex 官方文档 · Subagents](https://www.codex-docs.com/getting-started/concepts/subagents/)

**社区实测数据**（⚠️ 他人测量，本清单未独立复现）：

| 观测 | 数值 | 来源 |
|---|---|---|
| wait 占五小时配额 | **41.2%** | [linux.do #2894195](https://linux.do/t/topic/2894195) |
| wait 占 Astra 总消耗 | 61.2%，其中纯超时 47.1% | 同上 |
| Astra vs Sol 官方标称倍率 | 2.5× | OpenAI 定价 |
| Astra vs Sol **实测**倍率 | **3.9× / 4–5×**（缓存命中 97-98% 下） | [linux.do #2861037](https://linux.do/t/topic/2861037)、[#2861126](https://linux.do/t/topic/2861126) |
| Pro 20x 档：4 亿 token 吃掉配额 | Astra High **32%** vs Sol High 约 7% | [linux.do #2873230](https://linux.do/t/topic/2873230) |

**这解释了三个此前看起来奇怪的设计**：

1. 为什么 `donvito` 的 Plus 档**把 root 换成便宜模型** —— root 是轮询的发起方，它贵不贵直接决定 wait 开销
2. 为什么并发默认 **4 而不是 6 或 8** —— 并发越多，root 要轮询的对象越多
3. 为什么仓库专门提供 `-max-2-subagents` profile —— 把并发压到 2，就是在压轮询成本

### 控制 wait 开销的四个配置项

| 配置项 | 建议 | 说明 |
|---|---|---|
| `agents.max_concurrent_threads_per_session` | **从 2–4 起步** | 轮询对象数量的直接上限。别一上来拉到 8 |
| `agents.max_depth` | **保持默认 1** | 官方警告：调大会让「广泛委派」指令变成反复扇出，token、延迟、本地资源同时上涨 |
| root 的 `model` | 低档位订阅用**便宜模型** | root 承担轮询开销，也是上下文最长的线程 |
| root 的 `model_reasoning_effort` | 不要盲目设 `high` / `max` | 每次轮询都按这个强度计费 |

⚠️ `agents.max_threads` 是旧别名，已被 `max_concurrent_threads_per_session` 取代，新配置请用后者。

### 什么时候**不该**用编队

编队有固定开销，任务不够大就是净亏：

- ❌ **子任务之间有依赖** —— 官方判据：*如果子任务不需要知道其他 Agent 的中间结果就能独立完成，才适合并行*。有依赖就会退化成串行 + 轮询开销
- ❌ **单文件改动、几轮对话的小脚本** —— 编队的固定成本大于收益
- ❌ **只是想「显得并行」** —— 并发数拉高不等于更快，文件改动还可能冲突

✅ 适合的场景：**中大型工程重构、多模块协同、真正互相独立的子任务**。

📌 **一句话总结**：编队省的是「让旗舰模型干机械活」那部分钱，但引入了「root 空转轮询」这笔新开销。**任务够大、子任务真独立、root 用便宜模型、并发别拉满** —— 四个条件同时满足才是净省。

---

## 痛点二：推理强度设错，或该开的开关没开

**症状**：没配编队、也没多账号，就是单纯觉得「Astra 好贵」。或者反过来——已经很省着用了，额度还是掉得快。

**解法**：这一类不需要装任何东西，**改配置就行，而且改一次长期生效**。

### 五档推理强度的实际代价

`reasoning.effort` 有五档：`low` / `medium` / `high` / `xhigh` / `max`。

**关键认知**：强度**不改变单 token 价格**，它改变的是模型花掉多少 token。所以「调低强度省钱」的本质是「让它少想」。

某次公开测算中单任务的独立成本与质量分（⚠️ 第三方测算，非官方数据）：

| 强度 | 单任务成本 | 质量分 |
|---|---:|---:|
| `low` | $0.63 | 49 |
| `medium` | $1.16 | 52 |
| `high` | $1.41 | 53 |
| `xhigh` | $1.85 | 54 |
| `max` | $2.57 | 55 |

**边际收益递减得非常明显**：`low → medium` 花 0.53 美元买 3 分；`xhigh → max` 花 0.72 美元只买 1 分。

**官方自己的建议**：Agent 编码与研究类任务用 `medium`，复杂调试用 `high`，`xhigh` **只在你的评测显示明确收益时**才用。OpenAI 还特别提到：**先试 Astra 的 `low` 或 `medium`** ——Astra 在 `low` 下可能已经超过上一代在 `high` 下的表现。

📌 **最常见的浪费**：把强度一律设成 `high` 甚至更高，以为「反正更聪明总没坏处」。实际上一个在 `low` 下就能通过验证的短任务，**调高只会让它写更长的解释，不会让它更正确**。

### ⚠️ 一个反直觉情形：更高强度有时总成本更低

这条和上面不矛盾，但条件很严：

**机制**：单次调用更贵，但如果所需的调用**次数**下降得足够多，总成本可以反过来。高强度减少了试错与返工的轮数。

ARC-AGI-3 基准上的一组数据：

| 强度 | 得分 | 总成本 |
|---|---:|---:|
| `medium` | 38.6% | $48,090 |
| `xhigh` | 59.3% | $37,317 |
| `max` | 62.7% | **$26,098** |

⚠️ **但这个结论不能直接套到你身上**，三个前提必须同时成立：

1. 任务在 `medium` 下**确实存在大量返工**（反复失败、反复重做）
2. 提高强度**真的减少了调用次数**，不只是想得更久
3. 产出**达到完成标准** ——「`xhigh` 消耗更低」如果结果不合格，那不叫省

⚠️ 还有一条更要紧的限定：**上面那组数字测的是基准测试的 API 成本，不是订阅制配额的实际扣减行为**。两者的换算关系不公开。所以**不要默认选 `xhigh`**——先在自己的任务上量一遍返工率。

### 三个改一次就长期生效的设置

**① 开启实验性上下文管理**

旧的压缩机制是上下文满了就把整段对话摘要成一份，细节损失大、长会话里会反复重建对任务的理解。新机制给的是 token 预算 + 历史笔记 + 按需取回。

加到 `~/.codex/config.toml`：

```toml
[features.context_management]
experimental_mode = true
```

**改完必须完整重启 Codex**，不重启不生效。

⚠️ 适用范围（据 [openai/codex PR #42385](https://github.com/openai/codex/pull/42385)）：ChatGPT **Plus / Pro / Pro Lite** 且走 Codex 后端。**自定义 provider、自带凭证、非 Codex 端点不支持**——用第三方 API 的场景这个开关用不上。

**② 清理 `AGENTS.md` 与 Skill 描述**

Astra 对指令比上一代敏感得多，旧文件里模糊或冲突的规则会让它停下来问你，而不是自己判断。具体做法：

- **合并重复规则** ——同一件事在 AGENTS.md 和 Skill 里各写一遍，等于每轮多付一次
- **精简触发描述** ——触发条件写宽了，Skill 会在不需要的时候被拉起来
- **减少无条件规则**，换成精确触发 + 明确的完成标准
- 在提示词里写明「按上下文理解意图，把已授权的工作做完」，减少它反复澄清

📌 这条的收益容易被低估：`AGENTS.md` 是**每轮都进上下文**的，它的冗余会被会话长度放大。

**③ 聊天和编码用不同的入口**

闲聊、搜索、分析这类任务放到 ChatGPT 的对话模式里做 ——**它和 Codex 的配额是完全分开的**。拿 Codex 的额度去聊天，是在烧错的那份预算。

### 这一类的排查顺序

遇到「额度掉得快」，按这个顺序过一遍再去装工具：

1. 强度是不是一律设了 `high` 以上？→ 降到 `medium` 试
2. 实验性上下文管理开了吗？→ 开，然后完整重启
3. `AGENTS.md` 有多长、有多少条无条件规则？→ 精简
4. 是不是在用 Codex 做本该在对话模式做的事？→ 换入口
5. 以上都做了还是不够 → 再看[编队](#痛点一旗舰模型把配额烧穿)、[压缩](#痛点四上下文膨胀越聊越贵)、[计费方式](#痛点六计费方式本身选错了)

**前四步都是免费的，且不引入任何新依赖。** 先做完这四步，再考虑加东西。

---

## 痛点三：不知道钱花在哪

**症状**：账单出来了，但说不清哪个项目、哪个工具、哪一类操作吃掉了大头。想优化没有抓手。

**解法**：用量追踪。先量化再优化。

| 项目 | Star | 许可 | 最后更新 | 说明 |
|---|---:|---|---|---|
| [getagentseal/codeburn](https://github.com/getagentseal/codeburn) | 11056 | MIT | 2026-09-16 | 覆盖面最广：**37 个工具与 Agent**（Claude Code、Cursor、Codex、Gemini 等）。本地运行，不上传数据 |
| [junhoyeo/tokscale](https://github.com/junhoyeo/tokscale) | 5460 | MIT | 2026-09-15 | Rust 写的终端工具，在命令行里看用量。带全球排行榜（⚠️ 排行榜是可选的联网功能，在意隐私的注意） |
| [Javis603/token-monitor](https://github.com/Javis603/token-monitor) | 2185 | — | 2026-09-16 | 桌面常驻小组件，适合想一直盯着的场景。⚠️ 未标注许可证 |
| [xiufengsun/TokenTracker](https://github.com/xiufengsun/TokenTracker) | 1637 | MIT | 2026-09-16 | 本地优先，覆盖 31 个工具，含 DeepSeek Harness |
| [tddworks/ClaudeBar](https://github.com/tddworks/ClaudeBar) | 1495 | — | 2026-09-14 | macOS 菜单栏常驻。⚠️ 仅 macOS，未标注许可证 |
| [Dicklesworthstone/coding_agent_usage_tracker](https://github.com/Dicklesworthstone/coding_agent_usage_tracker) | 85 | — | 2026-09-04 | 单个 CLI 跨 Codex / Claude 等查用量，轻量 |

**怎么选**：想要覆盖面 → `codeburn`；习惯终端 → `tokscale`；想一直看着 → `token-monitor` 或 `ClaudeBar`。

---

## 痛点四：上下文膨胀，越聊越贵

**症状**：会话越长越贵。工具 schema、文件读取结果、历史对话在每一轮里重复计费，实际有效信息占比越来越低。

**解法**：在 Agent 和模型之间插一层压缩。

| 项目 | Star | 许可 | 最后更新 | 说明 |
|---|---:|---|---|---|
| [Paritok-official/paritok-4b-v1](https://github.com/Paritok-official/paritok-4b-v1) | 1454 | Apache-2.0 | 2026-09-10 | **改 `BASE_URL` 就能插进去，不动 Agent 一行代码**。剥离工具 schema 冗余、压缩工具结果与文件读取、摘要陈旧历史，按压缩后的 token 计费。**非破坏性**——Agent 可以按需取回任何原文。自称首轮省约 25%、长会话到 85%+，同上下文窗口塞约 3 倍轮次。附 [arXiv 论文](https://arxiv.org/abs/2608.24188) 与 HuggingFace 模型 |
| [ooples/token-optimizer-mcp](https://github.com/ooples/token-optimizer-mcp) | 532 | MIT | 2026-09-17 | MCP 形态，覆盖 16 个 CLI 客户端。会**量化每个 Agent 省了多少**，还带本地知识图谱共享 |
| [egorfedorov/claude-context-optimizer](https://github.com/egorfedorov/claude-context-optimizer) | 111 | MIT | 2026-09-15 | Claude Code 插件，标出浪费掉的上下文并给热力图，自称省 30–50% |

⚠️ **压缩类方案的共同注意事项**：它们都在你和模型之间加了一跳。这意味着多一个故障点，也意味着你的代码会经过这一层。**自托管还是用对方的服务，接入前要确认清楚**。`Paritok` 的模型权重公开在 HuggingFace 上，可以自己跑。

---

## 痛点五：多账号配额分散

**症状**：手上几个账号，每个都有独立配额窗口，但用的时候只能一个一个切，切换成本高、也看不到总体余量。

**解法**：负载均衡或统一控制台。

| 项目 | Star | 许可 | 最后更新 | 说明 |
|---|---:|---|---|---|
| [jlcodes99/cockpit-tools](https://github.com/jlcodes99/cockpit-tools) | 17811 | — | 2026-09-16 | 覆盖最广的账号管理：Antigravity / Codex / GitHub Copilot / Windsurf / Kiro / Cursor / Gemini-cli / CodeBuddy 八家，多账号切换 + 配额查看。Rust，中文界面。⚠️ 未标注许可证 |
| [Soju06/codex-lb](https://github.com/Soju06/codex-lb) | 3141 | MIT | 2026-09-16 | 多账号**负载均衡代理**，带用量追踪与仪表盘，兼容 OpenCode 端点 |
| [wannanbigpig/codex-accounts-manager](https://github.com/wannanbigpig/codex-accounts-manager) | 129 | — | 2026-09-09 | VS Code 插件形态，切 `auth.json`、跟踪配额 |
| [zangzi2018/quota-pool-for-codex](https://github.com/zangzi2018/quota-pool-for-codex) | 102 | AGPL-3.0 | 2026-09-16 | 自托管多设备控制台，含远程会话。⚠️ 非官方；AGPL-3.0 对商业集成有约束，用前看清许可 |

⚠️ **合规提醒**：多账号池化可能与服务商的服务条款冲突，尤其是把个人订阅额度对外分发的场景。**自己用和对外提供服务是两件事**，后者风险高得多。

---

## 痛点六：计费方式本身选错了

前面四类都是在**订阅制**的框架内省配额。但有时问题不在配置，在计费方式本身。

**两种计费的性质不同**：

| | 订阅制 | 按量计费 |
|---|---|---|
| 成本模式 | 固定月费 + **滚动窗口配额** | 按实际 token 付费 |
| 触顶表现 | **限流，活干不完也得等** | 不限流，花多少算多少 |
| 适合 | 用量稳定且可预测 | 用量波动大、或需要精确核算 |
| 风险 | 高强度任务瞬间烧穿 | 失控的 Agent 会烧钱 |

**判断方法**：如果你经常在窗口内触顶，而且[痛点二那四步免费优化](#这一类的排查顺序)做完、编队也配了，**还是**触顶——那问题可能不是配置，是这个档位的配额量级本身不够。这时候换计费方式比继续调配置有效。

⚠️ 顺带一条与[痛点一](#-编队不必然省额度wait-轮询是隐藏成本)相关的差别：按量计费下没有滚动窗口，所以 wait 轮询那笔开销只是多花一点钱，**不会让你的活干不完**。订阅制下它会直接变成限流。这是计费方式的性质差异，不是配置能消除的。

### 换按量计费前，先算再换

别凭感觉换。按这个顺序走：

**① 先量出自己的真实用量** ——用[痛点三](#痛点三不知道钱花在哪)里的任一工具跑一周，拿到输入/输出/缓存三项的实际 token 数。没有这个数，后面都是猜。

**② 代入算总成本** ——把三项 token 数代进比价工具，和订阅月费对比。注意要算**缓存命中后的有效成本**，不是标价。

**③ 确认目标端点的计量字段完整** ——见[下一节](#一个和成本直接相关的判据usage-字段完整性)。字段缺了，你换过去也验证不了到底省没省。

### 相关工具

| 项目 | Star | 许可 | 说明 |
|---|---:|---|---|
| [LMU-AI/ai-api-price-calculator](https://github.com/LMU-AI/ai-api-price-calculator) | — | 开源 | 把各平台的复杂计费统一换算成 ¥/百万 token，支持 Prompt Cache 与月费估算。在线版 [calc.lmu.ai](https://calc.lmu.ai/)。**本清单维护方出品，一并说明** |
| [LMU-AI/check-claude-api](https://github.com/LMU-AI/check-claude-api) | — | 开源 | 一键检测某个 Anthropic 协议端点是不是真实实现、支不支持 Prompt Cache。**本清单维护方出品** |

### 维护方自己用的是什么

**利益相关**：本清单由**灵眸AI（LMU AI）**维护，它是一个 AI API 聚合网关。下面这段是自我介绍，按需跳过——清单主体不含任何推广链接，六类痛点里收录的项目也和我们没有商业关系。

我们自己解决这个问题的方式就是**按量计费**，几条和上面讨论直接相关的：

- **无滚动窗口** ——没有 5 小时 / 周限额这回事，所以 [wait 轮询](#-编队不必然省额度wait-轮询是隐藏成本)那笔开销只是多花点钱，**不会让你的活干不完**
- **`usage` 四个字段完整** ——含两个缓存字段，所以上面那些优化你都能验证效果。[验证方法](#一个和成本直接相关的判据usage-字段完整性)在下一节，可以拿来验我们自己
- **一个 Base URL 覆盖国产 + 海外** ——Claude / GPT / Gemini / Grok 与 GLM / Qwen / DeepSeek / Kimi / MiniMax / MiMo 同一个端点，做[痛点二](#痛点二推理强度设错或该开的开关没开)那种「换个便宜模型试试」的对比时不用开多个账号
- **¥10 起充，余额永不过期、随时可退** ——先小额验一遍再决定投入

**⚠️ 一个必须说清的限制**：`[features.context_management] experimental_mode = true` 这个开关**只对走 Codex 后端的 ChatGPT Plus/Pro/Pro Lite 生效**，用任何第三方 API（包括我们）都用不上。所以[痛点二](#痛点二推理强度设错或该开的开关没开)里那三个免费设置，第一个在按量方案下是失效的——推理强度和 `AGENTS.md` 精简这两条仍然有效。

**⚠️ 另一个限制**：密钥的模型覆盖范围不是全量的。国产模型有集合分组可一个密钥通用；海外模型只能同厂商通用，Claude 和 GPT 需要分别配置。

注册入口（含邀请关系，完成首次充值或订阅可享 ¥2.00 新人体验金 + 按订单金额额外赠 10% 余额）：

```
https://api.lmuai.ai/register?ref=bF5zuCmw&utm_source=both&utm_medium=github&utm_campaign=awesome_ai_coding_cost
```

也可以不走这个链接，直接搜 `api.lmuai.ai` ——功能完全一样，只是没有上面那两项新人福利。

📌 **但这不是唯一答案**。按量计费适合用量波动大、需要精确核算的场景；如果你的用量稳定且可预测，订阅制的单位成本通常更低。**先把痛点二那四步免费优化做完，再决定要不要换计费方式。**

### 一个和成本直接相关的判据：`usage` 字段完整性

不管用哪种计费方式，**先确认你能不能拿到完整的计量数据**：

```json
{
  "usage": {
    "input_tokens": 245,
    "cache_creation_input_tokens": 3120,
    "cache_read_input_tokens": 8450,
    "output_tokens": 412
  }
}
```

后两个是缓存字段。在连续会话场景里，缓存命中率直接决定输入侧成本量级——**这两个字段缺失或恒为 0，意味着这部分成本不可核算**，你只能拿账单总额倒推，前面那些优化也就无法验证效果。

零成本自测（不需要有效凭证、不消耗额度）：

```bash
curl $BASE_URL/v1/messages \
  -H "x-api-key: sk-invalid-key-for-test" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"<模型名>","max_tokens":20,"messages":[{"role":"user","content":"hi"}]}'
```

- 返回**符合协议 schema 的鉴权错误** → 该路径是真实的协议实现
- 返回**站点首页 HTML 或通用 404** → 该路径未实现对应协议，请求被前置路由兜底了

---

## ⚠️ 一份流传较广的错误配置

2026 年 9 月有一份 Codex 编队配置被大量转载，与 `donvito/codex-astra-luna-orchestrator` 仓库实际内容**不一致**。逐字对照如下：

| 字段 | 流传的版本 | 仓库 **Pro** 档 | 仓库 **Plus** 档 |
|---|---|---|---|
| `model` | `gpt-6-astra` | `gpt-6-astra` | **`gpt-5.6-luna`** |
| `model_reasoning_effort` | `high` | **`medium`** | `max` |
| `max_concurrent_threads_per_session` | `6` | **`4`** | `4` |
| `default_subagent_reasoning_effort` | `medium` | **`max`** | `medium` |

**最关键的一条**：流传版本把旗舰模型钉在 root 位、推理强度 `high`。而仓库对低档位订阅的答案恰恰相反——**root 用便宜模型，旗舰只留在 reviewer 位、推理强度 `low`**。

结果是：低档位用户照抄这份配置，会复现它声称要解决的那个问题。

**另外**，仓库提供 `setup.sh` / `setup.ps1` 安装脚本，会询问档位并写入对应 profile。流传版本描述的是手动复制三个文件，遗漏了这一步，也遗漏了四套 profile 的存在。

以仓库为准：

- Pro 档配置 → [`profiles/pro/codex/config.toml`](https://github.com/donvito/codex-astra-luna-orchestrator/blob/main/profiles/pro/codex/config.toml)
- Plus 档配置 → [`profiles/plus/codex/config.toml`](https://github.com/donvito/codex-astra-luna-orchestrator/blob/main/profiles/plus/codex/config.toml)

📌 **通用教训**：这类配置的转载链条很长，**每一跳都可能失真**。照抄之前花两分钟打开仓库原文对一遍——尤其是模型名和推理强度这两个直接决定成本的字段。

---

## 附录：识别蹭热度的仓库

新模型发布后，搜索结果里会混入**旧仓库改名 + 灌内容**的项目。它们的 star 是历史积累的，和当前内容无关。

**一分钟识别法**：

```bash
curl -s https://api.github.com/repos/<owner>/<repo> \
  | python3 -c "import json,sys; d=json.load(sys.stdin); \
    print('created:', d['created_at'][:10], '| pushed:', d['pushed_at'][:10])"
```

把 `created_at` 和**模型的发布日期**对比：

- `created_at` 早于模型发布日很多，而所有提交都集中在最近几天 → 大概率是改名项目
- 再看提交历史里有没有 `Merge remote history` / `repo content sync` 这类信息

**实例**：筛选本清单时，搜索结果靠前有一个 1103★ 的 Astra 清单，`created_at` 是 **2023-05-19**，而 GPT-6 Astra 于 2026-09-03 发布；全部提交集中在 2026-09-06 一天内，含一条 `Merge remote history (repo content sync)`。据此未收录。

这个方法对任何「新技术 + awesome」类搜索都适用。

---

## 贡献

欢迎 PR。收录标准：

1. **能落地**——有具体配置、可安装、或可运行，不只是文章或观点
2. **在维护**——最后更新在 3 个月内；停更项目可以收录但必须标注
3. **注明来源与局限**——PR 里说明它解决什么问题、已知短板是什么
4. **不收改名蹭热度的项目**——见[附录](#附录识别蹭热度的仓库)

提 PR 时请按现有格式补齐 star、许可、最后更新日期三项。

## 维护

本清单每月核一次。仓库内有校验脚本：

```bash
# 检查有没有条目停更、star 数是否过期、链接是否失效
python3 scripts/check_entries.py

# 顺手把 star 数与更新日期写回 README
python3 scripts/check_entries.py --fix
```

判定规则与上面的收录标准一致：最后更新超过 90 天判为停更，star 数偏差超过 20% 判为数字过期。GitHub Actions 每月自动跑一次。

发现过期或错误信息，欢迎直接开 issue。

## 许可

内容部分采用 [CC0-1.0](LICENSE)（公共领域）——随便抄、随便改、随便用于商业目的，不用署名。

被收录的各个项目各自遵循其仓库标注的许可证，**接入前请自行确认**，清单里标注的许可字段仅供快速参考。

## 免责声明

- star 数与更新日期核实于 **2026-09-17**，会随时间变化
- 各项目的**节省比例均为项目方自述**，本清单未做独立复现验证，请自行小规模实测
- 多账号池化类工具可能与服务商条款冲突，风险自负
- 本清单包含维护方自己的两个开源工具，已在条目中标明
- 维护方是 AI API 网关服务商（灵眸AI），**利益相关已在[痛点六](#维护方自己用的是什么)与页脚声明**。清单主体六类痛点收录的项目与我们无商业关系，也包括与我们构成替代关系的方案（如多账号池化、订阅制优化）
- 注册链接带 `ref` 与 UTM 参数用于统计来源；不走该链接直接访问 `api.lmuai.ai` 功能完全相同

---

## English

A curated list of quota & cost optimization tools for AI coding agents, **organized by the problem you're hitting** rather than by technique.

Existing token-optimization lists group by method (prompt caching, KV cache, batch APIs, papers). But the situation developers actually face sounds like this:

> "I picked the flagship model, ran it for two minutes, and my 5-hour quota hit zero."

What helps there isn't a survey — it's something you can install right now.

**Inclusion rules**: every entry carries stars, license, and last-update date; stale projects are explicitly labeled; repos that were renamed to ride a trend are excluded (see [the appendix](#附录识别蹭热度的仓库) for the one-minute detection method).

**Sections** — see the Chinese content above for full tables:

1. **Flagship model burns your quota** → orchestration patterns (expensive model plans, cheap subagents execute). ⚠️ **Includes a section most orchestration guides omit**: waiting on subagents is not free — root polls them, and every poll is a real model call. Community measurements put `wait` at **41.2% of a 5-hour quota** and Astra's real consumption at **3.9–5× Sol** versus the 2.5× official ratio (not independently reproduced here)
2. **Reasoning effort set wrong, or a free switch left off** → the five `reasoning.effort` tiers and their real marginal cost, the counter-intuitive case where *higher* effort lowers total cost (and the three conditions that must hold), plus three settings you change once: `[features.context_management] experimental_mode = true`, trimming `AGENTS.md`, and not burning Codex quota on chat tasks. **The first four fixes here are free and add no dependencies** — do them before installing anything
3. **You can't tell where the money went** → usage trackers
4. **Context bloat** → non-destructive compression gateways
5. **Quota scattered across accounts** → load balancers and consoles
6. **Wrong billing model entirely** → subscription vs pay-as-you-go tradeoffs

⚠️ **One important correction**: a widely-reposted Codex orchestration config does **not** match the upstream repo. It pins the flagship model as root at `high` reasoning — while the repo's actual answer for lower subscription tiers is the opposite: **run root on the cheaper model, keep the flagship only as a low-reasoning reviewer**. See [the correction section](#️-一份流传较广的错误配置).

All savings figures are **as claimed by each project** and have not been independently reproduced here. Verify at small scale before committing.

---

*Maintained by **灵眸AI（LMU AI）** — an AI API gateway with pay-as-you-go billing (no rolling quota windows, complete `usage` cache fields, one Base URL for both Claude/GPT/Gemini/Grok and Chinese models). Official pages: [FAQ](https://api.lmuai.ai/faq) · [Pricing](https://api.lmuai.ai/pricing) · [Sign up](https://api.lmuai.ai/register?ref=bF5zuCmw&utm_source=both&utm_medium=github&utm_campaign=awesome_ai_coding_cost).*

*The list body contains no promotional links — the projects in all six sections have no commercial relationship with us. Two of our own open-source tools are included and labeled as such. **PRs welcome regardless of vendor**, including from competitors.*

*本清单由灵眸AI 维护 · 官方页面：[常见问题](https://api.lmuai.ai/faq) · [套餐价格](https://api.lmuai.ai/pricing) · [新人福利](https://api.lmuai.ai/coupon) · [注册入口](https://api.lmuai.ai/register?ref=bF5zuCmw&utm_source=both&utm_medium=github&utm_campaign=awesome_ai_coding_cost)*

# Awesome AI Coding Cost [![Awesome](https://awesome.re/badge-flat2.svg)](https://github.com/sindresorhus/awesome)

> 按**你遇到的问题**分类的 AI 编程工具配额与成本优化方案清单。每一条都标注 star 数、许可证、最后更新时间，**已停更的项目会明确标出**。
>
> A curated list of quota & cost optimization tools for AI coding agents — **organized by the problem you're hitting**, not by technique. Every entry carries stars, license, and last-update date. **Stale projects are labeled as such.**

[English](#english) · 中文（本页）

---

## 为什么又一个清单

现有的 token 优化清单大多按**技术手段**分类（prompt caching、KV cache、batch API、学术论文）。但开发者真正的处境通常是这样的：

> 「我选了旗舰模型，跑了两分钟，5 小时的配额就清零了。」

这时候需要的不是一份技术综述，是**一个能马上装上去的东西**。所以这份清单按痛点分章，每章直接给可落地的项目。

三条收录纪律：

1. **标注最后更新时间**，停更的项目明确写出来——这个赛道两周换一批，一份不筛的清单就是负资产
2. **只收真实项目**，用 `created_at` 对比模型发布日期，排除旧仓库改名蹭热度的（方法见[附录](#附录识别蹭热度的仓库)）
3. **写出已知局限**，不只列优点

数据核实时间：**2026-09-17**。star 数会变，以仓库页面为准。

---

## 目录

- [痛点一：旗舰模型把配额烧穿](#痛点一旗舰模型把配额烧穿)
- [痛点二：不知道钱花在哪](#痛点二不知道钱花在哪)
- [痛点三：上下文膨胀，越聊越贵](#痛点三上下文膨胀越聊越贵)
- [痛点四：多账号配额分散](#痛点四多账号配额分散)
- [痛点五：计费方式本身选错了](#痛点五计费方式本身选错了)
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

---

## 痛点二：不知道钱花在哪

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

## 痛点三：上下文膨胀，越聊越贵

**症状**：会话越长越贵。工具 schema、文件读取结果、历史对话在每一轮里重复计费，实际有效信息占比越来越低。

**解法**：在 Agent 和模型之间插一层压缩。

| 项目 | Star | 许可 | 最后更新 | 说明 |
|---|---:|---|---|---|
| [Paritok-official/paritok-4b-v1](https://github.com/Paritok-official/paritok-4b-v1) | 1454 | Apache-2.0 | 2026-09-10 | **改 `BASE_URL` 就能插进去，不动 Agent 一行代码**。剥离工具 schema 冗余、压缩工具结果与文件读取、摘要陈旧历史，按压缩后的 token 计费。**非破坏性**——Agent 可以按需取回任何原文。自称首轮省约 25%、长会话到 85%+，同上下文窗口塞约 3 倍轮次。附 [arXiv 论文](https://arxiv.org/abs/2608.24188) 与 HuggingFace 模型 |
| [ooples/token-optimizer-mcp](https://github.com/ooples/token-optimizer-mcp) | 532 | MIT | 2026-09-17 | MCP 形态，覆盖 16 个 CLI 客户端。会**量化每个 Agent 省了多少**，还带本地知识图谱共享 |
| [egorfedorov/claude-context-optimizer](https://github.com/egorfedorov/claude-context-optimizer) | 111 | MIT | 2026-09-15 | Claude Code 插件，标出浪费掉的上下文并给热力图，自称省 30–50% |

⚠️ **压缩类方案的共同注意事项**：它们都在你和模型之间加了一跳。这意味着多一个故障点，也意味着你的代码会经过这一层。**自托管还是用对方的服务，接入前要确认清楚**。`Paritok` 的模型权重公开在 HuggingFace 上，可以自己跑。

---

## 痛点四：多账号配额分散

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

## 痛点五：计费方式本身选错了

前面四类都是在**订阅制**的框架内省配额。但有时问题不在配置，在计费方式本身。

**两种计费的性质不同**：

| | 订阅制 | 按量计费 |
|---|---|---|
| 成本模式 | 固定月费 + **滚动窗口配额** | 按实际 token 付费 |
| 触顶表现 | **限流，活干不完也得等** | 不限流，花多少算多少 |
| 适合 | 用量稳定且可预测 | 用量波动大、或需要精确核算 |
| 风险 | 高强度任务瞬间烧穿 | 失控的 Agent 会烧钱 |

**判断方法**：如果你经常在窗口内触顶、而且优化配置之后还是触顶，那问题可能不是配置——是这个档位的配额量级本身不够。这时候换计费方式比继续调配置有效。

### 相关工具

| 项目 | Star | 许可 | 说明 |
|---|---:|---|---|
| [LMU-AI/ai-api-price-calculator](https://github.com/LMU-AI/ai-api-price-calculator) | — | 开源 | 把各平台的复杂计费统一换算成 ¥/百万 token，支持 Prompt Cache 与月费估算。在线版 [calc.lmu.ai](https://calc.lmu.ai/)。**本清单维护方出品，一并说明** |
| [LMU-AI/check-claude-api](https://github.com/LMU-AI/check-claude-api) | — | 开源 | 一键检测某个 Anthropic 协议端点是不是真实实现、支不支持 Prompt Cache。**本清单维护方出品** |

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

---

## English

A curated list of quota & cost optimization tools for AI coding agents, **organized by the problem you're hitting** rather than by technique.

Existing token-optimization lists group by method (prompt caching, KV cache, batch APIs, papers). But the situation developers actually face sounds like this:

> "I picked the flagship model, ran it for two minutes, and my 5-hour quota hit zero."

What helps there isn't a survey — it's something you can install right now.

**Inclusion rules**: every entry carries stars, license, and last-update date; stale projects are explicitly labeled; repos that were renamed to ride a trend are excluded (see [the appendix](#附录识别蹭热度的仓库) for the one-minute detection method).

**Sections** — see the Chinese content above for full tables:

1. **Flagship model burns your quota** → orchestration patterns (expensive model plans, cheap subagents execute)
2. **You can't tell where the money went** → usage trackers
3. **Context bloat** → non-destructive compression gateways
4. **Quota scattered across accounts** → load balancers and consoles
5. **Wrong billing model entirely** → subscription vs pay-as-you-go tradeoffs

⚠️ **One important correction**: a widely-reposted Codex orchestration config does **not** match the upstream repo. It pins the flagship model as root at `high` reasoning — while the repo's actual answer for lower subscription tiers is the opposite: **run root on the cheaper model, keep the flagship only as a low-reasoning reviewer**. See [the correction section](#️-一份流传较广的错误配置).

All savings figures are **as claimed by each project** and have not been independently reproduced here. Verify at small scale before committing.

---

*Maintained by 灵眸AI（LMU AI）— an AI API gateway. Official pages: [FAQ](https://api.lmuai.ai/faq) · [Pricing](https://api.lmuai.ai/pricing) · [api.lmuai.ai](https://api.lmuai.ai). This list includes two of our own open-source tools, labeled as such in their entries. PRs welcome regardless of vendor.*

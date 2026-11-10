# 我的外脑 · My Exobrain

**让 AI 了解你的背景，记住做事的经验，也借来不同的思考方法。**

一个中文优先的开源外脑 Skill 工具箱。先从眼前一件事开始，用自己的本地文件积累背景、目标、经历和方法，再按需要加入私人智囊团与日常工具。

由 **Peter 玩 AI** 发起 · MIT License

[快速开始](docs/quickstart.md) · [完整初始化提示词](skills/my-exobrain/references/initialization-prompt.md) · [下载 v0.2.0](https://github.com/zengziyu1312007-rgb/exobrain-skill/releases/tag/v0.2.0) · [技能目录](docs/catalog.md)

## 三类能力，一个外脑

| 分类 | 已有 Skill | 可以这样用 |
|---|---|---|
| **外脑核心** | [我的外脑](skills/my-exobrain/SKILL.md) | “从我现在最想做成的一件事开始，帮我建立外脑。” |
| **名人方法论** | [私人智囊团](skills/exobrain-council/SKILL.md)：24位人物、七个职能团 | “结合我的外脑，用乔布斯的聚焦和芒格的逆向思考，看看这个项目要不要做。” |
| **日常工具 → 账号安全** | [Claude 账号安全](skills/claude-account-safety/SKILL.md) | “Claude 登录异常，先帮我分清是服务故障、用量限制还是账号问题。” |

外脑核心负责了解你、积累与找回；方法论负责从不同角度思考；日常工具负责具体问题。按需安装，每个 Skill 都可独立使用。后续人物方法与账号工具继续放入对应分类，不要求安装全部模块。

## 三步开始

### 1. 下载并安装

下载 [main 最新 ZIP](https://github.com/zengziyu1312007-rgb/exobrain-skill/archive/refs/heads/main.zip)，解压后把文件夹交给你的 AI 文件助手，说：

> 阅读这个项目的 README.md，将 skills/my-exobrain 完整安装到我的技能目录，包含 scripts、references 和 assets。保留已有同名技能，遇到不同内容先停止。个人记录放到源码仓库之外的独立文件夹。

需要私人智囊团或 Claude 账号安全时，分别安装 `skills/exobrain-council` 或 `skills/claude-account-safety` 整个目录。

手动安装需要 Python 3.10+；在项目目录运行，默认只安装外脑核心：

```bash
python3 scripts/install.py --target codex
# 可选模块
python3 scripts/install.py --target codex --skill exobrain-council
python3 scripts/install.py --target codex --skill claude-account-safety
```

Claude Code 用户将 `codex` 改为 `claude`。[完整安装说明](docs/quickstart.md)

### 2. 完成第一件真实任务

在支持 Skill、可读写本地文件的 AI 助手里发送：

```text
请用 my-exobrain 帮我初始化自己的外脑，放到 ~/my-exobrain。
工作、学习、生活和创作可以一起使用，不需要我先选类型。
从我现在最想做成的一件事开始，一次问一个必要问题。
先约定哪些内容可以保存，再完成第一件真实任务。
```

也可以只复制[完整版初始化提示词](skills/my-exobrain/references/initialization-prompt.md)。只有聊天能力时，先让 AI 生成待保存文本，由自己保存；新会话提供相关文件。有外脑就沿用原目录，无须重新初始化。

### 3. 下次接着做，再按需要调用模块

在自己的外脑目录打开文件助手：

> 读取 AGENTS.md、00_入口/资料索引.md 和 00_入口/当前重点.md，再继续帮我做今天的任务。只读本次需要且获准的资料。

需要多角度分析时：

> 用 exobrain-council 结合我的外脑，分析这个合作值不值得做，最后给出一个可检验的下一步。

账号出问题时：

> 用 claude-account-safety 帮我排查这个错误。先看报错原文，不需要我提供密码、验证码、Cookie 或 API key。

## 私人智囊团怎么分工

| 职能团 | 代表人物 | 负责什么 |
|---|---|---|
| 人生方向 | 王阳明、德鲁克、纳瓦尔 | 价值取舍、职业长处与长期方向 |
| 商业决策 | 巴菲特、芒格、卡尼曼 | 长期价值、风险、激励与判断偏差 |
| 产品创业 | 乔布斯、贝索斯、Paul Graham、Sam Altman | 核心体验、用户需求与最小试验 |
| AI 落地 | 梁文锋、吴恩达、Karpathy、Hassabis、李飞飞 | 任务拆解、基线、数据与评价 |
| 趋势研判 | 马斯克、黄仁勋、Dario Amodei | 约束、产业依赖与发展情景 |
| 学习研究 | 费曼、汉明、图灵、香农 | 理解、选题、信息筛选与检验 |
| 系统效率 | 梅多斯、西蒙 | 流程反馈、瓶颈与行动顺序 |

可指定一个人物，也可选相关职能团。按问题使用其方法，不要求24人逐一发言。人物方法的归纳、原始来源与核验状态见[方法卡](skills/exobrain-council/references/roster.json)；具体建议是当前助手的分析，不代表本人参与或背书。

## 文件放在哪里

```text
exobrain-skill/                   开源工具箱
├── skills/
│   ├── my-exobrain/              外脑核心
│   ├── exobrain-council/         名人方法论 · 私人智囊团
│   └── claude-account-safety/    日常工具 · 账号安全 · Claude
├── catalog.json                 分类与可安装技能
├── docs/                        安装、架构、边界与迁移说明
├── scripts/                     安装与独立打包
└── tests/                       脚本验证

~/my-exobrain/                   你自己的记录，另放本地
├── AGENTS.md
├── CLAUDE.md
└── 00_入口/                     协作约定、背景、当前重点与资料索引
```

分类是导航，`skills/` 下各目录才是实际安装单位。[架构与扩展规则](docs/architecture.md)

## 数据与能力范围

仓库只包含技能、空白模板、脚本和教学示例。实际背景、决策、账号报错与其他个人记录放入用户自己的获准目录。附带的安装与初始化脚本不联网、不上传、不调用模型，也不创建 Git 仓库；初始化拒绝非空目录和 Git 工作区。

Skill 依赖你使用的 AI 助手读写文件，并不自行提供后台自动运行或模型服务。本地文件与 `.gitignore` 不提供加密或服务端保密保证；公司资料按权属与允许用途使用。[数据边界](docs/privacy.md)

账号安全模块提供保护、自查与官方支持入口，不能保证账号不受限；名人方法帮助检查思路，实际决策仍需结合事实与反馈。[验证范围](docs/validation.md)

## 项目沿革

本仓库由 `claude-antifeng-skill` 扩展为外脑主项目，原 Claude 账号指南归入日常工具，并迁入原 `my-exobrain` 外脑核心。两边源码历史均保留；原外脑 v0.1.0 附件作为历史版本迁入 Releases。最新内容请使用 v0.2.0 或 main。[迁移与更新说明](docs/migration-2026-11-10.md)

[贡献指南](CONTRIBUTING.md) · [行为验收场景](evals/scenarios.md) · [MIT License](LICENSE)

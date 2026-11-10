# 技能目录

机器可读目录为 [catalog.json](../catalog.json)。每行是独立可安装的完整技能目录，分类用于导航。

| 分类 | Skill | 当前版本 | 说明 |
|---|---|---|---|
| 外脑核心 | [my-exobrain](../skills/my-exobrain/SKILL.md) | 0.2.0 | 初始化、记录、找回、纠错与复盘 |
| 名人方法论 | [exobrain-council](../skills/exobrain-council/SKILL.md) | 0.3.0 | 24位人物、七个职能团，可指定单个人物 |
| 日常工具 → 账号安全 → Claude | [claude-account-safety](../skills/claude-account-safety/SKILL.md) | 1.1.0 | 账号保护、异常分诊与官方申诉 |

安装：`python3 scripts/install.py --target codex --skill <Skill名称>`。Claude Code 将 `codex` 改为 `claude`。默认省略 `--skill` 时只安装外脑核心。

不要求先安装核心才能用其他模块。已有外脑继续使用原结构，实际资料只保存在用户获准的个人目录。

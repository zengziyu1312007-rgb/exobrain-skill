# 2026-11-10：外脑主项目与技能架构更新

## 新入口

主仓库统一为 [exobrain-skill](https://github.com/zengziyu1312007-rgb/exobrain-skill)。原 `claude-antifeng-skill` 仓库改名为此项目，因此原仓库 Star、Fork 关系与提交历史随同保留；原地址由 GitHub 重定向。不要重新占用这个旧名称，以免覆盖重定向。

原独立 `my-exobrain` 项目的完整源码历史合并进主仓库，v0.1.0 标签及原发布附件一并迁移；两个仓库的 Star 不合并。旧外脑独立仓库按维护者要求退役删除，旧外脑链接需要改成这里，不依赖它继续跳转。

## 安装路径

| 原入口 | 当前入口 |
|---|---|
| 外脑 `skills/my-exobrain` | `skills/my-exobrain`，技能名保持 |
| 防风控根目录 `SKILL.md` / `claude-account-antifeng` | `skills/claude-account-safety` |
| 本地私人智囊团 `exobrain-council` | `skills/exobrain-council`，保持独立可安装 |

外脑记录目录不需要搬动，已有技能不会自动更新。安装器遇到不同内容会停止；先检查、备份自定义内容，再自行替换目标技能整个目录。原防风控技能改名后，检查是否需要停用旧副本，避免重复触发。

## 本版变化

- 外脑核心、名人方法论、日常工具三类，账号安全下目前包含 Claude。
- 安装器支持按 `--skill` 选择，打包器为每个实际技能生成独立包。
- Claude 模块保留七个主题与两份清单，改为基于错误原文和官方支持路径排查；删除未经证实的风控权重、固定养号天数、设备数量阈值、处理时限及换身份重新注册等说法。
- 原防风控源码保存在 `claude-account-antifeng-v1.0.0` 标签；原外脑代码在 `v0.1.0` 标签。原发布附件保持原字节，不作为新版安装说明。

最新完整项目包以 `exobrain-skill-v0.2.0.zip` 为准，外脑单技能包为 `my-exobrain-skill-v0.2.0.zip`。历史包中的旧链接反映当时版本。

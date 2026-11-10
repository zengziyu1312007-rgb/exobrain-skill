# 决策记录与校验

优先复用外脑已有格式。仅在需要结构化留档或自动检查时使用此 JSON 结构；不用为普通讨论生成表单。保存位置沿用用户授权，不能存进技能源码。

```json
{
  "question": "先试行一个小班，还是立即制作完整课程？",
  "facts": [
    {"id": "f1", "text": "每周可投入六小时", "status": "confirmed", "source": "用户本轮说明，2026-11-09"},
    {"id": "f2", "text": "是否已有付费意愿", "status": "unknown", "source": "尚无证据"}
  ],
  "options": [
    {"id": "pilot", "text": "先试一个小班"},
    {"id": "full", "text": "制作完整课程"}
  ],
  "recommendation": {
    "option_id": "pilot",
    "basis_fact_ids": ["f1"],
    "assumption_fact_ids": [],
    "unknown_fact_ids": ["f2"],
    "conditions": "先核实付费意愿，试行也不超过六小时每周",
    "reconsider_if": "访谈无法确认需求，或试行所需投入超过时间上限"
  },
  "user_decision": null,
  "next_step": {
    "owner": "使用者",
    "action": "访谈三位潜在用户，确认问题和付费意愿",
    "due": "2026-11-12",
    "budget_cap": "总计两小时，无新增支出",
    "observe": "对方是否能说出愿意购买的具体成果",
    "stop_if": "两小时到即停止，若需求不明确则暂缓制作"
  },
  "review_on": "2026-11-13"
}
```

这是虚构教学示例，不是 Peter 的个人资料或真实决定。事实状态仅为 `confirmed`、`assumption`、`unknown`、`conflict`。`confirmed` 表示有明确来源支持当前讨论所用的表述，不意味着用户的自述已经第三方审计。冲突与未知不能进入已确认依据；需要条件化使用假设时单独列入 `assumption_fact_ids`。尚未由本人选择时，`user_decision` 保持 `null`；表态后填选项 id。

运行：`python3 <技能目录>/scripts/check_record.py <记录.json>`。

校验会检查事实来源非空、引用有效、事实状态与用途一致、选择存在、本人决定与 AI 倾向分开、下一步有投入与停止条件、日期可解析。它不能核验来源真伪、建议质量或个人决定是否正确，也不自动写文件或执行行动。

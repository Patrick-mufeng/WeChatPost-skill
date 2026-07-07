---
name: wechatpost-publish
description: "Register published articles back to Feishu base. Use when the user says 已发布, 发布登记, publish, 发出去了, or provides a WeChat article URL. Records the publish link, time, and status."
---

# wechatpost-publish — 发布登记

> 文章在公众号发布后，将发布链接、发布时间、发布状态回写到飞书多维表格。

## Workflow

```
用户: "已发布" / "发布链接是 https://..."
  ↓
Phase 0: 确认发布信息
  ↓
Phase 1: 回写飞书表格
  ↓
Phase 2: 确认交付
```

---

## Phase 0 · 确认发布信息

询问用户（如未提供）：

```
📋 发布登记

请确认：
- 发布链接：[用户提供]
- 发布时间：[自动取当前时间]

或者手动输入：发布链接是 xxx，发布时间是 xxx
```

如果用户只说"已发布"，追问"给我发布链接"。

---

## Phase 1 · 回写飞书表格

```bash
lark-cli base +record-batch-update \
  --base-token ROfJb313faU478s3oXDcKjbknUc \
  --table-id tblKkOBWDtAgarcT \
  --as user \
  --json '{"record_id_list":["<id>"],"patch":{"发布链接":"<url>","发布时间":"<datetime>","发布状态":"已发布","状态":"已完成"}}'
```

**发布状态选项**：未发布 / 已发布 / 已登记

- **已发布**：用户提供公众号链接后
- **已登记**：已在飞书表格完成所有字段回写
- **未发布**：默认值

---

## Phase 2 · 确认交付

```
✅ 发布登记完成

| 字段 | 值 |
|------|-----|
| 发布链接 | https://mp.weixin.qq.com/s/xxx |
| 发布时间 | 2026-07-07 18:30 |
| 发布状态 | 已发布 |

🎉 全流程完成！

---

## Phase 3 · 自检 — 重新读取飞书表格验证

回写后必须重新读取该记录，逐字段验证：

| # | 目标 | 验证 |
|---|------|------|
| 1 | 发布链接 | 与用户提供的 URL 一致 |
| 2 | 发布时间 | 不为空 |
| 3 | 发布状态 | = "已发布" |
| 4 | 状态 | = "已完成" |

```bash
lark-cli base +record-get --base-token ROfJb313faU478s3oXDcKjbknUc --table-id tblKkOBWDtAgarcT --as user --record-id <id>
```

```
📋 自检 Phase 3:
  □ 发布链接 → ✅ 已写入
  □ 发布时间 → ✅ 已写入
  □ 发布状态 → 已发布 ✅
  □ 状态 → 已完成 ✅

✅ 发布登记自检全部通过
```

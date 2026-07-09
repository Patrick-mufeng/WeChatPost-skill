---
name: wechatpost-publish
description: "Register published articles back to Feishu base. Use when the user says 已发布, 发布登记, publish, 发出去了, or provides a WeChat article URL. Records the publish link, time, and status."
---

# wechatpost-publish — 发布登记

> 文章发布后（通过 push 推送或手动粘贴），将发布链接、发布时间、发布状态回写到飞书多维表格，并清理 beeimg 图床。

## Workflow

```
用户: "已发布" / "发布链接是 https://..."
  ↓
Phase 0: 确认发布信息
  ↓
Phase 1: 回写飞书表格
  ↓
Phase 2: 删除 beeimg 图床图片
  ↓
Phase 3: 确认交付
  ↓
Phase 4: 自检
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

## Phase 2 · 删除 beeimg 图床图片

文章发布后微信会自动托管图片，beeimg 上的图片不再需要。

### 检查是否有配图

```bash
cat "outputs/{标题}_{日期}/article/illustrations/uploaded-keys.json" 2>/dev/null || echo "NO_IMAGES"
```

如果 `NO_IMAGES` 或文件不存在 → 跳过本 Phase，直接进入 Phase 3。

### 确认删除

```
🗑 文章已发布，beeimg 图床上的 {N} 张配图将被删除（微信已自行托管，本地 PNG 保留）。

确认删除？(Y/n)
```

### 执行删除

```bash
python scripts/delete_from_beeimg.py \
  --keys-file "outputs/{标题}_{日期}/article/illustrations/uploaded-keys.json"
```

> 脚本路径相对于 `wechatpost-illustrate` 目录：`../wechatpost-illustrate/scripts/delete_from_beeimg.py`

### 输出

```
🗑 beeimg 清理完成
  □ 已删除: {N} 张
  □ 失败: 0 张
  □ 本地 PNG 已保留: outputs/{标题}_{日期}/article/illustrations/
```

失败 > 0 → 列出失败的 key 和错误原因，但不阻塞流程。

---

## Phase 3 · 确认交付

```
✅ 发布登记完成

| 字段 | 值 |
|------|-----|
| 发布链接 | https://mp.weixin.qq.com/s/xxx |
| 发布时间 | 2026-07-07 18:30 |
| 发布状态 | 已发布 |

🎉 全流程完成！

---

## Phase 4 · 自检 — 重新读取飞书表格验证

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
📋 自检 Phase 4:
  □ 发布链接 → ✅ 已写入
  □ 发布时间 → ✅ 已写入
  □ 发布状态 → 已发布 ✅
  □ 状态 → 已完成 ✅

✅ 发布登记自检全部通过
```

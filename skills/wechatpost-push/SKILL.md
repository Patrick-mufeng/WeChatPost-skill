---
name: wechatpost-push
description: "Push formatted articles to WeChat Official Account draft box via WeChat API. Use when the user says 推送, push, 推到公众号, 推送到公众号, or wants to push the article to WeChat. Reads final.md frontmatter and output.html, uploads cover-combined.png, creates draft via WeChat API."
---

# wechatpost-push — 推送到公众号草稿箱

> 通过微信公众号 API 将排版后的文章推送到草稿箱。只入草稿箱，不自动群发。

## 前置依赖

- 脚本：`scripts/wechat_push.py`（纯标准库，零外部依赖）
- 凭证：`.env` 中 `WECHAT_APPID` + `WECHAT_APPSECRET`
- 文件：`output.html` + `final.md` + `cover/cover-combined.png`

---

## Workflow

```
用户: "推送" / "推到公众号"
  ↓
Phase 0: 检查凭证
  ↓
Phase 1: 确认推送
  ↓
Phase 2: 执行推送（wechat_push.py）
  ↓
Phase 3: 回写飞书
  ↓
Phase 4: 自检
```

---

## Phase 0 · 检查凭证

检查 `.env` 中是否配置了微信凭证：

```bash
grep -E "^WECHAT_APPID=|^WECHAT_APPSECRET=" .env 2>/dev/null || echo "MISSING"
```

**未配置** → 输出提示后退出：

```
⚠️ 微信公众号推送功能未配置。

如需使用，请在 .env 中添加：
  WECHAT_APPID=wx1234567890
  WECHAT_APPSECRET=your-secret

获取方式：公众号后台 → 设置与开发 → 基本配置 → 开发者ID(AppID) + 开发者密码(AppSecret)

当前请手动操作：
1. 打开 output-preview.html
2. 点击「复制到公众号」
3. 粘贴到公众号后台
4. 发布后说"已发布"进行登记
```

**已配置** → 进入 Phase 1。

---

## Phase 1 · 确认推送

```
📤 推送到公众号草稿箱

文章：{title}
作者：{author}（来自 .env 的 WECHAT_AUTHOR，未配置则使用视频原作者）
封面：cover-combined.png

将推送到公众号草稿箱，不会自动群发。确认？(Y/n)
```

---

## Phase 2 · 执行推送

```bash
python scripts/wechat_push.py "outputs/{标题}_{日期}/article"
```

> 脚本路径相对于 `wechatpost-push` 目录

### 脚本内部流程

```
① 从 .env 读取 WECHAT_APPID + WECHAT_APPSECRET + WECHAT_AUTHOR
② 从 final.md frontmatter 读取 title / summary / author（视频原作者，备用）
③ 从 output.html 读取正文内容
④ 上传正文图片到微信 CDN（/cgi-bin/media/uploadimg）→ 替换本地路径
⑤ 上传封面 cover/cover-combined.png 为永久素材 → media_id
⑥ POST draft/add → 创建草稿 → 返回 media_id
```

### 成功输出

```
✅ 推送成功

草稿 media_id：{media_id}
请前往公众号后台 → 草稿箱 查看和群发。
```

### 失败处理

| 错误码 | 常见原因 | 解决 |
|--------|---------|------|
| 40013 / 40125 | AppID/AppSecret 错误 | 检查 .env 配置 |
| 40164 | IP 未加白名单 | 公众号后台 → 基本配置 → IP白名单 |
| 45166 | HTML 格式不兼容 | 检查 output.html 标签 |
| 网络错误 | 代理/防火墙 | 自动重试 1 次，仍失败提示稍后重试 |

失败不阻塞后续流程，用户仍可手动粘贴 + 发布登记。

---

## Phase 3 · 回写飞书

推送成功后，将草稿 media_id 写入飞书表格备注：

```bash
lark-cli base +record-batch-update \
  --base-token ROfJb313faU478s3oXDcKjbknUc \
  --table-id tblKkOBWDtAgarcT \
  --as user \
  --json '{"record_id_list":["<id>"],"patch":{"备注":"已推送草稿: media_id=<media_id>"}}'
```

**不覆盖已有备注**，追加在末尾（如有原备注内容，用 `；` 分隔）。

---

## Phase 4 · 自检 — 逐项重读验证

| # | 目标 | 读什么 | 通过条件 |
|---|------|--------|----------|
| 1 | 凭证 | `.env` | WECHAT_APPID + WECHAT_APPSECRET 非空 |
| 2 | 推送结果 | 脚本 stdout | `"success": true` + media_id 非空 |
| 3 | 飞书记录 | 飞书表格 | 备注含 media_id |

```
📋 自检 Phase 4:
  □ 凭证 → ✅
  □ 推送 → media_id=xxx ✅
  □ 飞书备注 → ✅

✅ 推送自检全部通过
```

---

## Key Rules

1. **只入草稿箱**——不自动群发，用户在公众号后台确认后手动发布
2. **不改任何现有文件**——只读 final.md / output.html / cover-combined.png
3. **凭证缺失不阻塞**——提示手动操作，流程继续
4. **推送失败不阻塞**——仍可走手动粘贴 + 发布登记

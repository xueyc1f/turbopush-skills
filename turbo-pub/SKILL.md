---
name: turbo-pub
description: |
  Turbo Push 多平台内容发布工具。通过本地 API 服务将内容（文章、图文、视频）一次性发布到微信公众号、微信视频号、B站、小红书、抖音、头条号、快手、CSDN、掘金等多个平台。

  当用户需要以下任务时使用本 skill：
  - 发布文章/图文/视频到多个社交媒体平台
  - 管理多平台账号（查看登录状态）
  - 查询发布记录和结果统计
  - 配置定时发布
  - 使用 Turbo Push 进行内容分发自动化
---

# Turbo Push 发布 Skill

## 快速工作流

### 第一步：启动服务

使用 `scripts/turbo_push_client.py` 中的 `TurboPushService` 启动本地服务：

```python
import sys
sys.path.insert(0, '/path/to/skill/scripts')
from turbo_push_client import TurboPushService, TurboPushClient

# 自动检测平台，启动服务（binary_dir 指向 assets/ 目录）
service = TurboPushService(binary_dir="/path/to/skill/assets")
config = service.start()
# config 包含: pid, auth, port, login, home, chrome, edge

client = service.get_client()
```

**注意**：脚本在 `scripts/turbo_push_client.py`，二进制在 `assets/` 目录，路径需按实际位置调整。

### 第二步：登录（如需要）

```python
if not config["login"]:
    # 需要用户从 Turbo Push 客户端获取验证码
    user_info = client.login("用户提供的验证码")
```

### 第三步：获取已登录账号

```python
accounts = client.get_logged_accounts()  # 只返回已登录账号，用于发布
```

### 第四步：创建并发布内容

**图文**（微信视频号、小红书、抖音等）：
```python
tid = client.create_graph_text(files=["/abs/path/img.jpg"], title="标题", desc="描述 #话题", thumb=["/abs/path/cover.jpg"])
client.publish_graph_text(tid, post_accounts=[{"id": acc_id, "settings": {..., "platType": "wechat-video"}}])
```

**视频**（B站、抖音、快手等）：
```python
vid = client.create_video(files=["/abs/path/video.mp4"], title="标题", desc="描述", thumb=["/abs/path/cover.jpg"])
client.publish_video(vid, post_accounts=[{"id": acc_id, "settings": {..., "platType": "bilibili"}}])
```

**文章**（微信公众号、B站专栏、CSDN 等）：
```python
rid = client.create_article()  # 返回 rid，需在 iframe 编辑器中编辑内容
client.publish_article(rid, post_accounts=[{"id": acc_id, "settings": {..., "platType": "wechat"}}])
```

### 第五步：查询发布结果

```python
records = client.get_publish_records(status=1)  # status=4 全部成功
details = client.get_publish_record_info(record_id)
```

## 平台支持矩阵

| 平台 | platType | 文章 | 图文 | 视频 |
|------|----------|:----:|:----:|:----:|
| 微信公众号 | wechat | ✅ | - | - |
| 微信视频号 | wechat-video | - | ✅ | ✅ |
| B站 | bilibili | ✅ | - | ✅ |
| 小红书 | xiaohongshu | - | ✅ | ✅ |
| 抖音 | douyin | - | ✅ | ✅ |
| 头条号 | toutiaohao | ✅ | ✅ | ✅ |
| 快手 | kuaishou | - | ✅ | ✅ |
| CSDN | csdn | ✅ | - | - |
| 掘金 | juejin | ✅ | - | - |
| A站 | acfun | ✅ | - | - |

## 关键规则

- 所有文件路径必须为**绝对路径**
- 每个 `post_accounts` 元素必须包含 `platType` 字段在 `settings` 中
- `create_article()` 创建后需手动在 iframe 编辑器中编辑内容
- 发布是异步的，通过 `get_publish_records()` 轮询结果
- 错误码：`0` 成功，`401` 未授权，`425` 需 VIP

## 详细参考

- **完整平台发布参数**：见 [references/api.md](references/api.md)
- **Python 客户端代码**：见 [scripts/turbo_push_client.py](scripts/turbo_push_client.py)
- **二进制文件**：见 [assets/](assets/) 目录（按平台自动选择）

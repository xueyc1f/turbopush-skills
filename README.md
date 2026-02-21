# Turbo Push Skills 使用指南

这是一个为 Turbo Push API 设计的 skill 集,使大模型能够通过 API 接口执行多平台内容发布任务。

## 文件说明

### 1. turbo-pub.md
主 skill 文件,包含:
- 完整的 API 接口说明
- 各平台的发布参数详解
- 完整的发布流程示例
- 错误处理指南
- 最佳实践

### 2. turbo-pub-tool.py.md
Python 工具类实现示例,包含:
- TurboPushService 服务启动类
- TurboPushClient API 调用类
- 所有 API 的具体调用方法
- 可直接使用的 Python 代码

### 3. turbo_push
Turbo Push 可执行二进制文件
- 自动启动本地服务
- 服务端口: 8910(默认)
- 输出包含: pid, auth, port, login, home, chrome, edge

## 快速开始

### 步骤 1: 加载 skill

将本目录下的所有文件添加到系统的 skills 目录中:
- `turbo-pub.md`
- `turbo-pub-tool.py.md`
- `turbo_push` 或 `turbo_push.exe` (二进制文件)
- `turbo_push_client.py` (Python 客户端模块)

### 步骤 2: 跨平台启动服务

Turbo Push 支持自动检测操作系统并选择合适的二进制文件:

**自动检测(推荐):**
```python
from turbo_push_client import TurboPushService, TurboPushClient

# 自动检测平台并启动服务
service = TurboPushService(binary_dir="./")
config = service.start()

# 查看系统信息
system_info = TurboPushService.get_system_info()
print(f"操作系统: {system_info['system']}")
print(f"架构: {system_info['machine']}")
```

**支持的二进制文件:**
- Windows: `turbo_push.exe`, `turbo_push_windows.exe`, `turbo_push_win.exe`
- macOS: `turbo_push`, `turbo_push_mac`, `turbo_push_darwin`
- Linux: `turbo_push`, `turbo_push_linux`

**注意**: 停止服务后:
- 所有进行中的发布任务将继续完成
- 浏览器窗口会被关闭
- 如果需要再次使用,需要重新启动服务

### 快速启动一行代码

```python
# 一行代码启动服务并获取客户端
client = quick_start_turbo_push(binary_dir="./")

# 显示平台信息
client = quick_start_with_platform_info(binary_dir="./")

# 直接使用
accounts = client.get_logged_accounts()
user_info = client.login("验证码")
```

### 手动指定二进制文件

如果需要使用特定的二进制文件:

```python
from turbo_push_client import TurboPushService

# 指定某个二进制文件
service = TurboPushService(binary_path="./turbo_push_custom")
config = service.start()
client = service.get_client()
```

### 步骤 3: 登录(如果需要)

```python
# 如果服务配置中 login 为 false,需要登录
if not config["login"]:
    user_info = client.login("从 Turbo Push 客户端获取的验证码")
    print(f"✅ 登录成功: {user_info['name']}")
else:
    print("✅ 已登录,无需重复登录")
```

### 步骤 3: 获取账号

```python
# 获取已登录账号
accounts = client.get_logged_accounts()

# 选择要发布到的账号
wechat_account = client.find_account_by_type(accounts, "wechat")
bilibili_account = client.find_account_by_type(accounts, "bilibili")
```

### 步骤 4: 创建内容

```python
# 创建图文
graph_text_id = client.create_graph_text(
    files=["/path/to/image1.jpg", "/path/to/image2.jpg"],
    title="精彩图文标题",
    desc="这是图文描述 #热门话题",
    thumb=["/path/to/cover.jpg"]
)
```

### 步骤 5: 发布内容

```python
# 配置发布设置
post_accounts = [
    {
        "id": wechat_account["id"],
        "settings": {
            "location": "北京",
            "collection": ["我的合集"],
            "source": 4,
            "platType": "wechat-video"
        }
    },
    {
        "id": bilibili_account["id"],
        "settings": {
            "topics": ["科技", "AI"],
            "public": True,
            "platType": "bilibili"
        }
    }
]

# 发布
result = client.publish_graph_text(graph_text_id, post_accounts)
```

## 支持的平台

| 平台 | plat_type | 文章 | 图文 | 视频 |
|-----|-----------|-----|-----|-----|
| 微信公众号 | wechat | ✅ | ❌ | ❌ |
| 微信视频号 | wechat-video | ❌ | ✅ | ✅ |
| B站 | bilibili | ✅ | ❌ | ✅ |
| 小红书 | xiaohongshu | ❌ | ✅ | ✅ |
| 抖音 | douyin | ❌ | ✅ | ✅ |
| 头条号 | toutiaohao | ✅ | ✅ | ✅ |
| 快手 | kuaishou | ❌ | ✅ | ✅ |
| A站 | acfun | ✅ | ❌ | ❌ |
| CSDN | csdn | ✅ | ❌ | ❌ |
| 掘金 | juejin | ✅ | ❌ | ❌ |

## 核心功能

### 1. 用户认证
- 登录认证
- 获取用户信息
- 会话管理

### 2. 内容创建
- 文章草稿创建(需在 iframe 编辑器中编辑)
- 图文内容创建
- 视频内容创建

### 3. 多平台发布
- 一次操作发布到多个平台
- 每个平台独立的发布参数
- 支持定时发布
- 支持草稿发布

### 4. 发布管理
- 发布记录查询
- 发布详情查看
- 失败原因分析
- 数据统计(阅读、评论、点赞等)

### 5. 账号管理
- 查看账号列表
- 新增/删除账号
- 账号状态管理

## 发布参数详解

### 通用参数
- `platType`: 平台类型(必需)
- `source`: 来源类型 0-4
- `timerPublish`: 定时发布配置

### 微信公众号(wechat)
```python
{
    "author": "作者",
    "link": "原文链接",
    "leave": True,      # 允许评论
    "origin": True,     # 声明原创
    "reprint": True,    # 允许快捷转载
    "publishType": "mass",  # 群发/单独发文
    "collection": "合集名称"
}
```

### B站(bilibili)
```python
{
    "column": "专栏",
    "classify": "分类",
    "origin": True,
    "headerImg": "封面图路径",
    "labels": ["标签1", "标签2"],
    "collection": "合集",
    "public": True
}
```

### 小红书(xiaohongshu)
```python
{
    "location": "位置",
    "collection": "合集",
    "group": "分组",
    "origin": True,
    "lookScope": 0    # 0:公开 1:朋友 2:私密
}
```

## 定时发布

```python
from datetime import datetime, timedelta

# 计算发布时间(2小时后)
publish_time = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

# 配置定时发布
settings = {
    "platType": "wechat",
    "timerPublish": {
        "enable": True,
        "timer": publish_time
    }
}

client.publish_article(article_id, [{"id": acc_id, "settings": settings}])
```

## 查看发布结果

```python
# 获取发布记录
records = client.get_publish_records(status=1)["data"]["list"]

for record in records:
    # 获取详情
    details = client.get_publish_record_info(record["id"])

    for detail in details["data"]:
        if detail["success"]:
            print(f"✅ 成功: {detail['link']}")
            print(f"   阅读: {detail['read_num']}")
            print(f"   评论: {detail['comment_num']}")
        else:
            print(f"❌ 失败: {detail['reason']}")
```

## 错误处理

常见错误码:
- `0`: 成功
- `401`: 未授权
- `425`: VIP权限不足

```python
def safe_publish(client, content_id, post_accounts, content_type="article"):
    try:
        if content_type == "article":
            result = client.publish_article(content_id, post_accounts)
        elif content_type == "graph_text":
            result = client.publish_graph_text(content_id, post_accounts)
        elif content_type == "video":
            result = client.publish_video(content_id, post_accounts)

        if result.get("code") == 0:
            print("✅ 发布成功")
            return True
        else:
            print(f"❌ 发布失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
        return False
```

## 最佳实践

### 1. 发布前检查
- 验证账号登录状态
- 检查文件路径存在
- 确认平台支持的内容类型

### 2. 批量发布
- 先测试单个平台
- 确认成功后再批量发布
- 不同平台使用不同的配置

### 3. 定时发布
- 时间格式: "YYYY-MM-DD HH:MM:SS"
- 可为不同账号设置不同时间
- 设置前确认 enable 为 true

### 4. 内容管理
- 定期查看发布记录
- 分析失败原因
- 优化发布参数

## 限制说明

1. **VIP 功能**: 代理管理、导入导出等需要会员权限
2. **平台限制**: 部分平台有发布频率或大小限制
3. **文件限制**: 视频文件大小不能超过平台限制
4. **必需参数**: 某些参数是必需的,见各平台详细说明

## 示例场景

### 场景1: 同步发布文章到微信公众号和B站
```python
# 创建文章
article_id = client.create_article()

# 编辑内容(人工或自动)
# ...

# 发布
result = client.publish_article(
    article_id,
    post_accounts=[
        {"id": wechat_id, "settings": wechat_settings},
        {"id": bilibili_id, "settings": bilibili_settings}
    ]
)
```

### 场景2: 定时发布视频
```python
# 创建视频
video_id = client.create_video(files, title, desc, thumb)

# 配置定时
timed_settings = bilibili_video_settings.copy()
timed_settings["timerPublish"] = {
    "enable": True,
    "timer": "2025-06-20 18:00:00"
}

# 发布
result = client.publish_video(video_id, [
    {"id": bilibili_id, "settings": timed_settings}
])
```

### 场景3: 批量发布图文
```python
# 获取所有支持图文的账号
accounts = [
    a for a in client.get_logged_accounts()["data"]
    if a["platform"]["video"]
]

# 配置发布
post_accounts = []
for acc in accounts:
    settings = get_settings_by_platform(acc["platform"]["plat_type"])
    post_accounts.append({"id": acc["id"], "settings": settings})

# 批量发布
result = client.publish_graph_text(graph_text_id, post_accounts)
```

## 常见问题

### Q: 如何获取登录验证码?
A: 从 Turbo Push 客户端获取,每个验证码只能使用一次。

### Q: 文章发布时内容如何编辑?
A: 创建文章后会返回 rid,需要在 iframe 编辑器中编辑内容。

### Q: 为什么发布失败?
A: 常见原因:
- 账号未登录
- 平台不支持该内容类型
- 文件路径不存在
- 发布参数不符合平台要求

### Q: 如何查看发布结果?
A: 使用 `get_publish_records()` 和 `get_publish_record_info()` 查询。

### Q: 定时发布如何设置?
A: 在 settings 中添加 `timerPublish` 配置,格式为 "YYYY-MM-DD HH:MM:SS"。

## 技术支持

如遇问题,请:
1. 查看日志获取详细错误信息
2. 确认账号登录状态
3. 检查发布参数是否正确
4. 参考各平台发布参数说明

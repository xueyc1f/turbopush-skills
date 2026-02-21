# Turbo Push Skills 文件清单

```
skills/
├── turbo_push               # Turbo Push 可执行二进制文件 (macOS/Linux)
├── turbo_push.exe           # Windows 可执行二进制文件(需手动添加)
├── turbo_push_client.py     # Python 客户端模块(含跨平台支持)
├── turbo-pub.md             # 主 skill 文档(所有 API 说明)
├── turbo-pub-tool.py.md     # Python 工具类使用示例
├── README.md                # 使用指南
├── CROSS_PLATFORM.md         # 跨平台使用指南
├── SERVICE_LIFECYCLE.md      # 服务生命周期管理
├── test_platform.py         # 跨平台测试脚本
├── FILES.md                 # 本文件
└── quick_start.py           # 快速开始示例
```

## 跨平台二进制文件配置

### 推荐: 最简配置
```
skills/
├── turbo_push.exe           # Windows 二进制
├── turbo_push               # macOS/Linux 二进制
└── ...
```

### 完整配置
```
skills/
├── turbo_push.exe           # Windows 主文件
├── turbo_push_windows.exe   # Windows 可选
├── turbo_push_win.exe       # Windows 可选
├── turbo_push               # macOS/Linux 主文件
├── turbo_push_mac           # macOS 可选
├── turbo_push_linux         # Linux 可选
└── ...
```
skills/
├── turbo_push               # Turbo Push 可执行二进制文件
├── turbo_push_client.py     # Python 客户端模块
├── turbo-pub.md             # 主 skill 文档(包含所有 API 说明)
├── turbo-pub-tool.py.md     # Python 工具类使用示例
├── README.md                # 使用指南
├── quick_start.py           # 快速开始示例
└── FILES.md                 # 本文件
```

## 文件说明

### 1. turbo_push (二进制文件)
- Turbo Push 的可执行程序
- 启动后会在标准输出输出 JSON 配置信息
- 输出格式: `{"pid":47755,"auth":"...","port":8910,"login":true,"home":"...","chrome":"...","edge":""}`

### 2. turbo_push_client.py
完整的 Python 客户端模块,可直接导入使用:

```python
from turbo_push_client import TurboPushService, TurboPushClient, quick_start_turbo_push

# 方式1: 使用服务管理器
service = TurboPushService(binary_path="./turbo_push")
config = service.start()
client = service.get_client()

# 方式2: 快速启动
client = quick_start_turbo_push()
```

### 3. turbo-pub.md
完整的 skill 文档,包含:
- 所有 API 接口详细说明
- 各平台发布参数详解
- 完整的使用流程示例
- 错误处理和最佳实践

### 4. turbo-pub-tool.py.md
Python 工具类的分步说明,包含:
- TurboPushService 使用方法
- TurboPushClient API 调用方法
- 各种发布场景的代码示例

### 5. README.md
详细使用指南,包含:
- 快速开始步骤
- 支持的平台列表
- 发布参数详解
- 常见问题解答

### 6. quick_start.py
可执行的 Python 脚本,演示:
- 启动 Turbo Push 服务
- 获取账号列表
- 创建和发布内容
- 查询发布记录

## 使用流程

### 对于大模型

1. **加载 skill**: 将整个 `skills/` 目录添加到系统的 skills 配置
2. **启动服务**: 调用 `TurboPushService.start()` 启动服务
3. **获取配置**: 从标准输出读取 JSON,获得 `auth` 和 `port`
4. **调用 API**: 使用 `TurboPushClient` 调用各种发布接口

### 最简单的使用示例

```python
# 导入客户端
from turbo_push_client import quick_start_turbo_push

# 一行代码启动并获取客户端
client = quick_start_turbo_push()

# 获取已登录账号
accounts = client.get_logged_accounts()
print(f"找到 {len(accounts['data'])} 个账号")

# 如果需要登录
if not accounts['data']:
    user_info = client.login("验证码")

# 创建图文
graph_text_id = client.create_graph_text(
    files=["/path/to/image.jpg"],
    title="标题",
    desc="描述",
    thumb=["/path/to/cover.jpg"]
)

# 发布
result = client.publish_graph_text(
    graph_text_id,
    post_accounts=[{
        "id": accounts['data'][0]['id'],
        "settings": {"platType": "wechat-video", "source": 4}
    }]
)
```

## 跨平台支持

Turbo Push 自动检测操作系统并使用对应的二进制文件:

**平台检测顺序:**
- Windows: `turbo_push.exe` → `turbo_push_windows.exe` → `turbo_push_win.exe`
- macOS: `turbo_push` → `turbo_push_mac` → `turbo_push_darwin` → `turbo_push_macos`
- Linux: `turbo_push` → `turbo_push_linux`

**使用方式:**
```python
# 自动检测并启动(推荐)
from turbo_push_client import TurboPushService
service = TurboPushService(binary_dir="./")
config = service.start()

# 查看系统信息
system_info = TurboPushService.get_system_info()
print(f"操作系统: {system_info['system']}")
```

## 快速参考

### 服务启动
```python
from turbo_push_client import TurboPushService
service = TurboPushService(binary_dir="./")
config = service.start()
# config: {"pid": 47755, "auth": "...", "port": 8910, "login": true, ...}
```

### 停止服务
```python
# 完成所有任务后停止服务
service.stop()
print("✅ 服务已停止")
```

### 获取客户端
```python
client = service.get_client()
```

### 创建内容
```python
# 文章
article_id = client.create_article()

# 图文
graph_text_id = client.create_graph_text(files, title, desc, thumb)

# 视频
video_id = client.create_video(files, title, desc, thumb)
```

### 发布内容
```python
# 发布文章
client.publish_article(article_id, post_accounts)

# 发布图文
client.publish_graph_text(graph_text_id, post_accounts)

# 发布视频
client.publish_video(video_id, post_accounts)
```

### 查询记录
```python
# 获取发布记录
records = client.get_publish_records(status=1)

# 获取发布详情
details = client.get_publish_record_info(record_id)
```

### 停止服务
```python
# 发布完成后停止服务
service.stop()
```

## 平台类型 (plat_type)

- `wechat`: 微信公众号
- `wechat-video`: 微信视频号
- `weibo`: 微博
- `bilibili`: B站
- `xiaohongshu`: 小红书
- `douyin`: 抖音
- `toutiaohao`: 头条号
- `kuaishou`: 快手
- `acfun`: A站
- `csdn`: CSDN
- `juejin`: 掘金

## 常用发布设置示例

### 微信公众号
```python
{
    "author": "作者",
    "origin": True,
    "publishType": "mass",
    "source": 4,
    "platType": "wechat"
}
```

### 微信视频号
```python
{
    "location": "位置",
    "collection": ["合集"],
    "source": 4,
    "platType": "wechat-video"
}
```

### B站
```python
{
    "topics": ["话题"],
    "public": True,
    "platType": "bilibili"
}
```

### 小红书
```python
{
    "location": "位置",
    "collection": "合集",
    "origin": True,
    "source": 3,
    "platType": "xiaohongshu"
}
```

## 错误处理

```python
try:
    client = quick_start_turbo_push()
    result = client.publish_graph_text(graph_text_id, post_accounts)
    
    if result.get("code") == 0:
        print("✅ 发布成功")
    else:
        print(f"❌ 发布失败: {result.get('msg')}")

except Exception as e:
    print(f"❌ 发生错误: {str(e)}")
```

## 注意事项

1. **启动服务**: 使用 `TurboPushService.start()` 启动后会自动读取配置
2. **认证**: 如果 `login: false`,需要调用 `client.login(code)` 登录
3. **文件路径**: 所有文件路径必须是绝对路径
4. **必需参数**: `platType` 是每个 settings 的必需参数
5. **停止服务**: 使用 `service.stop()` 停止服务(可选)

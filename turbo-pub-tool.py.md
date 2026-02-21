# Turbo Push API Tool

一个简化版的 Turbo Push API 调用工具,用于大模型直接接口调用内容发布任务。

## 启动 Turbo Push 服务

在使用 API 之前,需要先启动 Turbo Push 服务并获取连接信息。

### 自动启动服务

```python
import subprocess
import json
import time
import os
import signal

class TurboPushService:
    def __init__(self, binary_path="./turbo_push"):
        self.binary_path = binary_path
        self.process = None
        self.config = None

    def start(self):
        """
        启动 Turbo Push 服务
        返回: 服务配置信息(pid, auth, port, login, home, chrome, edge)
        """
        if os.path.exists(self.binary_path):
            # 设置可执行权限
            os.chmod(self.binary_path, 0o755)

        # 启动服务
        self.process = subprocess.Popen(
            [self.binary_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            universal_newlines=True
        )

        # 等待服务启动并读取标准输出
        timeout = 10  # 最多等待10秒
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # 检查进程是否还在运行
                if self.process.poll() is not None:
                    raise RuntimeError(f"Turbo Push 服务启动失败: {self.process.stderr.read()}")

                # 检查标准输出
                line = self.process.stdout.readline()
                if line:
                    line = line.strip()
                    if line.startswith("{"):
                        self.config = json.loads(line)
                        print(f"✅ Turbo Push 服务已启动")
                        print(f"   PID: {self.config['pid']}")
                        print(f"   Port: {self.config['port']}")
                        print(f"   Login: {self.config['login']}")
                        return self.config

                time.sleep(0.1)
            except json.JSONDecodeError:
                continue

        raise RuntimeError("Turbo Push 服务启动超时")

    def stop(self):
        """停止 Turbo Push 服务"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print("✅ Turbo Push 服务已停止")

    def get_config(self):
        """获取服务配置"""
        return self.config

    def get_client(self):
        """获取 TurboPushClient 实例"""
        if not self.config:
            raise RuntimeError("服务未启动,请先调用 start()")
        return TurboPushClient(
            base_url=f"http://127.0.0.1:{self.config['port']}",
            auth_token=self.config['auth']
        )
```

### 使用示例

```python
# 启动服务
service = TurboPushService(binary_path="./turbo_push")
config = service.start()

# 获取客户端
client = service.get_client()

# 使用客户端调用 API
user_info = client.login("验证码")
print(f"用户: {user_info['name']}")

# 使用完成后停止服务
service.stop()
```

### 快速获取连接信息

```python
def quick_start_turbo_push():
    """
    快速启动 Turbo Push 并返回客户端
    """
    service = TurboPushService()
    config = service.start()
    return service.get_client()

# 一行代码启动并获取客户端
client = quick_start_turbo_push()
```

---

## 基础配置

```python
import requests
import json

class TurboPushClient:
    def __init__(self, base_url="http://127.0.0.1:8910", auth_token=None):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = requests.Session()

    def _request(self, method, endpoint, data=None, params=None):
        """发送 API 请求"""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        if self.auth_token:
            headers["Authorization"] = self.auth_token

        if method == "GET":
            response = self.session.get(url, headers=headers, params=params)
        elif method == "POST":
            response = self.session.post(url, headers=headers, json=data)
        elif method == "DELETE":
            response = self.session.delete(url, headers=headers, json=data)

        try:
            return response.json()
        except:
            return response.text

    def set_auth_token(self, token):
        """设置认证令牌"""
        self.auth_token = token
```

## 用户登录

```python
# TurboPushClient 方法
def login(self, code):
    """
    登录 Turbo Push 系统
    :param code: 验证码(从 Turbo Push 客户端获取)
    """
    result = self._request("POST", "/user/login", data={"code": code})
    if result.get("code") == 0:
        data = result.get("data", {})
        self.auth_token = data.get("secure", {}).get("openID")
        return data
    return None

# 使用示例
client = TurboPushClient()
user_info = client.login("pgkerj")
print(f"用户: {user_info['name']}, openID: {user_info['secure']['openID']}")
```

## 获取平台和账号

```python
def get_platforms(self, enable=None, article=None, graph_text=None, video=None):
    """
    获取平台列表
    """
    params = {}
    if enable is not None: params["enable"] = enable
    if article is not None: params["article"] = article
    if graph_text is not None: params["graph_text"] = graph_text
    if video is not None: params["video"] = video
    return self._request("GET", "/platform/list", params=params)

def get_accounts(self):
    """获取所有账号"""
    return self._request("GET", "/account/list")

def get_logged_accounts(self):
    """获取已登录账号"""
    return self._request("GET", "/account/logged")

def find_account_by_type(self, accounts, plat_type):
    """查找指定类型的账号"""
    for acc in accounts.get("data", []):
        if acc.get("platform", {}).get("plat_type") == plat_type:
            return acc
    return None

# 使用示例
accounts = client.get_logged_accounts()
wechat_account = client.find_account_by_type(accounts, "wechat")
print(f"微信账号: {wechat_account['name']}, ID: {wechat_account['id']}")
```

## 创建内容

```python
def create_article(self):
    """
    创建文章草稿
    """
    result = self._request("POST", "/article/create")
    if result.get("code") == 0:
        return result.get("data")
    return None

def create_graph_text(self, files, title, desc, thumb):
    """
    创建图文内容
    :param files: 图片绝对路径数组
    :param title: 标题
    :param desc: 描述 (话题格式: #话题#, 提及用户格式: @用户名 )
    :param thumb: 封面图片路径数组(选一个)
    """
    data = {
        "files": files,
        "title": title,
        "desc": desc,
        "thumb": thumb
    }
    result = self._request("POST", "/graphText/create", data=data)
    if result.get("code") == 0:
        return result.get("data")
    return None

def create_video(self, files, title, desc, thumb):
    """
    创建视频内容
    :param files: 视频绝对路径数组(只支持单个视频)
    :param title: 视频标题
    :param desc: 视频描述
    :param thumb: 封面图片路径数组(选一个)
    """
    data = {
        "files": files,
        "title": title,
        "desc": desc,
        "thumb": thumb
    }
    result = self._request("POST", "/video/create", data=data)
    if result.get("code") == 0:
        return result.get("data")
    return None
```

## 发布文章

```python
def publish_article(self, article_id, post_accounts, sync_draft=False):
    """
    发布文章
    :param article_id: 文章 ID(rid)
    :param post_accounts: 发布账号列表
        [{
            "id": 账号 ID,
            "settings": 平台发布设置
        }]
    :param sync_draft: 是否同步为草稿
    """
    data = {
        "syncDraft": sync_draft,
        "postAccounts": post_accounts
    }
    return self._request("POST", f"/sse/article/{article_id}", data=data)

# 微信公众号发布设置
wechat_article_settings = {
    "author": "作者名称",
    "link": "https://example.com",
    "leave": True,           # 允许评论
    "origin": True,          # 声明原创
    "reprint": True,         # 允许快捷转载
    "publishType": "mass",   # 群发
    "source": 4,
    "collection": "科技合集",
    "platType": "wechat"
}

# B站专栏发布设置
bilibili_article_settings = {
    "column": "科技",
    "classify": "学习",
    "origin": True,
    "headerImg": "/path/to/cover.jpg",
    "labels": ["AI", "技术", "教程"],
    "collection": "教学",
    "public": True,
    "platType": "bilibili"
}

# 使用示例
article_id = client.create_article()
result = client.publish_article(
    article_id=article_id,
    post_accounts=[
        {"id": wechat_account["id"], "settings": wechat_article_settings},
        {"id": bilibili_account["id"], "settings": bilibili_article_settings}
    ]
)
```

## 发布图文

```python
def publish_graph_text(self, graph_text_id, post_accounts, sync_draft=False):
    """
    发布图文
    :param graph_text_id: 图文 ID(tid)
    :param post_accounts: 发布账号列表
    :param sync_draft: 是否同步为草稿
    """
    data = {
        "syncDraft": sync_draft,
        "postAccounts": post_accounts
    }
    return self._request("POST", f"/sse/graphText/{graph_text_id}", data=data)

# 微信视频号发布设置
wechat_video_settings = {
    "leave": True,
    "collection": ["生活记录"],
    "location": "北京",
    "linkType": 0,
    "linkAddr": "https://example.com",
    "music": "热门BGM",
    "activity": "活动",
    "source": 4,
    "platType": "wechat-video"
}

# 小红书发布设置
xiaohongshu_settings = {
    "location": "上海",
    "collection": "生活",
    "group": "日常",
    "origin": False,
    "source": 3,
    "lookScope": 0,  # 0:公开 1:朋友可见 2:仅自己可见
    "platType": "xiaohongshu"
}

# 使用示例
graph_text_id = client.create_graph_text(
    files=["/path/to/img1.jpg", "/path/to/img2.jpg"],
    title="精彩图文",
    desc="看看这个 #话题 #推荐",
    thumb=["/path/to/cover.jpg"]
)
result = client.publish_graph_text(
    graph_text_id=graph_text_id,
    post_accounts=[
        {"id": wechat_video_account["id"], "settings": wechat_video_settings},
        {"id": xiaohongshu_account["id"], "settings": xiaohongshu_settings}
    ]
)
```

## 发布视频

```python
def publish_video(self, video_id, post_accounts, sync_draft=False):
    """
    发布视频
    :param video_id: 视频 ID(vid)
    :param post_accounts: 发布账号列表
    :param sync_draft: 是否同步为草稿
    """
    data = {
        "syncDraft": sync_draft,
        "postAccounts": post_accounts
    }
    return self._request("POST", f"/sse/video/{video_id}", data=data)

# B站视频发布设置
bilibili_video_settings = {
    "topics": ["科技", "AI", "编程"],
    "genGT": {
        "enable": True,
        "syncPub": True
    },
    "collection": "科技视频",
    "stickers": [
        {
            "stickerType": 0,
            "minute": 0,
            "second": 5,
            "title": "欢迎关注",
            "content": "弹幕弹幕"
        }
    ],
    "topicId": 123,
    "platType": "bilibili"
}

# 使用示例
video_id = client.create_video(
    files=["/path/to/video.mp4"],
    title="精彩视频",
    desc="来看看这个作品 #热门 #推荐",
    thumb=["/path/to/cover.jpg"]
)
result = client.publish_video(
    video_id=video_id,
    post_accounts=[
        {"id": bilibili_account["id"], "settings": bilibili_video_settings}
    ]
)
```

## 发布记录

```python
def get_publish_records(self, status=None, type=None, size=10, page=1):
    """
    获取发布记录
    :param status: 发布状态筛选(1:发布中 2:全部失败 3:部分成功 4:全部成功)
    :param type: 内容类型筛选(1:文章 2:图文 3:视频)
    :param size: 每页条数
    :param page: 当前页
    """
    params = {"size": size, "current": page}
    if status is not None: params["status"] = status
    if type is not None: params["type"] = type
    return self._request("GET", "/record/list", params=params)

def get_publish_record_info(self, record_id):
    """
    获取发布记录详情
    :param record_id: 发布记录 ID
    """
    return self._request("GET", f"/record/info/{record_id}")
```

## 定时发布示例

```python
from datetime import datetime, timedelta

# 计算定时发布时间(2小时后)
publish_time = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

# 添加定时发布设置到 settings
timed_settings = wechat_article_settings.copy()
timed_settings["timerPublish"] = {
    "enable": True,
    "timer": publish_time
}

# 发布
result = client.publish_article(
    article_id=article_id,
    post_accounts=[{"id": wechat_account["id"], "settings": timed_settings}]
)
```

## 完整发布流程示例

```python
# 初始化客户端
client = TurboPushClient()

# 1. 登录
user_info = client.login("输入验证码")
print(f"登录成功: {user_info['name']}")

# 2. 获取已登录账号
accounts = client.get_logged_accounts()["data"]
print(f"已登录账号: {len(accounts)} 个")

# 3. 创建文章草稿
article_id = client.create_article()
print(f"文章 ID: {article_id}")

# 4. 提示用户使用 iframe 编辑器编辑内容
print(f"请在 iframe 中编辑文章: ?rid={article_id}")

# 5. 等待用户编辑完成(需要人工确认)
input("\n编辑完成后按回车键继续发布...")

# 6. 配置发布账号
post_accounts = []

for acc in accounts:
    plat_type = acc["platform"]["plat_type"]

    if plat_type == "wechat":
        post_accounts.append({
            "id": acc["id"],
            "settings": {
                "author": "我的账号",
                "origin": True,
                "publishType": "mass",
                "source": 4,
                "platType": "wechat"
            }
        })
    elif plat_type == "bilibili":
        post_accounts.append({
            "id": acc["id"],
            "settings": {
                "column": "科技",
                "origin": True,
                "public": True,
                "platType": "bilibili"
            }
        })

if post_accounts:
    print(f"准备发布到 {len(post_accounts)} 个平台...")

    # 7. 发布
    result = client.publish_article(article_id, post_accounts)
    print("发布请求已发送")

    # 8. 查询发布记录
    records = client.get_publish_records(status=1)["data"]["list"]

    if records:
        latest_record = records[0]

        # 等待发布完成
        print("等待发布完成...")
        import time
        time.sleep(30)  # 等待一段时间

        # 查看详情
        details = client.get_publish_record_info(latest_record["id"])

        for detail in details["data"]:
            acc_name = next((a["name"] for a in accounts if a["id"] == detail["account_id"]), "未知")
            if detail["success"]:
                print(f"✅ {acc_name}: {detail['link']}")
            else:
                print(f"❌ {acc_name}: {detail['reason']}")
```

## 平台类型对照

```python
PLATFORM_TYPES = {
    "wechat": "微信公众号",
    "wechat-video": "微信视频号",
    "weibo": "微博",
    "bilibili": "B站",
    "xiaohongshu": "小红书",
    "douyin": "抖音",
    "toutiaohao": "头条号",
    "zhihu": "知乎",
    "csdn": "CSDN",
    "juejin": "掘金",
    "kuaishou": "快手",
    "acfun": "Acfun"
}
```

## 错误处理

```python
def safe_publish(client, article_id, post_accounts):
    """安全发布,带错误处理"""
    try:
        result = client.publish_article(article_id, post_accounts)

        if result.get("code") == 0:
            print("✅ 发布请求成功")
            return True
        else:
            print(f"❌ 发布失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"❌ 发布异常: {str(e)}")
        return False
```

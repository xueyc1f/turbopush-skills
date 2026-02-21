---
name: turbo-pub
version: 1.0.0
description: |
  Turbo Push API 客户端 - 多平台内容发布工具

  该 skill 使大模型能够通过 Turbo Push API 执行以下任务:
  - 用户认证与会话管理
  - 多平台账号管理(登录、状态查看、删除)
  - 内容创建(文章、图文、视频)
  - 多平台发布(微信公众号、B站、小红书、抖音、头条号等)
  - 发布记录查询
  - 平台设置管理

  核心特性:
  - 支持一键发布到多个平台
  - 每个平台可自定义发布参数(settiings)
  - 支持定时发布(timerPublish)
  - SSE 实时监听发布状态

author: Turbo Push Team
tags:
  - content-publishing
  - multi-platform
  - social-media
  - automation
  - wechat
  - bilibili
  - douyin
  - xiaohongshu

# 配置要求
requires:
  - API_BASE_URL: Turbo Push 服务地址(默认: http://127.0.0.1:8910)
  - AUTH_TOKEN: 认证令牌(通过 /user/login 获取)

# 可用工具定义
tools:
  ---
  ## 用户认证

  ### loginWithCode
  使用验证码登录 Turbo Push 系统。

  **注意**: 验证码需要用户手工从 Turbo Push 客户端获取。

  **参数**:
  - code (string, required): 从 Turbo Push 客户端获取的验证码

  **返回**:
  - 用户信息(包含 open_id、授权状态、会员信息等)
  - 认证令牌(用于后续 API 调用)

  **示例**:
  ```python
  result = turbo_login(code="pgkerj")
  auth_token = result["openID"]  # 保存用于后续请求
  ```

  ### getUserInfo
  获取当前登录用户的详细信息。

  **返回**:
  - 用户 ID、名称、头像
  - open_id
  - 登录状态
  - 会员信息(过期时间、邀请码等)

  ----
  ## 平台与账号管理

  ### getPlatforms
  获取支持的平台列表。

  **返回**: 支持的平台列表,每个平台包含:
  - id: 平台 ID
  - name: 平台名称
  - plat_type: 平台类型标识(wechat、bilibili、douyin 等)
  - article: 是否支持文章
  - graph_text: 是否支持图文
  - video: 是否支持视频
  - status: 状态(1:开发中 2:已支持)

  **平台类型对照表**:
  - wechat: 微信公众号(文章)
  - wechat-video: 视频号(图文/视频)
  - weibo: 微博
  - bilibili: B站(专栏/视频)
  - xiaohongshu: 小红书
  - douyin: 抖音
  - toutiaohao: 头条号
  - zhihu: 知乎(文章)
  - csdn: CSDN(文章)
  - juejin: 掘金(文章)

  ### getAccounts
  获取所有账号列表。

  **返回**: 账号列表,包含:
  - id: 账号 ID(aid)
  - name: 账号名称
  - platform: 平台信息
  - avatar: 头像
  - login: 登录状态
  - login_time: 登录时间

  ### getLoggedAccounts
  获取已登录账号列表(更快,用于发布时选择账号)。

  **返回**: 同 getAccounts,但只返回已登录账号。

  ### loginAccount
  登录指定平台的账号。

  **参数**:
  - platform_id (integer, required): 平台 ID(pid)
  - platform_type (string, optional): 平台类型,用于提示用户

  **流程**:
  1. 调用此接口打开浏览器进行登录
  2. 用户在浏览器完成登录授权
  3. 系统自动保存登录信息

  **返回**: 登录成功后的账号信息

  ⚠️ **注意**: 此接口会打开浏览器窗口,需要用户手动完成登录流程。

  ### deleteAccount
  删除指定账号。

  **参数**:
  - account_id (integer, required): 账号 ID(aid)

  ----
  ## 内容创建

  ### createArticle
  创建文章草稿。编辑完成后可通过 iframe 编辑器修改内容。

  **返回**: 文章 ID(rid)

  ### createGraphText
  创建图文内容。

  **参数**:
  - files (string[], required): 图片绝对路径数组
  - title (string, required): 标题
  - desc (string, required): 描述
  - thumb (string[], required): 封面图片路径(选一个)

  **说明**:
  - 话题格式: (#话题#)
  - 提及用户格式: (@用户名 )
  - 图片需要使用绝对路径

  **返回**: 图文 ID(tid)

  ### createVideo
  创建视频内容。

  **参数**:
  - files (string[], required): 视频绝对路径数组(只支持单个视频)
  - title (string, required): 视频标题
  - desc (string, required): 视频描述
  - thumb (string[], required): 封面图片路径(选一个)

  **返回**: 视频 ID(vid)

  ----
  ## 内容发布

  ### publishArticle
  发布文章到指定平台的账号。

  **参数**:
  - article_id (string, required): 文章 ID(rid)
  - sync_draft (boolean, optional): 是否同步为草稿,默认 false
  - accounts (array, required): 发布账号数组,每个元素包含:
    - id (integer, required): 账号 ID
    - settings (object, required): 平台发布设置

  **平台发布设置说明**:

  **微信公众号 (platType: "wechat")**:
  ```python
  {
    "author": "作者名称",           # 可选
    "link": "原文链接",              # 可选
    "leave": true,                  # 允许评论
    "origin": true,                 # 声明原创
    "reprint": true,                # 允许快捷转载
    "publishType": "mass",          # "mass"(群发) | "publish"(单独发布)
    "source": 4,                    # 来源 0-4
    "collection": "合集名称",        # 可选
    "timerPublish": {               # 可选,定时发布
      "enable": true,
      "timer": "2025-06-15 18:30:00"
    }
  }
  ```

  **B站专栏 (platType: "bilibili")**:
  ```python
  {
    "column": "专栏分类",            # 可选
    "classify": "文章分类",          # 可选
    "origin": true,                 # 声明原创
    "headerImg": "/path/to/image", # 封面图
    "labels": ["标签1", "标签2"],    # 标签列表
    "collection": "合集名称",        # 可选
    "public": true                  # 公开状态
  }
  ```

  **返回**: 空(异步发布)

  ### publishGraphText
  发布图文内容。

  **参数**:
  - graph_text_id (string, required): 图文 ID(tid)
  - sync_draft (boolean, optional): 是否同步为草稿
  - accounts (array, required): 同 publishArticle

  **微信视频号 (platType: "wechat-video")**:
  ```python
  {
    "leave": true,
    "collection": ["合集名称"],
    "location": "位置",              # 可选
    "linkType": 0,                   # 0:无链接 1:公众号链接 2:网页链接
    "linkAddr": "https://...",       # 链接地址
    "music": "BGM名称",              # 可选
    "activity": "活动",              # 可选
    "source": 4,
    "timerPublish": {                # 可选
      "enable": true,
      "timer": "2025-05-25 17:30"
    }
  }
  ```

  **小红书 (platType: "xiaohongshu")**:
  ```python
  {
    "location": "位置",              # 可选
    "collection": "合集",            # 可选
    "group": "分组",                 # 可选
    "origin": false,
    "source": 3,
    "lookScope": 0                   # 0:公开 1:朋友可见 2:仅自己可见
  }
  ```

  **抖音/头条号 (platType: "douyin"|"toutiaohao")**:
  ```python
  {
    "location": "天津",
    "openBgm": true,                 # 开启BGM
    "source": 3
  }
  ```

  ### publishVideo
  发布视频内容。

  **参数**:
  - video_id (string, required): 视频 ID(vid)
  - sync_draft (boolean, optional): 是否同步为草稿
  - accounts (array, required): 发布账号数组

  **微信视频号视频 (platType: "wechat-video")**:
  ```python
  {
    "location": "位置",
    "linkType": 0,
    "linkAddr": "https://...",
    "activity": "活动",
    "collection": "合集",
    "timerPublish": {
      "enable": true,
      "timer": "2025-05-25 17:30"
    }
  }
  ```

  **B站视频 (platType: "bilibili")**:
  ```python
  {
    "topics": ["话题1", "话题2"],     # 分区话题
    "genGT": {                       # 生成封面/标签
      "enable": true,
      "syncPub": true
    },
    "collection": "合集名称",
    "stickers": [                    # 视频贴纸(弹幕)
      {
        "stickerType": 0,            # 0:文字贴纸
        "minute": 0,
        "second": 5,
        "title": "发弹幕啦",
        "content": "弹幕弹幕"
      }
    ],
    "topicId": 123,                  # 分区 ID
    "title": "视频标题",             # 可选,覆盖原标题
    "desc": "视频描述",              # 可选,覆盖原描述
    "tag": "标签1,标签2",            # 可选,视频标签
  # 更多参数...
  }
  ```

  **抖音/头条号视频 (platType: "douyin"|"toutiaohao")**:
  ```python
  {
    "topics": ["话题1", "话题2"],
    "location": "天津",
    "openBgm": true,
    "source": 3,
    "musicType": 0                   # 音乐类型
  }
  ```

  ----
  ## 发布记录管理

  ### getPublishRecords
  获取发布记录列表。

  **参数**:
  - status (integer, optional): 发布状态筛选
    - 1: 发布中
    - 2: 全部失败
    - 3: 部分成功
    - 4: 全部成功
  - type (integer, optional): 内容类型筛选
    - 1: 文章
    - 2: 图文
    - 3: 视频
  - size (integer, optional): 每页条数,默认 10
  - page (integer, optional): 当前页,默认 1

  **返回**: 发布记录列表,包含:
  - id: 记录 ID
  - content_id: 内容 ID
  - publish_type: 类型
  - status: 状态
  - since: 耗时

  ### getPublishRecordInfo
  获取发布记录详情,包含每个账号的发布结果。

  **参数**:
  - record_id (integer, required): 发布记录 ID

  **返回**: 发布详情数组,每个元素包含:
  - id: 详情 ID
  - account_id: 账号 ID
  - success: 是否成功
  - since: 耗时
  - link: 发布成功后的内容链接
  - read_num: 阅读数
  - comment_num: 评论数
  - like_num: 点赞数
  - reason: 失败原因(如果失败)

  ### deletePublishRecord
  删除发布记录。

  **参数**:
  - record_id (integer, required): 发布记录 ID

  ----
  ## SSE 监听

  ### listenSSE
  建立 SSE 连接,监听账号登录状态和发布进度。

  **事件类型**:
  - logout: 账号退出登录,需更新登录状态并提示用户
  - exit: 用户退出登录,需返回登录页面并断开连接
  - heartbeat: 心跳,无需处理

  **返回**: SSE 事件流

  ⚠️ **注意**: 此接口会阻塞,需要在后台持续监听。

  ----
  ## 平台设置管理

  ### getPlatformSettings
  获取指定平台的所有设置配置。

  **参数**:
  - platform_id (integer, required): 平台 ID

  **返回**: 设置列表,按默认配置优先、启用优先、更新时间倒序排列

  ### createPlatformSetting
  创建平台发布配置。

  **参数**:
  - name (string, required): 配置名称(同一平台下不能重复)
  - platform_id (integer, required): 平台 ID
  - setting (object, required): 平台特定配置内容
  - description (string, optional): 配置描述

  **说明**:
  - 如果是该平台的第一个配置,会自动设为默认
  - setting 字段根据平台类型不同而不同,参考发布接口中的 settings 参数

  ### deletePlatformSetting
  删除平台配置。

  **参数**:
  - setting_id (integer, required): 设置 ID

  **说明**: 默认配置不能删除

  ----
  ## 完整发布流程示例

  ### 示例1: 发布文章到微信公众号和B站

  ```python
  # 1. 登录
  auth_info = turbo_login(code="验证码")
  auth_token = auth_info["openID"]

  # 2. 获取已登录账号
  accounts = getLoggedAccounts()

  # 3. 选择账号(过滤微信和B站)
  target_accounts = [
    acc for acc in accounts
    if acc["platform"]["plat_type"] in ["wechat", "bilibili"]
  ]

  # 4. 创建文章草稿
  article_id = createArticle()

  # 5. 使用 iframe 编辑器编辑文章内容(需要人工介入)
  # ...

  # 6. 发布到指定账号
  result = publishArticle(
    article_id=article_id,
    sync_draft=False,
    accounts=[
      {
        "id": next(a["id"] for a in target_accounts if a["platform"]["plat_type"] == "wechat"),
        "settings": {
          "author": "我的账号",
          "origin": True,
          "publishType": "mass",
          "source": 4,
          "platType": "wechat"
        }
      },
      {
        "id": next(a["id"] for a in target_accounts if a["platform"]["plat_type"] == "bilibili"),
        "settings": {
          "column": "科技",
          "origin": True,
          "labels": ["AI", "技术"],
          "public": True,
          "platType": "bilibili"
        }
      }
    ]
  )

  # 7. 获取发布记录
  records = getPublishRecords(status=1, type=1)

  # 8. 查看发布详情
  for record in records["data"]["list"]:
    details = getPublishRecordInfo(record["id"])
    for detail in details["data"]:
      if detail["success"]:
        print(f"发布成功: {detail['link']}")
      else:
        print(f"发布失败: {detail['reason']}")
  ```

  ### 示例2: 发布图文到多个平台

  ```python
  # 1. 获取已登录账号
  accounts = getLoggedAccounts()

  # 2. 选择支持图文的账号
  target_accounts = [
    acc for acc in accounts
    if acc["platform"]["video"] and acc["platform"]["graph_text"]
  ]

  # 3. 创建图文
  graph_text_id = createGraphText(
    files=["/path/to/img1.jpg", "/path/to/img2.jpg"],
    title="我的图文标题",
    desc="这是精彩的内容 #热门话题 #推荐",
    thumb=["/path/to/cover.jpg"]
  )

  # 4. 发布到各平台
  post_accounts = []
  for acc in target_accounts:
    plat_type = acc["platform"]["plat_type"]

    if plat_type == "wechat-video":
      settings = {
        "location": "北京",
        "collection": ["我的合集"],
        "source": 4,
        "platType": "wechat-video"
      }
    elif plat_type == "xiaohongshu":
      settings = {
        "location": "上海",
        "collection": "生活",
        "origin": True,
        "source": 3,
        "lookScope": 0,
        "platType": "xiaohongshu"
      }
    elif plat_type == "douyin":
      settings = {
        "location": "广州",
        "openBgm": True,
        "source": 3,
        "platType": "douyin"
      }
    else:
      continue

    post_accounts.append({
      "id": acc["id"],
      "settings": settings
    })

  # 5. 统一发布
  publishGraphText(
    graph_text_id=graph_text_id,
    sync_draft=False,
    accounts=post_accounts
  )
  ```

  ### 示例3: 定时发布视频

  ```python
  # 1. 创建视频
  video_id = createVideo(
    files=["/path/to/video.mp4"],
    title="精彩视频作品",
    desc="看看这个视频 #热门 #推荐",
    thumb=["/path/to/cover.jpg"]
  )

  # 2. 配置定时发布
  from datetime import datetime, timedelta
  publish_time = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

  # 3. 发布到B站(定时)
  publishVideo(
    video_id=video_id,
    sync_draft=False,
    accounts=[{
      "id": account_id,
      "settings": {
        "topics": ["科技", "AI"],
        "genGT": {"enable": True, "syncPub": True},
        "collection": "科技视频",
        "platType": "bilibili",
        "timerPublish": {
          "enable": True,
          "timer": publish_time
        }
      }
    }]
  )
  ```

  ----
  ## 错误处理

  ### 常见错误码
  - 0: 成功
  - 401: 未授权(Authorization 缺失或无效)
  - 425: 非会员功能(VIP 权限不足)
  - 其他: 具体错误信息见 msg 字段

  ### 错误处理建议
  1. 检查 Authorization header 是否正确
  2. 检查账号是否已登录(login 状态)
  3. 检查平台类型是否正确
  4. 检查文件路径是否存在
  5. 检查发布参数是否符合平台要求

  ----
  ## 最佳实践

  1. **发布前验证**:
     - 优先使用 getLoggedAccounts() 只获取已登录账号
     - 发布前检查账号的 login 状态
     - 确认文件路径存在且可访问

  2. **批量发布**:
     - 使用 accounts 数组一次发布到多个平台
     - 不同平台使用不同的 settings 配置
     - 建议先测试单个平台成功后再批量发布

  3. **定时发布**:
     - timer 格式: "YYYY-MM-DD HH:MM:SS"
     - 可为不同账号设置不同的发布时间
     - 设置 timer 前确保 enable 为 true

  4. **内容管理**:
     - 发布记录可在 /record/list 查看
     - 发布失败原因可在 /record/info/{id} 查看
     - 支持重新失败的任务

  5. **设置管理**:
     - 使用 createPlatformSetting 为常用配置创建模板
     - 每个平台可以有多个配置
     - 可以设置默认配置简化发布流程

  ----
  ## 限制说明

  - VIP 功能需要会员权限(代理、导入导出等)
  - 部分平台可能有发布频率限制
  - 视频文件大小不能超过平台限制
  - 某些平台参数是必需的,见各平台设置说明
  - SSE 连接需要保持活跃,断开后需重新连接

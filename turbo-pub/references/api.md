# Turbo Push API 参数完整参考

> 数据来源：https://my.feishu.cn/wiki/RZgow71Lei6Ki0k6mUKcyo83nbb

## 发布账号参数结构

所有发布接口的 `post_accounts` 格式：
```python
[
    {
        "id": 账号ID,           # 必需，来自 get_logged_accounts()
        "settings": {           # 必需，平台特定参数
            "platType": "...",  # 必需，见各平台说明
            ...
        }
    }
]
```

---

## 各平台发布参数

### Acfun（platType: "acfun"）

用于 `publish_article()`（视频）。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `acfun` |
| classify | string | 分区，如 `动画/综合` |
| labels | string | 标签，多个用 `/` 分隔 |
| origin | bool | 原创: `true` / 转载: `false` |
| reprint | string | 转载来源，原创时留空 |
| dynamic | string | 粉丝动态 |
| timerPublish | object | 定时发布 `{enable: bool, timer: string}` |

```json
{
    "platType": "acfun",
    "classify": "动画/综合",
    "labels": "标签1/标签2",
    "origin": true,
    "reprint": "",
    "dynamic": "这是我的新视频",
    "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}
}
```

---

### 百家号（platType: "baijiahao"）

用于 `publish_article()` / `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `baijiahao` |
| watermark | uint8 | 水印（仅视频）: `0`不添加 `1`添加水印 `2`添加贴片 |
| location | string | 位置 |
| classify | string | 分类 |
| activity | string | 活动 |
| byAI | bool | AI创作声明 |
| timerPublish | object | 定时发布 |

```json
{"platType": "baijiahao", "watermark": 1, "location": "北京", "classify": "科技/互联网", "activity": "百度创作活动", "byAI": true, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### Bilibili 视频（platType: "bilibili"）

用于 `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `bilibili` |
| reprint | string | 转载来源，为空表示自制 |
| partition | string | 分区，如 `生活/日常` |
| creation | bool | 是否允许二创 |
| public | bool | 是否公开可见 |
| source | uint | 创作声明 |
| dynamic | string | 粉丝动态 |
| timerPublish | object | 定时发布 |

```json
{"platType": "bilibili", "reprint": "https://www.youtube.com/watch?v=...", "partition": "生活/日常", "creation": true, "public": true, "source": 1, "dynamic": "这是我的新视频", "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

### Bilibili 专栏（platType: "bilibili"）

用于 `publish_article()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `bilibili` |
| classify | string | 专栏分类，如 `游戏/单机游戏` |
| origin | bool | 声明原创，默认 `false` |
| headerImg | string | 头图绝对路径 |
| labels | string | 标签，最多10个，多个用 `/` 分隔 |
| collection | string | 合集 |
| public | bool | 是否公开可见 |
| timerPublish | object | 定时发布 |

```json
{"platType": "bilibili", "classify": "游戏/单机游戏", "origin": true, "headerImg": "/path/to/image.jpg", "labels": "游戏/单机", "collection": "我的合集", "public": true, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 抖音（platType: "douyin"）

用于 `publish_graph_text()` / `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `douyin` |
| activity | string | 添加活动奖励 |
| music | string | 音乐（仅图文生效） |
| label | string | 标签类型：`位置`/`团购`/`影视演绎`/`小程序` |
| location | string | 标签值。位置：留空将默认选第一个选项；团购：按 `[带货模式\|打卡模式]/范围/商品名/推广标题` 格式 |
| challenge | string | 挑战贴纸 |
| hotspot | string | 关联热点 |
| collection | string | 合集 |
| allowSave | bool | 允许他人保存 |
| lookScope | uint | 谁可以看：`0`公开 `1`好友 `2`自己 |
| timerPublish | object | 定时发布 |

```json
{"platType": "douyin", "activity": "抖音活动", "music": "热门音乐", "label": "位置", "location": "具体位置", "challenge": "热门挑战", "hotspot": "热点话题", "collection": "我的合集", "allowSave": true, "lookScope": 0, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

团购示例：
```json
{"platType": "douyin", "label": "团购", "location": "带货模式/全国/企业AI运营岗创客班/AI运营岗创客课程", "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 简书（platType: "jianshu"）

用于 `publish_article()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `jianshu` |
| collection | string | 文集 |
| vetoReprint | bool | 禁止转载 |

```json
{"platType": "jianshu", "collection": "我的文集", "vetoReprint": true}
```

---

### 掘金（platType: "juejin"）

用于 `publish_article()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `juejin` |
| classify | string | 分类，如 `后端` |
| tag | string | 标签，如 `Go` |
| collection | string | 专栏 |
| topic | string | 话题 |
| group | string | 沸点圈子 |
| link | string | 沸点链接 |

```json
{"platType": "juejin", "classify": "后端", "tag": "Go", "collection": "Go语言学习", "topic": "Go", "group": "Go", "link": "https://juejin.cn"}
```

---

### 快手（platType: "kuaishou"）

用于 `publish_graph_text()` / `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `kuaishou` |
| music | string | 添加音乐（仅图文） |
| linkApplet | string | 小程序链接 |
| source | uint | 作品声明：`0`不声明 `1`内容为AI生成 `2`演绎情节仅供娱乐 `3`个人观点仅供参考 `4`素材来源于网络 |
| collection | string | 合集 |
| location | string | 位置 |
| sameFrame | bool | 同框 |
| download | bool | 允许下载 |
| sameCity | bool | 同城推荐 |
| lookScope | uint | 谁可以看：`0`公开 `1`好友 `2`自己 |
| timerPublish | object | 定时发布 |

```json
{"platType": "kuaishou", "music": "热门音乐", "linkApplet": "小程序链接", "source": 1, "collection": "我的合集", "location": "北京", "sameFrame": true, "download": true, "sameCity": true, "lookScope": 0, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 腾讯内容开放平台（platType: "omtencent"）

用于 `publish_article()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `omtencent` |
| classify | string | 分类 |
| labels | string | 标签，多个用 `/` 分隔 |
| activity | string | 活动 |
| source | uint | 声明 |
| timerPublish | object | 定时发布 |

```json
{"platType": "omtencent", "classify": "科技", "labels": "互联网/Go", "activity": "腾讯创作活动", "source": 1, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 新浪微博 文章（platType: "sina"）

用于 `publish_article()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `sina` |
| collection | string | 专栏 |
| onlyFans | bool | 仅粉丝阅读全文，默认 `true` |
| lookScope | uint | 谁可以看：`0`公开 `1`粉丝 |
| source | uint | 内容声明：`0`不声明 `1`内容由AI生成 `2`内容为虚构演绎 |
| dynamic | string | 粉丝动态 |
| timerPublish | object | 定时发布 |

```json
{"platType": "sina", "collection": "我的专栏", "onlyFans": true, "lookScope": 0, "source": 1, "dynamic": "这是我的新文章", "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

### 新浪微博 视频/图文（platType: "sina"）

用于 `publish_video()` / `publish_graph_text()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `sina` |
| collection | string | 专栏 |
| onlyFans | bool | 仅粉丝阅读全文 |
| lookScope | uint | 谁可以看：`0`公开 `1`粉丝 `2`好友圈 `3`自己（仅视频） |
| source | uint | 内容声明：`0`不声明 `1`内容由AI生成 `2`内容为虚构演绎 |
| dynamic | string | 粉丝动态 |
| type | uint | 类型：`0`原创 `1`二创 `2`转载 |
| classify | string | 分类，如 `科技/互联网` |
| stress | bool | 允许画重点 |
| location | string | 位置 |
| wait | int | 等待X秒 |
| timerPublish | object | 定时发布 |

```json
{"platType": "sina", "collection": "我的专栏", "onlyFans": true, "lookScope": 0, "source": 1, "dynamic": "这是我的新视频", "type": 0, "classify": "科技/互联网", "stress": true, "location": "北京", "wait": 0, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### TikTok（platType: "tiktok"）

用于 `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `tiktok` |
| location | string | 位置 |
| lookScope | uint | 谁可以看：`0`所有人 `1`好友 `2`自己 |
| comment | bool | 允许评论 |
| creation | bool | 二次创作内容 |
| reveal | bool | 披露作品内容 |
| yourBrand | bool | 你的品牌 |
| brandContent | bool | 品牌内容 |
| aigc | bool | AI生成的内容 |
| timerPublish | object | 定时发布 |

```json
{"platType": "tiktok", "location": "北京", "lookScope": 0, "comment": true, "creation": false, "reveal": true, "yourBrand": true, "brandContent": false, "aigc": true, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 今日头条 文章（platType: "toutiao"）

用于 `publish_article()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `toutiao` |
| location | string | 位置 |
| placeAD | bool | 投放广告 |
| starter | bool | 首发 |
| collection | string | 合集（设置合集后**不能**定时发布） |
| syncPublish | bool | 同时发布微头条 |
| source | uint | `0`不声明 `1`取材网络 `2`引用站内 `3`个人观点仅供参考 `4`引用AI `5`虚构演绎故事经历 |
| timerPublish | object | 定时发布 |

```json
{"platType": "toutiao", "location": "北京", "placeAD": true, "starter": true, "collection": "我的合集", "syncPublish": true, "source": 1, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

### 今日头条 图文（platType: "toutiao"）

用于 `publish_graph_text()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| openBgm | bool | 开启配乐 |
| location | string | 位置 |
| placeAD | bool | 投放广告 |
| starter | bool | 首发 |
| collection | string | 合集（设置合集后**不能**定时发布） |
| syncPublish | bool | 同时发布微头条 |
| source | uint | 同上 |
| timerPublish | object | 定时发布 |

```json
{"platType": "toutiao", "openBgm": true, "location": "北京", "placeAD": true, "starter": true, "collection": "我的合集", "syncPublish": true, "source": 1, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

### 今日头条 视频（platType: "toutiao"）

用于 `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| gtEnable | bool | 视频生成图文 |
| gtSyncPub | bool | 生成图文与视频同时发布 |
| collection | string | 合集 |
| stickers | array | 互动贴纸 |
| source | uint | `0`不声明 `1`取自站外 `2`引用站内 `3`自行拍摄 `4`AI生成 `5`虚构演绎故事经历 `6`投资观点仅供参考 `7`健康医疗分享仅供参考 |
| link | string | 扩展链接 |
| lookScope | uint | 谁可以看：`0`公开 `1`粉丝 `2`自己 |
| timerPublish | object | 定时发布 |

```json
{"platType": "toutiao", "gtEnable": true, "gtSyncPub": true, "collection": "我的合集", "stickers": [], "source": 1, "link": "https://example.com", "lookScope": 0, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 微信公众号 文章/图文（platType: "wechat"）

用于 `publish_article()` / `publish_graph_text()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `wechat` |
| author | string | 作者 |
| link | string | 原文链接 |
| leave | bool | 开启留言，默认 `true` |
| origin | bool | 声明原创，默认 `false` |
| reprint | bool | 快捷转载（origin为true时可设置） |
| publishType | string | 发表类型：`mass`群发 / `publish`发布 |
| collection | string | 合集（文章/图文/视频合集不能重复） |
| source | uint | `0`不声明 `1`内容由AI生成 `2`素材来源官方媒体/网络新闻 `3`内容剧情演绎仅供娱乐 `4`个人观点仅供参考 |
| timerPublish | object | 定时发布 |

```json
{"platType": "wechat", "author": "作者", "link": "https://example.com", "leave": true, "origin": true, "reprint": true, "publishType": "mass", "collection": "我的合集", "source": 1, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

### 微信公众号 视频（platType: "wechat"）

用于 `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| materTitle | string | 素材标题 |
| barrage | bool | 弹幕 |
| barrageCheck | uint | `0`所有用户 `1`已关注用户 `2`已关注7天及以上用户 |
| turn2Channel | bool | 发表后转为视频号视频 |
| adTrans | uint | 广告过渡：`0`不设置 `1`接下来是广告时间 `2`-`6`其他广告过渡语 |
| author | string | 作者 |
| link | string | 原文链接 |
| leave | bool | 开启留言 |
| origin | bool | 声明原创 |
| reprint | bool | 快捷转载 |
| publishType | string | `mass`群发 / `publish`发布 |
| collection | string | 合集 |
| source | uint | 同上 |
| timerPublish | object | 定时发布 |

```json
{"platType": "wechat", "materTitle": "视频标题", "barrage": true, "barrageCheck": 1, "turn2Channel": true, "adTrans": 1, "author": "作者", "link": "https://example.com", "leave": true, "origin": true, "reprint": true, "publishType": "mass", "collection": "我的合集", "source": 1, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 微信视频号（platType: "wechat_video"）

⚠️ platType 值为 `wechat_video`（下划线）。

用于 `publish_graph_text()` / `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `wechat_video` |
| location | string | 位置 |
| collection | string | 合集 |
| linkType | uint | 链接类型：`0`不设置 `1`公众号文章 `2`红包封面 |
| linkAddr | string | 链接地址 |
| music | string | 音乐 |
| activity | string | 活动 |
| origin | bool | 原创（仅视频） |
| timerPublish | object | 定时发布 |

```json
{"platType": "wechat_video", "location": "北京", "collection": "我的合集", "linkType": 1, "linkAddr": "https://example.com", "music": "热门音乐", "activity": "微信活动", "origin": true, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 微视（platType: "weishi"）

用于 `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `weishi` |
| source | uint | `0`不声明 `1`该内容由AI生成 `2`剧情演绎仅供娱乐 `3`个人观点仅供参考 `4`取材网络谨慎甄别 |
| lookScope | uint | 谁可以看：`0`公开 `1`自己 |
| timerPublish | object | 定时发布 |

```json
{"platType": "weishi", "source": 1, "lookScope": 0, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 小红书（platType: "xiaohongshu"）

用于 `publish_graph_text()` / `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `xiaohongshu` |
| location | string | 位置 |
| collection | string | 合集 |
| group | string | 群聊 |
| mark | object | 标记：`{user: bool, search: string}`（`user: true`标记用户，`false`标记地点） |
| origin | bool | 声明原创，默认 `false` |
| source | uint | 作品声明：`0`不声明 `1`虚构演绎仅供娱乐 `2`笔记含AI合成内容 `3`已在正文中自主标注 `4`自主拍摄 `5`来源转载 |
| reprint | string | 来源转载的来源媒体 |
| lookScope | uint | 谁可以看：`0`公开 `1`好友 `2`自己 |
| timerPublish | object | 定时发布（格式：`2025-04-25 15:54`） |

```json
{"platType": "xiaohongshu", "location": "北京", "collection": "我的合集", "group": "我的群聊", "mark": {"user": true, "search": "用户名"}, "origin": true, "source": 1, "reprint": "来源", "lookScope": 0, "timerPublish": {"enable": true, "timer": "2025-09-21 15:30:00"}}
```

---

### 知乎 文章/图文（platType: "zhihu"）

用于 `publish_article()` / `publish_graph_text()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `zhihu` |
| question | string | 投稿至问题 |
| source | uint | 创作声明：`0`无声明 `1`包含剧透 ... `5`包含AI辅助创作 |
| topic | string | 文章话题，最多3个，多个用 `/` 分割 |
| collection | string | 专栏（为空表示不发布到专栏） |
| origin | uint | 内容来源：`0`不设置 `1`官方网站 `2`新闻报道 `3`电视媒体 `4`纸质媒体 |

```json
{"platType": "zhihu", "question": "如何评价Go语言？", "source": 5, "topic": "Go/后端/编程", "collection": "我的专栏", "origin": 1}
```

### 知乎 视频（platType: "zhihu"）

用于 `publish_video()`。

| 字段 | 类型 | 说明 |
|------|------|------|
| platType | string | 固定为: `zhihu` |
| classify | string | 领域分类 |
| reprint | bool | `true`转载 `false`原创 |
| question | string | 投稿至问题 |
| source | uint | 创作声明：`0`无声明 ... `5`包含AI辅助创作 |
| topic | string | 文章话题，最多3个，多个用 `/` 分割 |

---

## 定时发布

在任意平台 `settings` 中添加 `timerPublish`：

```python
from datetime import datetime, timedelta

publish_time = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

settings = {
    "platType": "wechat",
    # ... 其他参数
    "timerPublish": {
        "enable": True,
        "timer": publish_time   # 格式: "YYYY-MM-DD HH:MM:SS"
    }
}
```

⚠️ 今日头条（toutiao）设置了 `collection` 后不能同时使用定时发布。

---

## API 端点速查

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /user/login | 登录（body: `{"code": "验证码"}`） |
| GET | /account/logged | 获取已登录账号 |
| GET | /account/list | 获取所有账号 |
| GET | /platform/list | 获取平台列表 |
| POST | /article/create | 创建文章草稿 |
| POST | /graphText/create | 创建图文 |
| POST | /video/create | 创建视频 |
| POST | /sse/article/{rid} | 发布文章 |
| POST | /sse/graphText/{tid} | 发布图文 |
| POST | /sse/video/{vid} | 发布视频 |
| GET | /record/list | 查询发布记录 |
| GET | /record/info/{id} | 查询发布详情 |
| DELETE | /record/del | 删除发布记录 |

### 发布记录状态码
- `1`: 发布中
- `2`: 全部失败
- `3`: 部分成功
- `4`: 全部成功

### 响应错误码
- `0`: 成功
- `401`: 未授权（Authorization 缺失或无效）
- `425`: 非会员功能（需要 VIP）

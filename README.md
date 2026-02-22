# turbo-pub skill

让 AI 助手通过 [Turbo Push](https://turbopush.top) 将内容一键发布到微信公众号、微信视频号、B站、小红书、抖音、头条号、快手等多个平台。

## 安装

### 方式一：直接复制目录

将 `turbo-pub/` 目录复制到你的 AI 助手的 skills 目录：

```bash
# OpenCode / OhMyOpenCode
cp -r turbo-pub/ ~/.agents/skills/

# 或其他支持 skills 的 AI 工具，复制到对应目录
```

### 方式二：打包安装（推荐）

使用 `create-skill` 提供的打包脚本：

```bash
# 打包为 .skill 文件
python scripts/package_skill.py turbo-pub/

# 生成 turbo-pub.skill，将其导入到支持的 AI 助手中
```

## 使用前提

1. **安装 Turbo Push 客户端**：前往 [Turbo Push 官网](https://turbopush.top) 下载并安装
2. **登录账号**：在 Turbo Push 客户端中登录你要发布的各平台账号
3. **获取验证码**：首次使用时需要从 Turbo Push 客户端获取验证码

## 快速使用

安装 skill 后，直接告诉 AI 你想做什么：

> "帮我把这篇文章发布到微信公众号和B站"

> "把这个视频发布到抖音和小红书，小红书设置位置为北京"

> "查看最近的发布记录"

AI 会自动：
1. 启动本地 Turbo Push 服务（`assets/` 中的二进制文件）
2. 获取已登录账号
3. 创建内容并发布到指定平台
4. 返回发布结果

## 支持的平台

| 平台 | platType | 文章 | 图文 | 视频 |
|------|----------|:----:|:----:|:----:|
| 微信公众号 | wechat | ✅ | ✅ | ✅ |
| 微信视频号 | wechat_video | - | ✅ | ✅ |
| B站 | bilibili | ✅ | - | ✅ |
| 小红书 | xiaohongshu | - | ✅ | ✅ |
| 抖音 | douyin | - | ✅ | ✅ |
| 今日头条 | toutiao | ✅ | ✅ | ✅ |
| 快手 | kuaishou | - | ✅ | ✅ |
| 知乎 | zhihu | ✅ | ✅ | ✅ |
| 新浪微博 | sina | ✅ | ✅ | ✅ |
| TikTok | tiktok | - | - | ✅ |
| 掘金 | juejin | ✅ | - | - |
| 简书 | jianshu | ✅ | - | - |
| A站 | acfun | ✅ | - | - |
| 百家号 | baijiahao | ✅ | - | ✅ |
| 腾讯内容 | omtencent | ✅ | - | - |
| 微视 | weishi | - | - | ✅ |

## 文件说明

```
turbo-pub/
├── SKILL.md                    # Skill 主文件（AI 加载的入口）
├── scripts/
│   └── turbo_push_client.py    # Python 客户端（AI 直接运行）
├── references/
│   └── api.md                  # 完整平台参数文档（按需加载）
└── assets/
    ├── turbo_push_apple_silicon # macOS ARM64 (M系列芯片)
    ├── turbo_push_mac_intel     # macOS Intel
    ├── turbo_push_linux         # Linux
    └── turbo_push.exe           # Windows
```

## 常见问题

**Q: 提示找不到二进制文件？**  
A: 确保 `assets/` 目录中有对应平台的可执行文件，并告知 AI `assets/` 的绝对路径。

**Q: 登录状态失效？**  
A: 重新启动服务后，在 Turbo Push 客户端获取新验证码重新登录。

**Q: 发布失败怎么排查？**  
A: 让 AI 调用 `get_publish_record_info(record_id)` 查看具体失败原因。

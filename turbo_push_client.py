#!/usr/bin/env python3
"""
Turbo Push Python Client
用于大模型调用 Turbo Push API 进行多平台内容发布
"""

import subprocess
import json
import time
import os
import sys
import platform
import requests


class TurboPushService:
    """Turbo Push 服务管理类"""

    def __init__(self, binary_path=None, binary_dir="."):
        """
        初始化服务管理器
        :param binary_path: turbo_push 二进制文件路径(可选)
        :param binary_dir: 二进制文件所在目录(默认当前目录)
        """
        self.binary_dir = binary_dir
        self.binary_path = binary_path or self._find_binary()
        self.process = None
        self.config = None

    @staticmethod
    def _get_platform_suffix():
        """
        获取当前平台对应的二进制文件后缀
        :return: 文件名后缀
        """
        system = platform.system()
        if system == "Windows":
            return ".exe"
        elif system == "Darwin":
            return "_mac"
        elif system == "Linux":
            return "_linux"
        else:
            return ""

    @staticmethod
    def _find_binary(search_dir="."):
        """
        根据当前平台自动查找合适的二进制文件
        :param search_dir: 搜索目录
        :return: 二进制文件路径
        """
        system = platform.system()
        machine = platform.machine()
        
        # 尝试的文件名列表(按优先级排序)
        possible_names = []
        
        if system == "Windows":
            possible_names = [
                "turbo_push.exe",
                "turbo_push_windows.exe",
                "turbo_push_win.exe",
            ]
        elif system == "Darwin":
            # macOS 上区分 ARM 和 Intel 架构
            if "arm64" in machine.lower():
                # Apple Silicon (M1, M2, M3 等)
                possible_names = [
                    "turbo_push",
                    "turbo_push_arm64",
                    "turbo_push_apple_silicon",
                    "turbo_push_m1",
                    "turbo_push_mac",
                ]
            else:
                # Intel (x86_64)
                possible_names = [
                    "turbo_push",
                    "turbo_push_intel",
                    "turbo_push_x86_64",
                    "turbo_push_mac_intel",
                    "turbo_push_mac",
                ]
        elif system == "Linux":
            possible_names = [
                "turbo_push",
                "turbo_push_linux",
                "turbo_push_linux_amd64",
                "turbo_push_linux_arm64",
            ]
        else:
            possible_names = ["turbo_push"]

        # 在指定目录中搜索
        for name in possible_names:
            full_path = os.path.join(search_dir, name)
            if os.path.exists(full_path):
                arch_info = f" ({'ARM64' if 'arm' in machine.lower() else 'Intel'})" if system == "Darwin" else ""
                print(f"✅ 找到二进制文件: {full_path} ({system}{arch_info})")
                return full_path

        # 找不到文件,返回最可能使用的文件名
        preferred = possible_names[0]
        print(f"⚠️ 未找到二进制文件,将尝试使用: {preferred}")
        return os.path.join(search_dir, preferred)

    @staticmethod
    def get_system_info():
        """
        获取系统信息
        :return: 系统信息字典
        """
        return {
            "system": platform.system(),
            "machine": platform.machine(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "working_dir": os.getcwd()
        }

    def start(self):
        """
        启动 Turbo Push 服务
        :return: 服务配置信息
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
                    stderr = self.process.stderr.read()
                    raise RuntimeError(f"Turbo Push 服务启动失败: {stderr}")

                # 检查标准输出
                line = self.process.stdout.readline()
                if line:
                    line = line.strip()
                    if line.startswith("{"):
                        self.config = json.loads(line)
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


class TurboPushClient:
    """Turbo Push API 客户端"""

    def __init__(self, base_url="http://127.0.0.1:8910", auth_token=None):
        """
        初始化客户端
        :param base_url: API 基础地址
        :param auth_token: 认证令牌
        """
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

    def get_platforms(self, enable=None, article=None, graph_text=None, video=None):
        """获取平台列表"""
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

    def create_article(self):
        """创建文章草稿"""
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

    def publish_article(self, article_id, post_accounts, sync_draft=False):
        """
        发布文章
        :param article_id: 文章 ID(rid)
        :param post_accounts: 发布账号列表
        :param sync_draft: 是否同步为草稿
        """
        data = {
            "syncDraft": sync_draft,
            "postAccounts": post_accounts
        }
        return self._request("POST", f"/sse/article/{article_id}", data=data)

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


def quick_start_turbo_push(binary_dir="."):
    """
    快速启动 Turbo Push 并返回客户端(自动检测平台)
    :param binary_dir: 二进制文件所在目录(默认当前目录)
    :return: TurboPushClient 实例
    """
    service = TurboPushService(binary_dir=binary_dir)
    config = service.start()
    return service.get_client()


def quick_start_with_platform_info(binary_dir="."):
    """
    快速启动并显示平台信息
    :param binary_dir: 二进制文件所在目录
    :return: TurboPushClient 实例
    """
    system_info = TurboPushService.get_system_info()
    print(f"🖥️  操作系统: {system_info['system']}")
    print(f"💻 架构: {system_info['machine']}")
    print(f"📂 工作目录: {system_info['working_dir']}")
    print()
    
    service = TurboPushService(binary_dir=binary_dir)
    config = service.start()
    return service.get_client()


# 平台类型对照
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

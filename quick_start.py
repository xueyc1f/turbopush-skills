#!/usr/bin/env python3
"""
Turbo Push 快速开始示例

演示如何快速启动服务并使用 API 发布内容
"""

import subprocess
import json
import time
import os
import requests


class TurboPushService:
    """Turbo Push 服务管理类"""
    def __init__(self, binary_path=None, binary_dir="."):
        """初始化服务管理器(自动检测平台)"""
        self.binary_dir = binary_dir
        self.binary_path = binary_path or self._find_binary(binary_dir)
        self.process = None
        self.config = None

    @staticmethod
    def _find_binary(search_dir="."):
        """根据当前平台自动查找合适的二进制文件"""
        import platform
        system = platform.system()
        machine = platform.machine()
        
        possible_names = []
        if system == "Windows":
            possible_names = ["turbo_push.exe", "turbo_push_windows.exe", "turbo_push_win.exe"]
        elif system == "Darwin":
            # macOS 区分 ARM 和 Intel
            if "arm64" in machine.lower():
                possible_names = ["turbo_push", "turbo_push_arm64", "turbo_push_apple_silicon", "turbo_push_m1", "turbo_push_mac"]
            else:
                possible_names = ["turbo_push", "turbo_push_intel", "turbo_push_x86_64", "turbo_push_mac_intel", "turbo_push_mac"]
        elif system == "Linux":
            if "arm64" in machine.lower():
                possible_names = ["turbo_push", "turbo_push_linux_arm64", "turbo_push_linux"]
            else:
                possible_names = ["turbo_push", "turbo_push_linux_amd64", "turbo_push_linux"]
        else:
            possible_names = ["turbo_push"]

        for name in possible_names:
            full_path = os.path.join(search_dir, name)
            if os.path.exists(full_path):
                arch_info = f" ({'ARM64' if 'arm' in machine.lower() else 'Intel'})" if system == "Darwin" else ""
                print(f"✅ 找到二进制文件: {full_path} ({system}{arch_info})")
                return full_path

        preferred = possible_names[0]
        print(f"⚠️ 未找到二进制文件,将尝试使用: {preferred}")
        return os.path.join(search_dir, preferred)

    def stop(self):
        """停止服务"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

    def get_client(self):
        """获取客户端"""
        if not self.config:
            raise RuntimeError("服务未启动")
        return TurboPushClient(
            base_url=f"http://127.0.0.1:{self.config['port']}",
            auth_token=self.config['auth']
        )


class TurboPushClient:
    """Turbo Push API 客户端"""
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

    def login(self, code):
        """登录"""
        result = self._request("POST", "/user/login", data={"code": code})
        if result.get("code") == 0:
            data = result.get("data", {})
            self.auth_token = data.get("secure", {}).get("openID")
            return data
        return None

    def get_logged_accounts(self):
        """获取已登录账号"""
        return self._request("GET", "/account/logged")

    def create_graph_text(self, files, title, desc, thumb):
        """创建图文"""
        data = {"files": files, "title": title, "desc": desc, "thumb": thumb}
        result = self._request("POST", "/graphText/create", data=data)
        if result.get("code") == 0:
            return result.get("data")
        return None

    def publish_graph_text(self, graph_text_id, post_accounts):
        """发布图文"""
        data = {"syncDraft": False, "postAccounts": post_accounts}
        return self._request("POST", f"/sse/graphText/{graph_text_id}", data=data)

    def get_publish_records(self, status=1, size=5):
        """获取发布记录"""
        return self._request("GET", "/record/list", params={"status": status, "size": size, "current": 1})

def main():
    # ========== 步骤 1: 显示系统信息 ==========
    print("🔍 检测系统环境...")
    import platform as sys_platform
    
    system_info = {
        "system": sys_platform.system(),
        "machine": sys_platform.machine(),
        "os_version": sys_platform.version(),
        "working_dir": os.getcwd()
    }
    
    print(f"✅ 检测完成:")
    print(f"   操作系统: {system_info['system']}")
    print(f"   架构: {system_info['machine']}")
    print(f"   Python: {system_info['python_version']}")
    print(f"   工作目录: {system_info['working_dir']}")
    
    # ========== 步骤 2: 启动服务 ==========
    print("\n🚀 正在启动 Turbo Push 服务...")
    service = TurboPushService(binary_dir="./")
    config = service.start()

    print(f"\n✅ 服务已成功启动!")
    print(f"   PID: {config['pid']}")
    print(f"   Port: {config['port']}")
    print(f"   Login: {'是' if config['login'] else '否'}")
    print(f"   Home: {config['home']}")

    # ========== 步骤 2: 获取客户端 ==========
    client = service.get_client()

    # ========== 步骤 3: 获取已登录账号 ==========
    print("\n📋 正在获取账号列表...")
    accounts = client.get_logged_accounts()
    account_list = accounts.get("data", [])

    print(f"✅ 找到 {len(account_list)} 个已登录账号:")
    for i, acc in enumerate(account_list[:5], 1):
        print(f"   {i}. {acc['name']} - {acc['platform']['name']}")

    if not account_list:
        print("\n❌ 没有已登录账号,请先登录")
        return

    # ========== 步骤 4: 登录(如果需要) ==========
    if not config["login"]:
        print("\n🔐 需要登录,请从 Turbo Push 客户端获取验证码")

        code = input("📝 请输入验证码: ").strip()
        if code:
            user_info = client.login(code)
            if user_info:
                print(f"✅ 登录成功: {user_info['name']}")
            else:
                print("❌ 登录失败")
                return
        else:
            print("❌ 未输入验证码")
            return
    else:
        print("\n✅ 已登录,跳过登录步骤")

    # ========== 步骤 5: 选择账号 ==========
    print("\n🎯 选择要发布到的平台:")
    for i, acc in enumerate(account_list, 1):
        print(f"   {i}. {acc['name']} {acc['platform']['plat_type']}")

    print(f"\n💡 支持的内容类型:")
    print("   1. 图文(graph_text) - 微信视频号、小红书、抖音等")
    print("   2. 视频(video) - B站、抖音、快手等")
    print("   3. 文章(article) - 微信公众号、B站专栏、CSDN等")

    # ========== 示例: 创建图文 ==========
    print("\n" + "="*50)
    print("📝 示例: 创建并发布图文")
    print("="*50)

    # 创建图文
    graph_text_id = client.create_graph_text(
        files=["/path/to/image1.jpg", "/path/to/image2.jpg"],
        title="精彩图文标题",
        desc="这是图文的描述内容 #热门话题 #推荐",
        thumb=["/path/to/cover.jpg"]
    )

    if graph_text_id:
        print(f"✅ 图文创建成功: ID = {graph_text_id}")

        # 配置发布(以微信视频号为例)
        wechat_account = None
        xiaohongshu_account = None

        for acc in account_list:
            pt = acc["platform"]["plat_type"]
            if pt == "wechat-video" and not wechat_account:
                wechat_account = acc
            elif pt == "xiaohongshu" and not xiaohongshu_account:
                xiaohongshu_account = acc

        post_accounts = []

        if wechat_account:
            post_accounts.append({
                "id": wechat_account["id"],
                "settings": {
                    "location": "北京",
                    "collection": ["我的合集"],
                    "source": 4,
                    "platType": "wechat-video"
                }
            })
            print(f"   ➕ 已添加微信视频号: {wechat_account['name']}")

        if xiaohongshu_account:
            post_accounts.append({
                "id": xiaohongshu_account["id"],
                "settings": {
                    "location": "上海",
                    "collection": "生活",
                    "origin": True,
                    "source": 3,
                    "lookScope": 0,
                    "platType": "xiaohongshu"
                }
            })
            print(f"   ➕ 已添加小红书: {xiaohongshu_account['name']}")

        if post_accounts:
            # 发布
            print(f"\n🚀 正在发布到 {len(post_accounts)} 个平台...")
            result = client.publish_graph_text(
                graph_text_id=graph_text_id,
                post_accounts=post_accounts
            )

            if result.get("code") == 0:
                print("✅ 发布请求已发送")
                print("   请查看客户端查看发布进度")
            else:
                print(f"❌ 发布失败: {result.get('msg')}")
        else:
            print("⚠️ 没有找到支持图文的账号")
    else:
        print("❌ 图文创建失败")

    # ========== 快速查询发布结果 ==========
    print("\n" + "="*50)
    print("📊 查询发布记录")
    print("="*50)

    records = client.get_publish_records(status=1, size=5)
    record_list = records.get("data", {}).get("list", [])

    if record_list:
        print(f"✅ 找到 {len(record_list)} 条发布记录:")
        for i, record in enumerate(record_list, 1):
            status_map = {1: "发布中", 2: "全部失败", 3: "部分成功", 4: "全部成功"}
            status_text = status_map.get(record.get("status"), "未知")
            print(f"   {i}. 记录ID: {record['id']} - 状态: {status_text} - 耗时: {record.get('since', 'N/A')}")
    else:
        print("ℹ️ 暂无发布记录")

    # ========== 完成 ==========
    print("\n" + "="*50)
    print("✅ 演示完成!")
    print("="*50)
    print(f"\n💡 提示:")
    print(f"   - 客户端: {config['home']}")
    print(f"   - Chrome: {config['chrome']}")
    print(f"   - API文档: 查看 turbo-pub.md")
    
    # ========== 停止服务 ==========
    print("\n" + "="*50)
    print("正在停止 Turbo Push 服务...")
    print("="*50)
    service.stop()
    print("✅ 服务已停止,所有任务已完成")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n🔧 尝试清理服务进程...")
        # 如果发生异常,尝试清理进程
        if 'service' in locals() and service.process:
            service.stop()


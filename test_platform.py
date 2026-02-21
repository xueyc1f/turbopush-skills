#!/usr/bin/env python3
"""
跨平台测试脚本
验证 TurboPushService 的自动平台检测功能
"""

import os
import sys

# 添加 skills 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from turbo_push_client import TurboPushService


def test_platform_detection():
    """测试平台检测功能"""
    print("="*60)
    print("🔍 Turbo Push 跨平台检测测试")
    print("="*60)
    
    # 1. 显示系统信息
    print("\n📊 系统信息:")
    system_info = TurboPushService.get_system_info()
    print(f"   操作系统: {system_info['system']}")
    print(f"   架构: {system_info['machine']}")
    print(f"   Python 版本: {system_info['python_version']}")
    print(f"   工作目录: {system_info['working_dir']}")
    
    # 2. macOS 架构判断
    if system_info["system"] == "Darwin":
        machine = system_info["machine"]
        print(f"\n🍎 macOS 芯片检测:")
        if "arm64" in machine.lower():
            print(f"   ✅ Apple Silicon (ARM64)")
            print(f"      芯片: M1, M2, M3, M4 等系列")
        else:
            print(f"   ✅ Intel (x86_64)")
            print(f"      架构: 双核/四核/六核等 Intel 处理器")
    
    # 2. 检测二进制文件
    print("\n📦 二进制文件检测:")
    binary_path = TurboPushService._find_binary(search_dir=".")
    print(f"   选择的文件: {binary_path}")
    
    # 3. 检查文件是否存在
    exists = os.path.exists(binary_path)
    print(f"   文件存在: {'是 ✓' if exists else '否 ✗'}")
    
    # 4. 文件信息
    if exists:
        file_size = os.path.getsize(binary_path)
        file_size_mb = file_size / (1024 * 1024)
        print(f"   文件大小: {file_size_mb:.2f} MB")
    
    
    # 5. 测试优先级列表
    print("\n🔍 文件检测优先级:")
    system = system_info['system']
    machine = system_info['machine']
    
    if system == "Windows":
        names = ["turbo_push.exe", "turbo_push_windows.exe", "turbo_push_win.exe"]
    elif system == "Darwin":
        # macOS 上区分 ARM 和 Intel
        if "arm64" in machine.lower():
            # Apple Silicon
            names = [
                "turbo_push",
                "turbo_push_arm64",
                "turbo_push_apple_silicon",
                "turbo_push_m1",
                "turbo_push_mac"
            ]
        else:
            # Intel
            names = [
                "turbo_push",
                "turbo_push_intel",
                "turbo_push_x86_64",
                "turbo_push_mac_intel",
                "turbo_push_mac"
            ]
    elif system == "Linux":
        # Linux 上区分架构
        if "arm64" in machine.lower():
            # ARM64
            names = [
                "turbo_push",
                "turbo_push_linux_arm64",
                "turbo_push_linux",
            ]
        else:
            # AMD64
            names = [
                "turbo_push",
                "turbo_push_linux_amd64",
                "turbo_push_linux",
            ]
    else:
        names = ["turbo_push"]
    
    for i, name in enumerate(names, 1):
        full_path = os.path.join(".", name)
        exists = os.path.exists(full_path)
        status = "✓" if exists else "✗"
        print(f"   {i}. {name:30s} {status}")
    
    # 6. 推荐配置
    print("\n💡 推荐配置:")
    if system == "Windows":
        print("   - 保留: turbo_push.exe")
        print("   - 可选: turbo_push_windows.exe, turbo_push_win.exe")
    elif system == "Darwin":
        machine = system_info["machine"]
        if "arm64" in machine.lower():
            print("   - Apple Silicon 芯片:")
            print("     - 保留: turbo_push")
            print("     - 可选: turbo_push_arm64, turbo_push_m1")
            print("   ✅ 建议: 使用 Apple Silicon 编译的版本性能最佳")
        else:
            print("   - Intel 芯片:")
            print("     - 保留: turbo_push")
            print("     - 可选: turbo_push_intel")
            print("   ✅ 建议: 使用 Rosetta 2 兼容模式运行 ARM 版本可能性能更优")
    elif system == "Linux":
        machine = system_info["machine"]
        if "arm64" in machine.lower():
            print("   - ARM64 架构:")
            print("     - 保留: turbo_push")
            print("     - 可选: turbo_push_linux_arm64")
        else:
            print("   - x86_64 架构:")
            print("     - 保留: turbo_push")
            print("     - 可选: turbo_push_linux_amd64")
    else:
        print(f"   - 保留: turbo_push (检测到 {system})")

    print("\n" + "="*60)
    print("✅ 测试完成")
    print("="*60)


def test_service_creation():
    """测试服务创建(不实际启动)"""
    print("\n🧪 服务创建测试:")
    
    try:
        # 创建服务实例
        service = TurboPushService(binary_dir=".")
        print(f"   ✅ 服务实例创建成功")
        print(f"   ✅ 二进制路径: {service.binary_path}")
        
        # 不实际启动,避免端口冲突
        print(f"   ℹ️  跳过实际启动(测试模式下)")
        
    except Exception as e:
        print(f"   ❌ 创建失败: {e}")


if __name__ == "__main__":
    print()
    test_platform_detection()
    test_service_creation()
    print("\n💡 提示:")
    print("   - 如果二进制文件不存在,请手动放置到 skills/ 目录")
    print("   - Windows 用户使用 turbo_push.exe")
    print("   - macOS/Linux 用户使用 turbo_push")
    print()

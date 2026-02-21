# 更新摘要

## 最新更新内容

### macOS ARM/Intel 架构区分 (v2.2)

#### 1. macOS 芯片检测增强
- ✅ 新增 macOS ARM64 和 Intel 架构检测
- ✅ Apple Silicon (M1/M2/M3/M4) 和 Intel Mac 使用不同的二进制文件
- ✅ 优化性能: Apple Silicon 原生 ARM64 版本性能最佳
- ✅ Intel Mac 支持通过 Rosetta 2 运行 ARM 版本

#### 2. macOS 架构检测优先级

**Apple Silicon (ARM64):**
- `turbo_push` → `turbo_push_arm64` → `turbo_push_apple_silicon` → `turbo_push_m1` → `turbo_push_mac`

**Intel (x86_64):**
- `turbo_push` → `turbo_push_intel` → `turbo_push_x86_64` → `turbo_push_mac_intel` → `turbo_push_mac`

#### 3. Linux 架构支持
- ✅ Linux AMD64 (x86_64) 和 ARM64 架构分别支持
- ✅ AMD64: turbo_push → turbo_push_linux_amd64 → turbo_push_linux
- ✅ ARM64: turbo_push → turbo_push_linux_arm64 → turbo_push_linux

#### 4. 更新文件
- `turbo_push_client.py` - 添加 macOS ARM64/Intel 检测
- `CROSS_PLATFORM.md` - 更新 macOS 架构说明
- `test_platform.py` - 添加架构检测测试
- `FILES.md` - 添加 ARM/Intel 配置说明
- `README.md` - 更新跨平台示例

## 使用方式

### 自动检测 ARM/Intel (推荐)
```python
from turbo_push_client import TurboPushService

service = TurboPushService(binary_dir="./")
config = service.start()  # 自动检测平台和架构
```

### 查看芯片信息
```python
from turbo_push_client import TurboPushService

system_info = TurboPushService.get_system_info()
print(f"架构: {system_info['machine']}")  # arm64 或 x86_64
```

## 使用方式

### 简单方式(自动检测)
```python
from turbo_push_client import TurboPushService

# 只需要这一行,自动检测平台
service = TurboPushService(binary_dir="./")
config = service.start()
```

### 查看系统信息
```python
from turbo_push_client import TurboPushService

system_info = TurboPushService.get_system_info()
print(system_info)
```

### 快速启动
```python
from turbo_push_client import quick_start_turbo_push

client = quick_start_turbo_push(binary_dir="./")
```

## 文件变更

### 修改的文件
- `turbo_push_client.py` - 添加 `_find_binary()`, `get_system_info()` 方法

### 新增的文件
- `CROSS_PLATFORM.md` - 跨平台使用指南
- `test_platform.py` - 测试脚本

### 更新的文件
- `README.md`
- `FILES.md`
- `turbo-pub-tool.py.md`

## 版本信息

- 当前版本: v2.2
- 发布日期: 2025-02-20
- 兼容平台: Windows, macOS (ARM64/Intel), Linux (amd64/arm64)

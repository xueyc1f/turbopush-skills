# 跨平台使用指南

Turbo Push 支持在 Windows、macOS 和 Linux 上运行,系统会自动选择合适的二进制文件。

## 支持的平台

### Windows
- 兼容: Windows 7/8/10/11, Windows Server 2012+
- 二进制文件: `turbo_push.exe`, `turbo_push_windows.exe`, `turbo_push_win.exe`

### macOS
- 兼容: macOS 10.13+ (High Sierra 及以上)
- 架构区分:
  - **Apple Silicon (ARM64)**: M1, M2, M3, M4 等芯片
  - **Intel (x86_64)**: Intel 芯片的 Mac
- 二进制文件:
  - **ARM64**: `turbo_push`, `turbo_push_arm64`, `turbo_push_apple_silicon`, `turbo_push_m1`, `turbo_push_mac`
  - **Intel**: `turbo_push`, `turbo_push_intel`, `turbo_push_x86_64`, `turbo_push_mac_intel`

### Linux
- 兼容: Ubuntu 16.04+, CentOS 7+, Debian 8+
- 架构支持: amd64, arm64
- 二进制文件: `turbo_push`, `turbo_push_linux`, `turbo_push_linux_amd64`, `turbo_push_linux_arm64`

## 自动平台检测

`TurboPushService` 类会自动检测操作系统和架构并尝试使用对应的二进制文件:

```python
from turbo_push_client import TurboPushService

# 自动检测平台和架构
service = TurboPushService(binary_dir="./")
config = service.start()

# 查看系统信息
system_info = TurboPushService.get_system_info()
print(f"操作系统: {system_info['system']}")
print(f"架构: {system_info['machine']}")
```

### macOS ARM64 vs Intel 检测

**检测 macOS 架构:**
```python
import platform

if platform.system() == "Darwin":
    machine = platform.machine()
    if "arm64" in machine.lower():
        # Apple Silicon
        print("✅ 检测到 Apple Silicon (ARM64)")
    else:
        # Intel
        print("✅ 检测到 Intel (x86_64)")
```

### 自动检测逻辑

系统会按以下优先级查找二进制文件:

**Windows:**
1. `turbo_push.exe`
2. `turbo_push_windows.exe`
3. `turbo_push_win.exe`

**macOS ARM64 (Apple Silicon):**
1. `turbo_push`
2. `turbo_push_arm64`
3. `turbo_push_apple_silicon`
4. `turbo_push_m1`
5. `turbo_push_mac`

**macOS Intel:**
1. `turbo_push`
2. `turbo_push_intel`
3. `turbo_push_x86_64`
4. `turbo_push_mac_intel`

**Linux:**
1. `turbo_push`
2. `turbo_push_linux`

**Linux amd64:**
1. `turbo_push`
2. `turbo_push_linux_amd64`

**Linux arm64:**
1. `turbo_push`
2. `turbo_push_linux_arm64`

## 手动指定二进制文件

如果需要使用特定的二进制文件,可以指定完整路径:

```python
from turbo_push_client import TurboPushService

# 指定某个特定的二进制文件
service = TurboPushService(binary_path="./turbo_push_custom")
config = service.start()
```

## 二进制文件配置

### skills/ 目录结构

```
skills/
├── turbo_push.exe           # Windows 主文件
├── turbo_push               # macOS/Linux 主文件(通用)
├── turbo_push_arm64         # macOS ARM64 专用(M1/M2/M3)
├── turbo_push_intel         # macOS Intel 专用
├── turbo_push_linux         # Linux 主文件
├── turbo_push_linux_amd64   # Linux AMD64 专用
├── turbo_push_linux_arm64   # Linux ARM64 专用
└── ...
```

### 推荐配置

**最简单配置:**
- `turbo_push.exe` (Windows)
- `turbo_push` (macOS/Linux 通用)

**跨平台完整配置:**
```
skills/
├── turbo_push.exe           # Windows
├── turbo_push_arm64         # macOS Apple Silicon
├── turbo_push_intel         # macOS Intel
├── turbo_push_linux_amd64   # Linux AMD64
└── turbo_push_linux_arm64   # Linux ARM64
```

**macOS 专用配置:**
```
skills/
├── turbo_push               # macOS 通用
├── turbo_push_arm64         # Apple Silicon (M1/M2/M3/M4)
├── turbo_push_intel         # Intel Mac
└── ...
```
skills/
├── turbo_push              # 通用二进制 (macOS/Linux)
├── turbo_push.exe          # Windows 二进制
├── turbo_push_windows.exe  # Windows 专用(可选)
├── turbo_push_mac          # macOS 专用(可选)
└── turbo_push_linux        # Linux 专用(可选)
```

### 推荐配置

**最简单配置:**
- `turbo_push` (macOS/Linux) 或 `turbo_push.exe` (Windows)

**多平台配置:**
```
skills/
├── turbo_push.exe       # Windows 使用
├── turbo_push           # macOS/Linux 使用
└── ...
```

## 各平台使用示例

### Windows

```python
from turbo_push_client import TurboPushService

# 方式1: 自动检测
service = TurboPushService(binary_dir=r"C:\path\to\skills")
config = service.start()

# 方式2: 指定路径
service = TurboPushService(binary_path=r"C:\path\to\turbo_push.exe")
config = service.start()

client = service.get_client()
# ... 使用客户端 ...
service.stop()
```

### macOS

```python
from turbo_push_client import TurboPushService

# 自动检测
service = TurboPushService(binary_dir="/path/to/skills")
config = service.start()

client = service.get_client()
# ... 使用客户端 ...
service.stop()
```

### Linux

```python
from turbo_push_client import TurboPushService

# 自动检测
service = TurboPushService(binary_dir="/path/to/skills")
config = service.start()

client = service.get_client()
# ... 使用客户端 ...
service.stop()
```

## 查看系统信息

使用静态方法查看当前系统信息:

```python
from turbo_push_client import TurboPushService

# 获取系统信息
system_info = TurboPushService.get_system_info()

print(f"操作系统: {system_info['system']}")
print(f"架构: {system_info['machine']}")
print(f"系统版本: {system_info['os_version']}")
print(f"Python 版本: {system_info['python_version']}")
print(f"工作目录: {system_info['working_dir']}")
```

输出示例:
```
操作系统: Darwin
架构: arm64
系统版本: Darwin Kernel Version 21.6.0
Python 版本: 3.10.6
工作目录: /Users/username/projects/turbo_push/skills
```

## 快速启动方法

### 方式1: 自动检测(推荐)

```python
from turbo_push_client import quick_start_turbo_push

# 自动检测平台并启动
client = quick_start_turbo_push(binary_dir="./")
```

### 方式2: 显示平台信息

```python
from turbo_push_client import quick_start_with_platform_info

# 显示平台信息并启动
client = quick_start_with_platform_info(binary_dir="./")
```

输出:
```
🖥️  操作系统: Darwin
💻 架构: arm64
📂 工作目录: /Users/username/projects/turbo_push/skills

✅ 找到二进制文件: ./turbo_push (Darwin)
✅ 服务已启动 (PID: 47755, 端口: 8910)
```

## 二进制文件权限

### Linux/macOS
如果遇到权限错误,可尝试手动设置:

```bash
chmod +x ./skills/turbo_push
```

或:
```bash
chmod 0755 ./skills/turbo_push
```

### Windows
确保 `.exe` 文件有执行权限,通常不需要额外设置。

## 故障排查

### 问题1: 找不到二进制文件

**错误信息:**
```
⚠️ 未找到二进制文件,将尝试使用: turbo_push
RuntimeError: 服务启动失败
```

**解决方案:**
1. 确认 `turbo_push` 或 `turbo_push.exe` 在 `skills/` 目录中
2. 查看当前系统是否支持
3. 手动指定正确的文件路径

### 问题2: 权限错误

**错误信息:**
```
Permission denied: './turbo_push'
```

**解决方案:**
```bash
chmod +x ./turbo_push
```

### 问题3: 二进制文件与系统不匹配

**错误信息:**
```
Exec format error
cannot execute binary file
```

**解决方案:**
1. 确认使用的是对应系统的二进制文件
2. Windows 使用 `.exe` 文件
3. macOS 使用 macOS 编译的文件
4. Linux 使用 Linux 编译的文件

## 最佳实践

1. **保持目录简洁**
   ```
   skills/
   ├── turbo_push.exe    # Windows
   ├── turbo_push        # macOS/Linux
   └── ...
   ```

2. **使用自动检测**
   ```python
   service = TurboPushService(binary_dir="./")
   ```

3. **添加系统信息日志**
   ```python
   system_info = TurboPushService.get_system_info()
   print(f"系统: {system_info['system']}")
   ```

4. **错误处理**
   ```python
   try:
       service = TurboPushService()
       config = service.start()
   except RuntimeError as e:
       print(f"启动失败: {e}")
       sys.exit(1)
   finally:
       service.stop()
   ```

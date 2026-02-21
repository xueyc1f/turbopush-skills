# 服务生命周期管理

本文档说明 Turbo Push 服务的启动、使用和停止的最佳实践。

## 正确的服务生命周期

```
1. 启动服务 → service.start()
2. 获取客户端 → service.get_client()
3. 执行操作 → client.*()
4. 停止服务 → service.stop()
```

## 完整示例

### 标准流程

```python
from turbo_push_client import TurboPushService

# 1. 启动服务
service = TurboPushService(binary_path="./turbo_push")
config = service.start()

# 2. 获取客户端
client = service.get_client()

# 3. 执行发布任务
accounts = client.get_logged_accounts()
graph_text_id = client.create_graph_text(files, title, desc, thumb)
result = client.publish_graph_text(graph_text_id, post_accounts)

# 4. 停止服务
service.stop()
print("✅ 服务已停止")
```

### 使用 try-finally 确保清理

```python
from turbo_push_client import TurboPushService

service = TurboPushService(binary_path="./turbo_push")

try:
    # 启动服务
    config = service.start()
    client = service.get_client()

    # 执行操作
    # ... API 调用 ...

finally:
    # 无论成功或失败,都停止服务
    service.stop()
```

### 使用上下文管理器 (推荐)

创建一个上下文管理器,自动管理服务生命周期:

```python
from contextlib import contextmanager
from turbo_push_client import TurboPushService

@contextmanager
def turbo_push_service(binary_path="./turbo_push"):
    """
    Turbo Push 服务上下文管理器
    自动处理服务的启动和停止
    """
    service = TurboPushService(binary_path=binary_path)
    config = service.start()
    
    try:
        yield service, config
    finally:
        service.stop()
        print("✅ Turbo Push 服务已自动停止")

# 使用示例
with turbo_push_service() as (service, config):
    client = service.get_client()
    # ... 执行操作 ...
    
# 退出 with 块后自动停止服务
```

## 发布后的处理

### 场景1: 发布后立即停止

```python
service = TurboPushService()
config = service.start()
client = service.get_client()

# 发布
result = client.publish_graph_text(graph_text_id, post_accounts)

# 验证发布请求是否接收
if result.get("code") == 0:
    print("✅ 发布请求已接收")
    print("📊 后台正在处理发布任务...")
    
    # 可以选择:
    # 选项A: 立即停止服务(发布任务在后台继续)
    service.stop()
    print("✅ 服务已停止,发布任务在后台继续")
    
    # 选项B: 等待发布完成再停止
    # time.sleep(30)  # 等待一些时间
    # service.stop()
```

### 场景2: 发布完成后再停止

```python
service = TurboPushService()
config = service.start()
client = service.get_client()

# 发布
result = client.publish_graph_text(graph_text_id, post_accounts)

if result.get("code") == 0:
    # 监控发布进度
    import time
    print("⏳ 等待发布完成...")
    
    while True:
        time.sleep(10)  # 每10秒检查一次
        records = client.get_publish_records(status=1, size=1)
        latest = records.get("data", {}).get("list", [])
        
        if not latest:
            break
        
        record = latest[0]
        details = client.get_publish_record_info(record["id"])
        
        # 检查是否全部完成
        all_done = all(d["success"] for d in details.get("data", []))
        
        if all_done or record.get("status") in [2, 4]:  # 全部成功或全部失败
            print("✅ 发布已完成")
            break
        elif record.get("status") == 1:  # 还在发布中
            print(f"⏳ 发布中... 已耗时 {record.get('since', 'N/A')}")
        else:
            print(f"⚠️ 发布状态: {record.get('status')}")
            break
    
    # 停止服务
    service.stop()
    print("✅ 服务已停止")
```

## 错误处理

### 带错误处理的服务管理

```python
from turbo_push_client import TurboPushService

def publish_with_auto_stop(binary_path, post_data):
    """
    带自动停止服务的发布函数
    """
    service = TurboPushService(binary_path=binary_path)
    
    try:
        # 启动服务
        config = service.start()
        print(f"✅ 服务已启动 (PID: {config['pid']})")
        
        # 获取客户端
        client = service.get_client()
        
        # 执行发布
        graph_text_id = client.create_graph_text(**post_data)
        result = client.publish_graph_text(
            graph_text_id,
            post_accounts=post_data["accounts"]
        )
        
        if result.get("code") == 0:
            print("✅ 发布成功")
            return True
        else:
            print(f"❌ 发布失败: {result.get('msg')}")
            return False
            
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # 无论成功还是失败,都停止服务
        try:
            service.stop()
            print("✅ 服务已停止")
        except Exception as e:
            print(f"⚠️ 停止服务时出错: {str(e)}")
```

## 注意事项

### 何时停止服务

**立即停止的场景:**
- 发布请求已成功接收
- 不需要监控发布进度
- 需要释放系统资源

**延时停止的场景:**
- 需要监控发布进度
- 需要获取发布结果
- 需要处理发布完成后的操作

### 停止服务的影响

停止服务后:
- ✅ 浏览器窗口会被关闭
- ✅ 所有进行中的发布任务会继续完成
- ✅ API 请求会返回错误
- ✅ SSE 连接会断开

### 资源清理

Turbo Push 会自动清理:
- 浏览器进程
- 临时文件
- 数据库连接

### 异常情况处理

如果程序崩溃或异常退出:

```python
import atexit
from turbo_push_client import TurboPushService

# 全局服务实例
_global_service = None

def cleanup_service():
    """清理函数,在程序退出时自动调用"""
    global _global_service
    if _global_service:
        try:
            _global_service.stop()
            print("✅ 程序退出时自动停止了服务")
        except:
            pass

# 注册清理函数
atexit.register(cleanup_service)

def start_global_service():
    """启动全局服务"""
    global _global_service
    _global_service = TurboPushService()
    return _global_service.start()

# 在程序开始时
start_global_service()

# 程序正常或异常退出时会自动停止服务
```

## 多次启动和停止

```python
from turbo_push_client import TurboPushService

def multiple_tasks(tasks):
    """
    执行多个任务,每个任务独立启动和停止服务
    """
    for task in tasks:
        print(f"\n📋 处理任务 {tasks.index(task) + 1}/{len(tasks)}")
        
        service = TurboPushService(config=task["config"])
        
        try:
            # 启动
            service.start()
            client = service.get_client()
            
            # 执行任务
            print(f"🚀 正在发布: {task['title']}")
            result = client.publish_graph_text(
                task["content_id"],
                task["accounts"]
            )
            
            if result.get("code") == 0:
                print(f"✅ 任务 {tasks.index(task) + 1} 完成")
            else:
                print(f"❌ 任务 {tasks.index(task) + 1} 失败")
                
        finally:
            # 每个任务完成后都停止服务
            service.stop()
            print(f"✅ 任务 {tasks.index(task) + 1} 服务已停止")
```

## 最佳实践总结

1. **始终使用 finally 确保停止服务**
   ```python
   try:
       service.start()
       # ... 操作 ...
   finally:
       service.stop()
   ```

2. **使用上下文管理器自动管理生命周期**
   ```python
   with turbo_push_service() as service:
       client = service.get_client()
       # ... 操作 ...
   ```

3. **异常处理要停止服务**
   ```python
   except Exception as e:
       print(f"错误: {e}")
       raise
   finally:
       service.stop()
   ```

4. **长期运行程序使用 atexit**
   ```python
   service.start()
   atexit.register(service.stop)
   ```

5. **发布完成后即可停止**
   - 发布任务会继续在后台完成
   - 不需要等待发布完成
   - 节省系统资源

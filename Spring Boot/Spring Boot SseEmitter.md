# Spring Boot SseEmitter

SseEmitter 是 Spring Framework 4.2+ 提供的用于服务器发送事件（Server-Sent Events, SSE） 的类，允许服务器向客户端单向实时推送数据

适用场景:

1. 实时通知（新闻推送、告警提醒）
2. 进度更新（文件处理进度、任务状态）
3. 日志流（实时输出日志到前端）
4. 数据仪表盘（实时数据图表更新）
5. 兼容性要求高（需支持旧版浏览器）

适用于需要服务器主动向客户端推送数据的场景，尤其适合实时性要求高但交互简单的应用。若需双向通信，建议使用 WebSocket。

## 基本用法
### 服务端实现
```java
@RestController
@RequestMapping("/sse")
public class SseController {

    // 保存所有连接的 emitter
    private final ConcurrentHashMap<String, SseEmitter> emitters = new ConcurrentHashMap<>();

    // 客户端连接端点
    @GetMapping("/longConnect")
    public SseEmitter longConnect() {
        // 超时时间（毫秒）
        SseEmitter emitter = new SseEmitter(60_000L);

        // 注册回调（连接完成/超时/错误时移除）
        emitter.onCompletion(() -> emitters.remove(emitter));
        emitter.onTimeout(() -> emitters.remove(emitter));
        emitter.onError((e) -> emitters.remove(emitter));

        emitters.put(UUID.randomUUID().toString(), emitter);
        return emitter;
    }

    @PostMapping("/broadcast")
    public void broadcast(@RequestParam String message) {
        // 向所有客户端推送消息
        for (SseEmitter emitter : emitters.values()) {
            try {
                emitter.send(SseEmitter.event()
                        // 事件名称（可选）
                        .name("message")
                        // 数据内容
                        .data(message));
            } catch (IOException e) {
                emitter.completeWithError(e);
            }
        }
    }
}
```

### 客户端实现

```html
<!DOCTYPE html>
<html>
<body>
    <div id="messages"></div>
    <script>
        const eventSource = new EventSource('/sse/longConnect');
        
        // 监听默认事件（无事件名）
        eventSource.onmessage = (event) => {
            document.getElementById('messages').innerHTML += event.data + '<br>';
        };
        
        // 监听自定义事件（对应 emitter.send() 中的 .name()）
        eventSource.addEventListener('message', (event) => {
            console.log('自定义事件:', event.data);
        });
        
        // 错误处理
        eventSource.onerror = (error) => {
            console.error('SSE连接错误:', error);
            eventSource.close();
        };
    </script>
</body>
</html>
```

## 高级功能

### 发送结构化数据

```
// 服务端
emitter.send(SseEmitter.event()
    .name("userUpdate")
    .data(Map.of("id", 123, "name", "张三"), MediaType.APPLICATION_JSON));

// 客户端
eventSource.addEventListener('userUpdate', (event) => {
    const data = JSON.parse(event.data);
    console.log(data.id, data.name);
});
```

### 设置重试时间（客户端断连后重试间隔）
```
emitter.send(SseEmitter.event()
    .data("消息内容")
    // 5秒后重试
    .reconnectTime(5000)); 
```

### 指定事件ID（支持断线续传）
```
emitter.send(SseEmitter.event()
    // 事件ID
    .id("event-001")  
    .data("消息内容"));
```

## 同步与异步

### 同步执行优缺点
优点

1. 简单直接 `emitter.send("即时消息");`
2. 保证顺序
   ```
   emitter.send("消息1"); // 保证先发送
   emitter.send("消息2"); // 保证后发送
   ```
3. 错误立即反馈
   ```
   try {
       emitter.send(data); // 异常立即抛出
   } catch (IOException e) {
       // 立即处理错误
   }
   ```
   
缺点:

1. 阻塞主线程
2. 性能瓶颈，存在大量客户端时，同步发送会导致线程池耗尽，从而影响其他请求的处理
3. 超时风险

### 异步执行的优缺点

优点:

1. 非阻塞，高性能
   ```java
   @GetMapping("/stream")
   public SseEmitter stream() {
       SseEmitter emitter = new SseEmitter();
   
       // 异步执行，立即返回响应
       executor.execute(() -> {
           for (int i = 0; i < 1000; i++) {
               try {
                   emitter.send("数据 " + i);
                   Thread.sleep(100); // 模拟处理延迟
               } catch (Exception e) {
                   emitter.completeWithError(e);
               }
           }
       });
       // 立即返回，不阻塞
       return emitter; 
   }
   ```
2. 更好的吞吐量
3. 超时友好，主线程快速返回，避免控制器超时

缺点:

1. 复杂度增加
2. 顺序不确定性
   ```
   // 无法保证哪个先到达客户端
   executor.execute(() -> emitter.send("消息1"));
   executor.execute(() -> emitter.send("消息2"));
   ```
3. 错误处理复杂，需要在异步上下文中处理

### 最佳实践

适合同步发送的场景

```java
// 1. 少量即时消息
@PostMapping("/notify")
public void sendNotification(@RequestParam String message) throws IOException {
    emitter.send(message); // 简单直接
}

// 2. 需要严格顺序的场景
public void sendSequentialData() throws IOException {
    emitter.send("步骤1完成");
    emitter.send("步骤2开始"); // 保证顺序
}
```


适合异步发送的场景

```java
// 1. 大量数据或耗时操作
@GetMapping("/notify")
public SseEmitter streamBigData() {
    SseEmitter emitter = new SseEmitter();
    
    executor.execute(() -> {
        try {
            List<Data> bigData = fetchLargeData(); // 耗时操作
            for (Data item : bigData) {
                emitter.send(item);
            }
            emitter.complete();
        } catch (Exception e) {
            emitter.completeWithError(e);
        }
    });
    
    return emitter;
}

// 2. 高并发场景
public void broadcastToAll(String message) {
    for (SseEmitter emitter : emitters) {
        executor.execute(() -> {
            try {
                emitter.send(message);
            } catch (IOException e) {
                // 异步移除失效的emitter
                emitters.remove(emitter);
            }
        });
    }
}
```

## 心跳
```java
 public void heartBeat() {
     String heartbeatId = "heartbeat_" + System.currentTimeMillis();
     for (Map.Entry<String, SseEmitter> entry : emitters.entrySet()) {
         SseEmitter emitter = entry.getValue();
         String key = entry.getKey();
         try {
             // 构建心跳数据
             Map<String, Object> heartbeatData = Map.of(
                     "type", "HEARTBEAT",
                     "timestamp", System.currentTimeMillis(),
                     "serverTime", new Date(),
                     "activeConnections", emitters.size(),
                     "message", "ping"
             );
             emitter.send(SseEmitter.event()
                     .name("HEARTBEAT")
                     .data(heartbeatData)
                     .id(heartbeatId)
                     .reconnectTime(5000L));
         } catch (Exception e) {
             emitter.completeWithError(e);
             emitters.remove(key);
         }
     }
 }
```
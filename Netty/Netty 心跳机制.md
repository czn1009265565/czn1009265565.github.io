# Netty 心跳机制

## IdleStateHandler

 IdleStateHandler这个类会根据你设置的超时参数的类型和值，循环去检测channelRead和write方法多久没有被调用了，如果这个时间超过了你设置的值，那么就会触发对应的事件，read触发read，write触发write，all触发all。

- 如果超时了，则会调用userEventTriggered方法，且会告诉你超时的类型
- 如果没有超时，则会循环定时检测，除非你将IdleStateHandler移除Pipeline



## 自定义IdleHandler

实现userEventTriggered()方法作为超时事件的逻辑处理

```java
@Slf4j
public class HeartBeatHandler extends ChannelInboundHandlerAdapter {

    @Override
    public void userEventTriggered(ChannelHandlerContext ctx, Object evt) throws Exception {
        // 判断evt是否是IdleStateEvent（用于触发用户事件，包含 读空闲/写空闲/读写空闲 ）
        if (evt instanceof IdleStateEvent) {
            IdleStateEvent event = (IdleStateEvent) evt; //强制类型转换
            if (event.state() == IdleState.READER_IDLE) {
                log.info("进入读空闲...");
            } else if (event.state() == IdleState.WRITER_IDLE) {
                log.info("进入写空闲...");
            } else if (event.state() == IdleState.ALL_IDLE) {
                log.info("进入读写空闲...");
                Channel channel = ctx.channel();
                channel.close();
                log.info("断开连接 channelId:{}", channel.id());
            }
        }
    }
}
```

## 添加心跳检测

```java
public class WSServerInitialzer extends ChannelInitializer<SocketChannel> {
    @Override
    protected void initChannel(SocketChannel ch) throws Exception {
        ChannelPipeline pipeline = ch.pipeline();

        // http 编解码器
        pipeline.addLast(new HttpServerCodec());
        // 大数据流的支持
        pipeline.addLast(new ChunkedWriteHandler());
        // http message 聚合
        pipeline.addLast(new HttpObjectAggregator(1024*64));

        // 增加心跳支持 start
        pipeline.addLast(new IdleStateHandler(60, 60, 300));
        pipeline.addLast(new HeartBeatHandler());

        // websocket 服务器处理的协议 指定客户端访问路由 /ws
        // 本handler处理繁重复杂任务
        // 会帮你处理握手动作
        // 对于websocket来讲，都是以frames传输的，不同的数据类型对应的frames也不同
        pipeline.addLast(new WebSocketServerProtocolHandler("/ws"));

        // 自定义handler
        pipeline.addLast(new ChatHandler());
    }
}
```
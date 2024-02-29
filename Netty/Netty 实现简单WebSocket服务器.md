# Netty 实现简单WebSocket服务器

## 依赖配置

```xml
<dependency>
    <groupId>io.netty</groupId>
    <artifactId>netty-all</artifactId>
    <version>4.1.60.Final</version>
</dependency>
```

## 初始化Server

```java
public class WSServer {
    public static void main(String[] args) throws InterruptedException {
        EventLoopGroup mainGroup = new NioEventLoopGroup();
        EventLoopGroup subGroup = new NioEventLoopGroup();

        try{
            ServerBootstrap server = new ServerBootstrap();
            server.group(mainGroup, subGroup)
                    .channel(NioServerSocketChannel.class)
                    .childHandler(new WSServerInitialzer());

            ChannelFuture channelFuture = server.bind(8080).sync();

            channelFuture.channel().closeFuture().sync();
        } finally {
            mainGroup.shutdownGracefully();
            subGroup.shutdownGracefully();
        }
    }
}
```

## 初始化通道

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

## 自定义处理类

```java
/**
 * 处理消息的handler
 * TextWebSocketFrame 在netty中用于为websocket专门处理文本的对象，frame是消息的载体
 */
public class ChatHandler extends SimpleChannelInboundHandler<TextWebSocketFrame> {
    /**
     * 用于记录和管理所有客户端的 channel
     */
    private static ChannelGroup clients =
            new DefaultChannelGroup(GlobalEventExecutor.INSTANCE);

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, TextWebSocketFrame msg) throws Exception {
        // 获取客户端传输过来的消息
        String content = msg.text();
        System.out.println("接收到的消息:".concat(content));

        for (Channel channle : clients) {
            channle.writeAndFlush(new TextWebSocketFrame(String.format("%s:%s", LocalDateTime.now(), content)));
        }
    }

    /**
     * 当客户端连接服务端之后
     * 获取客户端的channel,并放入ChannelGroup中进行管理
     *
     * @param ctx 上下文
     * @throws Exception exception
     */
    @Override
    public void handlerAdded(ChannelHandlerContext ctx) throws Exception {
        clients.add(ctx.channel());
    }

    @Override
    public void handlerRemoved(ChannelHandlerContext ctx) throws Exception {
        // 当触发 handlerRemoved channelGroup 会自动移除对应客户端channel
        // clients.remove(ctx.channel());
        System.out.println("客户端断开 channel对应长id:".concat(ctx.channel().id().asLongText()));
        System.out.println("客户端断开 channel对应短id:".concat(ctx.channel().id().asShortText()));
    }
}
```

## 前端页面

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title></title>
    </head>
    <body>
        
        <div>发送消息:</div>
        <input type="text" id="msgContent"/>
        <input type="button" value="点我发送" onclick="CHAT.chat()"/>
        
        <div>接受消息：</div>
        <div id="receiveMsg" style="background-color: gainsboro;"></div>
        
        <script type="application/javascript">
            
            window.CHAT = {
                socket: null,
                init: function() {
                    if (window.WebSocket) {
                        CHAT.socket = new WebSocket("ws://127.0.0.1:8080/ws");
                        CHAT.socket.onopen = function() {
                            console.log("连接建立成功...");
                        },
                        CHAT.socket.onclose = function() {
                            console.log("连接关闭...");
                        },
                        CHAT.socket.onerror = function() {
                            console.log("发生错误...");
                        },
                        CHAT.socket.onmessage = function(e) {
                            console.log("接受到消息：" + e.data);
                            var receiveMsg = document.getElementById("receiveMsg");
                            var html = receiveMsg.innerHTML;
                            receiveMsg.innerHTML = html + "<br/>" + e.data;
                        }
                    } else {
                        alert("浏览器不支持websocket协议...");
                    }
                },
                chat: function() {
                    var msg = document.getElementById("msgContent");
                    CHAT.socket.send(msg.value);
                }
            };
            
            CHAT.init();
            
        </script>
    </body>
</html>

```
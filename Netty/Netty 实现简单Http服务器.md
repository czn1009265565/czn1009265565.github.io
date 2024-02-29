# Netty 实现简单Http服务器

创建启动器步骤：

1. 初始化NioEventLoopGroup线程组。bossGroup 用于监听客户端连接，专门负责与客户端创建连接，并把连接注册到workerGroup的Selector中。 workerGroup用于处理每一个连接发生的读写事件。
2. 设置通道类型 channel
3. 设置option参数
4. 自定义handler处理类
5. 端口绑定
6. 启动
7. 等待通道关闭
8. 优雅关闭 NioEventLoopGroup


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
public class HelloServer {

    public static void main(String[] args) throws InterruptedException {
        // 接收服务端的请求，但是不做任何处理
        NioEventLoopGroup bossGroup = new NioEventLoopGroup();
        // 真正处理业务逻辑
        NioEventLoopGroup workerGroup = new NioEventLoopGroup();

        try {
            ServerBootstrap bootstrap = new ServerBootstrap();
            bootstrap.group(bossGroup, workerGroup)         // 主从线程组
                    .channel(NioServerSocketChannel.class)  // NIO双向通道
                    .childHandler(new HelloInitializer())   // 子处理器
            ;
            // 启动server 绑定端口号 以同步方式启动
            ChannelFuture channelFuture = bootstrap.bind(8080).sync();
            // 监听关闭的channel,设置为同步方式
            channelFuture.channel().closeFuture().sync();
        }finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }
}
```

## 初始化通道

```java
public class HelloInitializer extends ChannelInitializer<SocketChannel> {

    protected void initChannel(SocketChannel ch) throws Exception {
        // 通过SocketChannel去获得对应的管道
        ChannelPipeline pipeline = ch.pipeline();

        pipeline.addLast("HttpServerCodec", new HttpServerCodec());

        // 添加自定义的助手类
        pipeline.addLast("customHandler", new CustomHandler());
    }
}
```

## 自定义处理类

```java
public class CustomHandler extends SimpleChannelInboundHandler<HttpObject> {

    protected void channelRead0(ChannelHandlerContext ctx, HttpObject msg) throws Exception {
        // 获取channel
        Channel channel = ctx.channel();

        // 显示客户端远程地址
        if (msg instanceof HttpRequest) {
            System.out.println(channel.remoteAddress());
        }

        // 定义发送的数据消息
        ByteBuf content = Unpooled.copiedBuffer("hello netty", CharsetUtil.UTF_8);

        // 构建一个 http response
        FullHttpResponse response = new DefaultFullHttpResponse(
                HttpVersion.HTTP_1_1,
                HttpResponseStatus.OK,
                content);
        response.headers().set(HttpHeaderNames.CONTENT_TYPE, "text/plain");
        response.headers().set(HttpHeaderNames.CONTENT_LENGTH, content.readableBytes());

        // 响应刷到客户端
        ctx.writeAndFlush(response);
    }
}
```
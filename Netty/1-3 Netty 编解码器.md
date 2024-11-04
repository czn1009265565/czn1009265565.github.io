# Netty 编解码器

## 简介
网络应用中的数据传输，需要将原始字节数据转换成对应的自定义消息对象。
服务器编码数据后发送到客户端，客户端接收字节数据后解码还原成服务端发送的消息对象。

- 解码器：负责将消息从字节或其他序列形式转成指定的消息对象
- 编码器：将消息对象转成字节或其他序列形式在网络上传输

Netty 的编解码器实现了 ChannelHandlerAdapter，可以将多个编解码器链接在一起，以实现复杂的转换逻辑

## 解码器Decoder

解码器负责 解码“入站”数据从一种格式到另一种格式，解码器处理入站数据是抽象类 `ChannelInboundHandler` 的实现。
需要将解码器放在 `ChannelPipeline` 中。对于解码器，Netty中主要提供了抽象基类 `ByteToMessageDecoder` 和 `MessageToMessageDecoder`。

### ByteToMessageDecoder
ByteToMessageDecoder是Netty中处理字节到消息解码的基类。

**实现原理:**  
当有新数据到达时，Netty会将这些数据缓存到一个内部缓冲区（ByteBuf）中。
ByteToMessageDecoder会检查这个缓冲区，
若缓冲区中的数据不足以进行解码，ByteToMessageDecoder会保留这些数据，并等待更多的数据到达。
若缓冲区中的数据足够进行解码，则调用decode方法进行解码。

### MessageToMessageDecoder
MessageToMessageDecoder主要用于处理基于消息的解码。
与直接处理字节流的解码器不同，MessageToMessageDecoder工作在一个更高的抽象层次上，
它接收Netty中的ByteBuf或其他类型的消息对象，并将它们解码为另一种形式的消息对象。

**实现原理:**  
当有新数据到达时，Netty会将这些数据封装成消息对象（如ByteBuf），并调用MessageToMessageDecoder的channelRead方法。
channelRead方法内部会将接收到的消息转换为List，并调用decode方法进行解码。
解码过程中，子类实现的decode方法会根据具体的协议逻辑将接收到的消息解码为另一种类型的消息，并将解码后的消息添加到传入的List<Object>中。
解码完成后，解码后的消息会被传递给下一个ChannelInboundHandler处理。


## 编码器Encoder
与 `ByteToMessageDecoder` 和 `MessageToMessageDecoder` 相对应，
Netty提供了对应的编码器实现 `MessageToByteEncoder` 和 `MessageToMessageEncoder`，二者都实现了 `ChannelOutboundHandler` 接口。

### MessageToByteEncoder
MessageToByteEncoder是Netty中用于将消息对象编码为字节流的编码器基类。

**实现原理:**  
当有消息需要发送时，Netty会调用MessageToByteEncoder的write方法，write方法内部调用子类实现的encode方法。
encode方法会接收一个ChannelHandlerContext参数、一个要编码的消息对象以及一个ByteBuf参数，用于存放编码后的字节流。
开发者需要在encode方法中实现将消息对象编码到ByteBuf中的逻辑。


### MessageToMessageEncoder
将消息对象编码为另一种形式的消息。

**实现原理:**  
当有消息需要发送时，Netty会调用MessageToMessageEncoder的write方法，
write方法内部会首先检查消息类型，消息类型一致则调用子类实现的encode方法进行编码。
encode方法会根据具体的协议逻辑将业务消息对象编码为另一种形式的消息，并将编码后的消息添加到传入的List<Object>中。
编码完成后，编码后的消息会被逐个写入到网络中。
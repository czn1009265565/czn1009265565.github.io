# WireShark

Wireshark 是一款开源的网络协议分析工具(前身为 Ethereal)，用于捕获、解析和展示网络数据包的详细信息

## 安装
从 `wireshark.org` 下载安装包，安装时勾选 `Npcap/WinPcap` 驱动


## 过滤器

1. 捕获过滤器(Capture Filters)  
   - 在开始捕获前设置，仅捕获符合条件的数据包，减少内存和磁盘占用
   - 位置：主界面 → 捕获选项 → “捕获过滤器”输入框
2. 显示过滤器(Display Filters)  
   - 在已捕获的数据包中动态筛选，不影响原始数据
   - 位置：主界面顶部“应用显示过滤器”输入框

### 捕获过滤器

#### 1. 基础结构

```
<协议> <方向> <主机/端口> <逻辑运算符> <条件>
```

- 协议：tcp、udp、icmp、arp等(若省略则默认为ip或ether)
- 方向：src(源)、dst(目标)、src or dst(双向)
- 主机/端口：IP 地址(如host 192.168.1.1)或端口(如port 80)
- 逻辑运算符：and(与)、or(或)、not(非)

#### 2. 常用示例

- 捕获特定 IP 的流量	`host 192.168.1.100`
- 捕获源 IP 为 10.0.0.1 的流量	`src host 10.0.0.1`
- 捕获 HTTP 流量(端口 80)	`tcp port 80`
- 捕获 DNS 查询(端口 53)	`udp port 53`
- 排除 ARP 和广播流量	`not arp and not broadcast`
- 捕获特定网段	`net 192.168.0.0/24`
- 捕获多个端口	`tcp port 80 or tcp port 443`

获取特定客户端端口 `netstat -ano | findstr <客户端PID>`

### 显示过滤器

#### 1. 基本结构

```
协议.字段 运算符 值
```

- 协议/字段：如tcp.port、ip.src、http.request.method

- 运算符
  1. ==(等于)、!=(不等于)
  2. >、<(大小比较)
  3. contains(包含) `http.host contains "google"`
  4. matches(正则匹配) `http.request.uri matches ".*\.jpg"`

#### 2. 常用示例

- 过滤 HTTP GET 请求	`http.request.method == "GET"`
- 过滤源 IP 和端口	`ip.src == 192.168.1.1 and tcp.port == 8080`
- 过滤 DNS 响应	`dns.flags.response == 1`
- 过滤特定协议	`tcp 或 udp 或 icmp`
- 过滤错误包	`tcp.analysis.retransmission`
- 过滤 HTTPS 流量	`tcp.port == 443`
- 过滤 MAC 地址	`eth.src == 00:11:22:33:44:55`
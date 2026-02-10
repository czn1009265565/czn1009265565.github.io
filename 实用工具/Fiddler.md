# Fiddler

## Fiddler app抓包

### 核心原理
1. 正常流程: App -> 互联网目标服务器。通信是端到端加密的
2. Fiddler 介入后: App -> Fiddler（代理）-> 互联网目标服务器
   - App 认为 Fiddler 是目标服务器，并与 Fiddler 建立 SSL 连接
   - Fiddler 再以客户端的身份，与真正的目标服务器建立另一个 SSL 连接
   - Fiddler 解密从 App 收到的流量，进行记录和分析，然后重新加密发送给服务器，反之亦然

这个过程被称为 MITM。为了实现它，Fiddler 必须生成自己的根证书，并让设备和 App 信任这个证书

### 详细抓包流程

#### 1. Fiddler 本机配置

1. 安装与启动
   - 从 Telerik 官网下载并安装 Fiddler Classic
   - 以管理员身份运行 Fiddler（重要！否则可能无法正确捕获所有流量或安装证书）
2. 配置 HTTPS 解密
   - 进入菜单栏: Tools > Options > HTTPS 选项卡
   - ✅ 勾选 Decrypt HTTPS traffic。这是最核心的选项
   -  在下拉菜单中，选择 ...from all processes（从所有进程）以捕获包括系统进程在内的所有流量。如果只抓浏览器，可选另一个
   - 首次勾选时，会弹出对话框，询问是否信任 Fiddler 的根证书。点击 “Yes” 或 “OK”。这会将 Fiddler 的根证书安装到计算机的“受信任的根证书颁发机构”存储区。如果此步骤失败，请右键 Fiddler 图标，选择“以管理员身份运行”
   - ✅ 勾选 Ignore server certificate errors（忽略服务器证书错误）。这有助于应对一些证书不匹配的情况
3. 配置连接设置
   - 切换到 Connections 选项卡
   - 确保 Fiddler Classic listents on port 设置为 8888（默认值）。你可以更改它，但记住端口号，后续设备配置要用
   - ✅ 勾选 Allow remote computers to connect（允许远程计算机连接）。这是让手机能连上 Fiddler 的关键
   - 点击 “OK” 保存设置。Fiddler 会提示需要重启，点击 “Yes” 重启 Fiddler
4. 获取本机 IP 地址
   - 在 Windows 命令行中输入 ipconfig

#### 2. 移动设备配置
1. 网络连接
   - 确保手机和运行 Fiddler 的电脑连接到同一个局域网（同一个 Wi-Fi）
2. 配置代理
   - iOS: 设置 > 无线局域网 > 点击当前连接的 Wi-Fi 右边的 (i) 图标 > 滚动到最底部“配置代理” > 手动
   - Android: 设置 > 网络和互联网 > WLAN > 长按当前连接的 Wi-Fi > 修改网络 > 高级选项 > 代理 > 手动
   - 服务器: 填写步骤一第4点中获取的电脑 IP 地址
   - 端口: 填写 Fiddler 的监听端口，默认为 8888
   - 保存
3. 安装 Fiddler 证书
   - 打开手机上的浏览器（Safari/Chrome）
   - 在地址栏输入 http://<你的电脑IP>:8888，例如 http://192.168.1.10:8888
   - 你会看到一个 Fiddler 的欢迎页面。点击页面上的 FiddlerRoot certificate 链接下载证书
   - iOS 特别说明（关键且复杂）
     1. 下载后，进入 设置 > 已下载的描述文件，安装 Fiddler 证书
     2. 这还没完！你必须手动信任该根证书: 设置 > 通用 > 关于本机 > 证书信任设置
     3. 找到刚刚安装的 “DO_NOT_TRUST_FiddlerRoot” 证书，开启对其的完全信任。没有这一步，iOS 10+ 系统上抓取 HTTPS 流量会失败
   - Android 特别说明: 
     1. 下载后，系统会引导你安装证书。你可能需要为证书命名
     2. Android 7.0 (Nougat) 及更高版本: 系统默认不再信任用户安装的证书（出于安全原因）。你需要将证书移动到系统证书存储区，这通常需要 Root 权限。对于非 Root 设备，一个变通方法是修改 App 的 android:networkSecurityConfig（如果你能控制该 App），或者使用像 VirtualXposed 这样的沙盒环境

#### 3. 开始抓包与分析

1. 清空会话列表: 在 Fiddler 中，按下 Ctrl + X 清空当前所有会话，方便观察新流量
2. 操作 App: 在手机上打开你想要抓包的目标 App，进行各种操作（登录、刷新、点击等）
3. 观察 Fiddler: 你会看到 HTTP 和 HTTPS 请求源源不断地出现在 Fiddler 的会话列表中
   - #: 请求序号
   - Protocol: 协议（HTTP/HTTPS）
   - Host: 请求的域名
   - URL: 请求的具体路径
   - Body: 响应大小
   - Caching: 缓存相关信息
   - Content-Type: 响应内容类型
   - Process: 发出请求的进程（对 PC 端有用，对手机端通常显示为 Tunnel to）
4. 分析会话: 点击任意一个会话，右侧会显示详细标签页
   - Inspectors: 最常用的标签。上半部分是请求详情，下半部分是响应详情。你可以查看 Raw（原始数据）、Headers（头信息）、JSON/XML/HexView（格式化的内容）等
   - Statistics: 统计信息，显示请求耗时、字节数等
   - AutoResponder: 自动响应器，可用于模拟服务器返回数据，进行前端调试

#### 4. 收尾工作

抓包完成后，记得在手机 Wi-Fi 设置中将代理改回“无”或“自动”，否则手机在离开此 Wi-Fi 后将无法上网

### 常见问题及解决

#### 问题 1: Fiddler 会话列表为空，抓不到任何包

1. 代理未设置或设置错误:  double-check 手机的代理 IP 和端口是否正确。确保电脑防火墙没有阻止 Fiddler（可暂时关闭防火墙测试）
2. 电脑和手机不在同一网络: 确保它们连接的是同一个路由器发出的 Wi-Fi
3. Fiddler 未允许远程连接: 检查 Connections 设置中 Allow remote computers to connect 是否勾选
4. App 使用了非代理网络: 某些 App（特别是金融、游戏类）会检测并主动绕过系统代理。它们可能使用原生代码（如 OkHttp 的 Proxy.NO_PROXY）或直接使用底层 Socket。解决方案: 使用更底层的抓包工具，如 Wireshark（但无法解密 HTTPS），或使用 VPN 模式 的抓包方案，如 Charles Proxy 的 VPN 功能、Packet Capture（手机端 App）或 HttpCanary（安卓端，需安装其证书）
5. 流量不是 HTTP/HTTPS: Fiddler 只能抓应用层协议。如果是 TCP/UDP 等传输层协议，需要使用 Wireshark

#### 问题 2: HTTPS 请求显示为 “Tunnel to ... 443” 且无法解密

- 现象: 会话列表中只看到一条 CONNECT 请求，状态为 200，后面跟着一堆 Tunnel to 的会话，点开看不到请求和响应内容。
- 原因: 这表示 SSL 隧道已建立，但 Fiddler 未能成功解密。根本原因是客户端（手机或 App）不信任 Fiddler 的证书。
- 解决方案: 
  1. 证书未正确安装/信任（最常见）: 
     - iOS:  确保已完成 设置 > 通用 > 关于本机 > 证书信任设置 中的完全信任步骤。
     - Android:  对于 Android 7.0+，如果 App 的 targetSdkVersion >= 24，则默认只信任系统证书。解决方案包括: a) Root 手机并将 Fiddler 证书移动到系统证书目录；b) 修改 App 的源码或重打包；c) 在电脑上安装一个旧版 Android 模拟器（如 Genymotion），其系统证书管理较宽松。
  2. 重新安装证书: 在 Fiddler 的 Tools > Options > HTTPS 中点击 Actions > Export Root Certificate to Desktop，将证书文件通过数据线或邮件发送到手机，手动安装。

#### 问题 3: 遇到 SSL Pinning（证书绑定/证书锁定）

- 现象: 即使证书已正确安装和信任，抓取特定 App 的 HTTPS 流量时依然失败，或 App 直接报网络错误、闪退
- 原因: 这是一种高级安全措施。App 不仅验证证书链是否被系统信任，还会在代码层面硬编码（或从服务器获取）一个真正的服务器证书公钥或哈希值。在握手时，它会对比收到的证书和预设的值是否一致。由于 Fiddler 的证书与预设值不匹配，App 会主动终止连接
- 解决方案（按难度排序）
  1. 尝试旧版本 App: 早期版本可能未启用 SSL Pinning。从第三方应用市场下载历史版本
  2. 使用反编译和重打包工具（针对 Android）
     - 使用 apktool 反编译 APK 文件
     - 找到并修改网络安全配置文件（network_security_config.xml）或包含证书校验逻辑的 Smali 代码
     - 使用 apktool 重新打包并签名。此过程技术性较强
  3. 使用动态代码注入工具（最有效）
     - Frida: 一个动态插桩工具。你需要编写或使用现成的脚本（如 universal-android-ssl-pinning-bypass.js）来 Hook 关键的证书验证函数（如 checkServerTrusted），使其总是返回成功。这需要电脑上运行 frida-server，手机需要 ADB 调试权限，不一定需要 Root，但通常 Root 后更稳定
     - Objection: 一个基于 Frida 的运行时移动探索工具包，内置了禁用 SSL Pinning 的命令（android sslpinning disable），非常方便
     - Xposed 模块: 如 JustTrustMe、SSLUnpinning。需要在已安装 Xposed 框架的 Root 手机上使用
  4. 将 Fiddler 证书安装为系统证书（仅限已 Root 的 Android 设备）: 这可以绕过一些较弱的 Pinning 实现（只验证证书链），但无法对抗硬编码公钥的强 Pinning

#### 问题 4: Fiddler 报证书错误（如 certificate unknown， certificate has expired）

1. Fiddler 根证书过期: Fiddler 生成的根证书默认有效期为1年。解决方案: 进入 Tools > Options > HTTPS，点击 Actions > Reset All Certificates。这会删除旧证书并生成新的，你需要重新在手机和电脑上安装和信任新证书
2. 服务器使用了不常见的密码套件或协议: Fiddler 可能不支持某些极端配置。尝试更新 Fiddler 到最新版本
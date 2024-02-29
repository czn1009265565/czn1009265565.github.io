## Charles

### 安装

官网`https://www.charlesproxy.com/` 下载即可

### 设置为系统代理

1. 顶部菜单栏 -> Proxy -> Windows Proxy

2. 顶部菜单栏 -> Proxy -> Proxy Settings -> Proxies -> 勾上 Enable transparent HTTP proxying


### 代理手机网络请求
1. 保证手机和 PC 是在同一个局域网

2. 手机WIFI 设置代理 主机名、端口

### Https

#### 电脑证书配置
1. help –> SSLProxying –> Install Charles Root Certificate 将证书安装在受信任的根证书下
2. Proxy –> SSL Proxying Settings 勾选Enable SSL Proxying, 并添加`*:*`

### 手机端证书配置
1. help–>SSLProxying–> Install Charles Root Certificate on a Mobile Device or Remote Browser
2. 访问`chls.pro/ssl` 下载证书(前提设置好手机代理)

至此，手机浏览器抓包应该不成问题。后续APP抓包则涉及SSL planning,APK反编译暂时不提。


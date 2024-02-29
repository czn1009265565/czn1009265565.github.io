## Zerotier

### 背景

在没有公网IP的情况下想要组建私人局域网，实现多端互联，包括手机、日常笔记本、以及服务器。

### 使用流程

1. Zerotier官网申请账号 `https://my.zerotier.com/`
2. 注册并创建一个Basic NetWorks(免费)
3. 进入NetWorks详情页获取NetWorkId
4. 下载Zerotier客户端，包括安卓、Mac、Windows、Linux

```shell
# Centos7安装
curl -s https://install.zerotier.com | sudo bash
systemctl start zerotier-one.service
systemctl enable zerotier-one.service
zerotier-cli join 8056c2e21c2f1d6a

# 卸载
rpm -e zerotier-one
rm -rf /var/lib/zerotier-one/
```

5. 客户端连接后，在ZeroTier 管理页面，通过客户端的请求
6. 修改分配局域网IP，实现互通互联

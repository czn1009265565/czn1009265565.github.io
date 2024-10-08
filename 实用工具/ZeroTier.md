## ZeroTier

### 简介

ZeroTier是一款利用 UDP 打洞来实现内网穿透的工具，相比其他工具成功率更高、部署更简单。
其基本工作原理是组建一个虚拟局域网，各个设备（NAS、Linux、Windows、Mac、iOS、Android）安装了客户端、加入到这个虚拟局域网后，
就会自动分配一个IP，从而实现局域网内各个设备及服务的相互访问。


### 使用流程

1. ZeroTier官网申请账号 `https://my.zerotier.com/`
2. 注册并创建一个Basic NetWorks(免费)
3. 进入NetWorks详情页获取NetWorkId
4. 下载ZeroTier客户端，包括安卓、Mac、Windows、Linux  
    ```shell
    # Centos7安装
    curl -s https://install.zerotier.com | sudo bash
    # 启动服务并设置开机自启
    systemctl start zerotier-one.service
    systemctl enable zerotier-one.service
    # 卸载
    rpm -e zerotier-one
    rm -rf /var/lib/zerotier-one/
    ```
5. 加入网络  
   ```shell
   zerotier-cli join 8056c2e21c2f1d6a
   # 查看网络状态
   zerotier-cli status
   ```
6. 客户端加入后，ZeroTier的Web管理页面就能看到该网络，勾选该网络，表示同意客户端接入
7. Web管理页面修改分配局域网IP，实现互通互联

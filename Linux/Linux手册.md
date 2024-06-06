# Linux 手册

[GitHub项目地址](https://github.com/jaywcjlove/linux-command.git)

[命令检索](jaywcjlove.github.io/linux-command)


## ssh

```shell
# ssh 用户名@远程服务器地址
ssh root@172.30.255.101
# 指定端口
ssh -p 2211 root@172.30.255.101

# ssh
ssh -p 22 user@ip  # 默认用户名为当前用户名，默认端口为 22
ssh-keygen # 为当前用户生成 ssh 公钥 + 私钥
ssh-keygen -f keyfile -i -m key_format -e -m key_format # key_format: RFC4716/SSH2(default) PKCS8 PEM
ssh-copy-id user@ip # 将当前用户的公钥复制到需要 ssh 的服务器的 ~/.ssh/authorized_keys，之后可以免密登录
```

## scp

```shell
scp [参数] [原路径] [目标路径]

# 从远程复制文件到本地
scp root@172.30.255.101:/opt/soft/nginx-0.5.38.tar.gz /opt/soft/
# 从远程复制目录到本地
scp -r root@172.30.255.101:/opt/soft/mongodb /opt/soft/
scp -r -P 22 root@172.30.255.101:/opt/soft/mongodb /opt/soft/


# 上传本地文件至远程
scp /opt/soft/nginx-0.5.38.tar.gz root@10.10.10.10:/opt/soft/scptest
# 上传本地文件到远程机器指定目录
scp -r /opt/soft/mongodb root@10.10.10.10:/opt/soft/scptest
scp -r  -P 22 /opt/soft/mongodb root@10.10.10.10:/opt/soft/scptest
```


## crontab

### 命令
```shell
# 列出该用户的计时器设置
crontab -l

# 编辑该用户的计时器设置
crontab -e
```

### 语法

```
minute   hour   day   month   week   command     顺序：分 时 日 月 周
```

- minute： 表示分钟，可以是从0到59之间的任何整数。
- hour：表示小时，可以是从0到23之间的任何整数。
- day：表示日期，可以是从1到31之间的任何整数。
- month：表示月份，可以是从1到12之间的任何整数。
- week：表示星期几，可以是从0到7之间的任何整数，这里的0或7代表星期日。
- command：要执行的命令，可以是系统命令，也可以是自己编写的脚本文件。

### 示例

|执行时间|格式|
|---|---|
|每分钟定时执行一次	|* * * * *|
|每小时定时执行一次	|0 * * * *|
|每天定时执行一次	|0 0 * * *|
|每周定时执行一次	|0 0 * * 0|
|每月定时执行一次	|0 0 1 * *|
|每月最后一天定时执行一次	|0 0 L * *|
|每年定时执行一次	|0 0 1 1 *|

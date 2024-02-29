# Aria2
Aria2 是目前最强大的全能型下载工具，它支持 BT、磁力、HTTP、FTP 等下载协议，常用做离线下载的服务端

### Docker Compose模板
```yaml
version: "3.8"

services:

  Aria2-Pro:
    container_name: aria2-pro
    image: p3terx/aria2-pro
    environment:
      - PUID=65534
      - PGID=65534
      - UMASK_SET=022
      - RPC_SECRET=P3TERX
      - RPC_PORT=6800
      - LISTEN_PORT=6888
      - DISK_CACHE=64M
      - IPV6_MODE=false
      - UPDATE_TRACKERS=true
      - CUSTOM_TRACKER_URL=
      - TZ=Asia/Shanghai
    volumes:
      - ${PWD}/aria2-config:/config
      - ${PWD}/aria2-downloads:/downloads
# If you use host network mode, then no port mapping is required.
# This is the easiest way to use IPv6 networks.
    network_mode: host
#    network_mode: bridge
#    ports:
#      - 6800:6800
#      - 6888:6888
#      - 6888:6888/udp
    restart: unless-stopped
# Since Aria2 will continue to generate logs, limit the log size to 1M to prevent your hard disk from running out of space.
    logging:
      driver: json-file
      options:
        max-size: 1m

# AriaNg is just a static web page, usually you only need to deploy on a single host.
  AriaNg:
    container_name: ariang
    image: p3terx/ariang
    command: --port 6880 --ipv6
    network_mode: host
#    network_mode: bridge
#    ports:
#      - 6880:6880
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: 1m
```

1. 启动容器 `docker-compose up -d`
2. 访问`http://localhost:6880` AriaNg设置>Aria2 RPC密钥 完成RPC密钥配置


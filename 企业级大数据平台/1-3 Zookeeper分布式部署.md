# Zookeeper分布式部署

### 解压安装
```shell
tar -zxvf apache-zookeeper-3.7.1-bin.tar.gz -C /opt/module/

mv /opt/module/apache-zookeeper-3.7.1-bin/ /opt/module/zookeeper
```

### 配置服务器编号
1. 在`/opt/module/zookeeper/`目录下创建zkData `mkdir zkData`
2. 在`/opt/module/zookeeper/zkData`目录下创建一个myid的文件 `vim myid`
3. 在文件中添加与server对应的编号 `1`


### 配置zoo.cfg文件
1. 重命名`/opt/module/zookeeper/conf`目录下的zoo_sample.cfg为zoo.cfg
   ```shell
   mv zoo_sample.cfg zoo.cfg
   ```
2. 打开zoo.cfg文件 `vim zoo.cfg`
   ```shell
   # 修改数据存储路径配置
   dataDir=/opt/module/zookeeper/zkData
   # 加如下配置
   #######################cluster##########################
   server.1=hadoop101:2888:3888
   server.2=hadoop102:2888:3888
   server.3=hadoop103:2888:3888
   ```
3. 同步/opt/module/zookeeper目录内容到hadoop102、hadoop103
   ```shell
   scp -r /opt/module/zookeeper hadoop@hadoop102:/opt/module/zookeeper
   scp -r /opt/module/zookeeper hadoop@hadoop103:/opt/module/zookeeper
   ```
4. 分别修改hadoop102、hadoop103上的myid文件中内容为2、3
5. zoo.cfg配置参数解读 `server.A=B:C:D`

   - A是一个数字，表示这个是第几号服务器。集群模式下配置一个文件myid，这个文件在dataDir目录下，这个文件里面有一个数据就是A的值，Zookeeper启动时读取此文件，拿到里面的数据与zoo.cfg里面的配置信息比较从而判断到底是哪个server。
   - B是这个服务器的地址； 
   - C是这个服务器Follower与集群中的Leader服务器交换信息的端口；
   - D是万一集群中的Leader服务器挂了，需要一个端口来重新进行选举，选出一个新的Leader，而这个端口就是用来执行选举时服务器相互通信的端口。

### 启动集群

```shell
# hadoop101
bin/zkServer.sh start
# hadoop102
bin/zkServer.sh start
# hadoop103
bin/zkServer.sh start
```
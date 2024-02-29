## Zookeeper 集群搭建

为保证集群高可用，Zookeeper 集群的节点数最好是奇数，最少有三个节点，所以这里搭建一个三个节点的集群。

本文介绍 zookeeper 3.4.14 集群搭建

1. 修改hosts文件
	```
	10.192.77.203 zookeeper001
	10.192.77.203 zookeeper002
	10.192.77.203 zookeeper003
	```

1. 解压
	
	```
	$ tar -zxvf zookeeper-3.4.14.tar.gz

	$ cp -r zookeeper-3.4.14 /usr/local/zookeeper001
	$ cp -r zookeeper-3.4.14 /usr/local/zookeeper002
	$ cp -r zookeeper-3.4.14 /usr/local/zookeeper003
	```

2. 配置文件修改,拷贝配置样本 zoo_sample.cfg 为 zoo.cfg 并进行修改

	1. zookeeper001配置
		```
		tickTime=2000
		initLimit=10
		syncLimit=5
		dataDir=/usr/local/zookeeper-cluster/data/01
		dataLogDir=/usr/local/zookeeper-cluster/log/01
		clientPort=2181

		# server.1 这个1是服务器的标识，可以是任意有效数字，标识这是第几个服务器节点，这个标识要写到dataDir目录下面myid文件里
		# 指名集群间通讯端口和选举端口
		server.1=zookeeper001:2287:3387
		server.2=zookeeper002:2288:3388
		server.3=zookeeper003:2289:3389
		```
	2. zookeeper002配置
		```
		tickTime=2000
		initLimit=10
		syncLimit=5
		dataDir=/usr/local/zookeeper-cluster/data/02
		dataLogDir=/usr/local/zookeeper-cluster/log/02
		clientPort=2182

		server.1=zookeeper001:2287:3387
		server.2=zookeeper002:2288:3388
		server.3=zookeeper003:2289:3389
		```
	3. zookeeper003配置
		```
		tickTime=2000
		initLimit=10
		syncLimit=5
		dataDir=/usr/local/zookeeper-cluster/data/03
		dataLogDir=/usr/local/zookeeper-cluster/log/03
		clientPort=2183

		server.1=zookeeper001:2287:3387
		server.2=zookeeper002:2288:3388
		server.3=zookeeper003:2289:3389
		```
	如果是多台服务器，则集群中每个节点通讯端口和选举端口可相同，IP 地址修改为每个节点所在主机 IP 即可。
3. 创建存储目录
	```
	# dataDir
	mkdir -vp  /usr/local/zookeeper-cluster/data/01
	# dataDir
	mkdir -vp  /usr/local/zookeeper-cluster/data/02
	# dataDir
	mkdir -vp  /usr/local/zookeeper-cluster/data/03
	```
4. 写入节点标识到 myid 文件
	```
	#server1
	echo "1" > /usr/local/zookeeper-cluster/data/01/myid
	#server2
	echo "2" > /usr/local/zookeeper-cluster/data/02/myid
	#server3
	echo "3" > /usr/local/zookeeper-cluster/data/03/myid
	```
5. 启动集群
	```
	# 启动节点1
	/usr/local/zookeeper001/bin/zkServer.sh start
	# 启动节点2
	/usr/local/zookeeper002/bin/zkServer.sh start
	# 启动节点3
	/usr/local/zookeeper003/bin/zkServer.sh start
	```
6. 查看状态
	```
	$ jps
	3907 QuorumPeerMain
	3987 QuorumPeerMain
	3945 QuorumPeerMain


	$ /usr/local/zookeeper001/bin/zkServer.sh status
	$ /usr/local/zookeeper002/bin/zkServer.sh status
	$ /usr/local/zookeeper003/bin/zkServer.sh status
	```
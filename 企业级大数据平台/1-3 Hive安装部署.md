# Hive安装部署

## 解压安装

```shell
tar -zxvf hive-3.1.3.tar.gz -C /opt/module/
mv /opt/module/apache-hive-3.1.3-bin/ /opt/module/hive
```

**添加环境变量**  

```shell
sudo vim /etc/profile.d/hadoop_env.sh

#HIVE_HOME
export HIVE_HOME=/opt/module/hive
export PATH=$PATH:$HIVE_HOME/bin


source /etc/profile.d/hadoop_env.sh
```

## 元数据配置

1. 添加MySQL驱动
   ```shell
   cp mysql-connector-j-8.0.31.jar /opt/module/hive/lib/
   ```
2. 在`$HIVE_HOME/conf`目录下新建 `hive-site.xml`文件
   ```xml
   <?xml version="1.0"?>
   <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
   <configuration>
       <!--配置Hive保存元数据信息所需的 MySQL URL地址-->
       <property>
           <name>javax.jdo.option.ConnectionURL</name>
           <value>jdbc:mysql://localhost:3306/hive?serverTimezone=Asia/Shanghai</value>
       </property>
   
       <!--配置Hive连接MySQL的驱动全类名-->
       <property>
           <name>javax.jdo.option.ConnectionDriverName</name>
           <value>com.mysql.cj.jdbc.Driver</value>
       </property>
   
       <!--配置Hive连接MySQL的用户名 -->
       <property>
           <name>javax.jdo.option.ConnectionUserName</name>
           <value>root</value>
       </property>
   
       <!--配置Hive连接MySQL的密码 -->
       <property>
           <name>javax.jdo.option.ConnectionPassword</name>
           <value>password</value>
       </property>
   
       <property>
           <name>hive.metastore.warehouse.dir</name>
           <value>/user/hive/warehouse</value>
       </property>
   
       <property>
           <name>hive.metastore.schema.verification</name>
           <value>false</value>
       </property>
   
       <property>
           <name>hive.server2.thrift.port</name>
           <value>10000</value>
       </property>
   
       <property>
           <name>hive.server2.thrift.bind.host</name>
           <value>hadoop101</value>
       </property>
   
       <property>
           <name>hive.metastore.event.db.notification.api.auth</name>
           <value>false</value>
       </property>
       
       <property>
           <name>hive.cli.print.header</name>
           <value>true</value>
       </property>
   
       <property>
           <name>hive.cli.print.current.db</name>
           <value>true</value>
       </property>
   </configuration>
   ```
3. 创建数据库
   ```shell
   mysql> CREATE DATABASE hive CHARACTER SET utf8 COLLATE utf8_general_ci;
   ```
4. 初始化Hive元数据库
   ```shell
   schematool -initSchema -dbType mysql -verbose
   ```
5. 启动Hive
   ```shell
   hive
   ```


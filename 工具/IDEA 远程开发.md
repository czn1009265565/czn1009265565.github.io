# IDEA 远程开发

## 远程部署

远程部署的思路是在本地编写代码，然后把本地的代码文件定期同步到 `Linux` 服务器，再用本地电脑操作远程服务器完成部署和运行。

### 文件同步

1. 菜单路径: Tools => Development => Configuration
2. 新增SFTP连接，输入Server Name(推荐以服务器IP命名)
3. 配置SSH连接，输入IP，端口，用户名及密码，点击Test Connection进行验证
4. 配置路径映射，点击Mappings，填写本地及远程服务器路径映射  
   - Local Path 本地代码文件路径，例如 `D:\github\spring-boot-examples`
   - Deployment Path 远程服务器文件路径，例如 `/home/app/spring-boot-examples`
5. 点击OK，完成保存

### 查看远程文件列表

菜单路径: Tools => Development => Browse Remote Host

### 开启自动同步

菜单路径: Tools => Development => Automatic Upload

### 同步删除文件
到目前为止，如果我们删除了本地电脑的文件，远程 Linux 服务器的对应文件并不会删除

1. 菜单路径: Tools => Development => Options
2. 勾选 `Delete target items when source ones do not exist` (手动同步)
3. 勾选 `Delete remote files when local are deleted`

### 手动同步

右键左侧文件或目录，选择 `Deployment => Upload to <Server Name>`

### 远程终端


### 远程调试



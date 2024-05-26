# Windows WSL

## 前置条件
1. Windows10
2. 对于 x64 系统：版本 1903 或更高版本，内部版本为 18362.1049 或更高版本
3. 对于 ARM64 系统：版本 2004 或更高版本，内部版本为 19041 或更高版本。


## WSL安装部署

1. 启用适用于 Linux 的 Windows 子系统
    ```shell
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    ```
2. 启用虚拟机功能
    ```shell
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    ```
3. 重新启动计算机，以完成配置更新
4. [下载 Linux 内核更新](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi),并运行更新包
5. 将 WSL 2 设置为默认版本
    ```shell
    wsl --set-default-version 2
    ```
6. 更新WSL `wsl --update`
7. 重启WSL实例 `wsl --shutdown`
   
## Ubuntu 安装部署

1. 打开 `Microsoft Store`，安装 `Ubuntu 22.04`
2. 首次启动 `Ubuntu 22.04` 需要创建用户账户和密码
3. 安装图形界面
   ```shell
   sudo apt update
   sudo apt install ubuntu-desktop
   ```
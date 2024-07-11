# VMware ESXI 6.7安装部署

## 前置准备

### 封装网卡驱动
由于VMware ESXI 仅支持英特尔网卡，因此需要封装网卡驱动(本机网卡RTL8111/8168/8411)

1. 下载对应网卡驱动vib文件 `https://vibsdepot.v-front.de/wiki/index.php/Net55-r8168`
2. VMware-PowerCLI-12.7.0 `https://developer.broadcom.com/tools/vmware-powercli/12.7.0`
3. ESXi-Customizer-PS-2.9.0 `https://github.com/VFrontDe-Org/ESXi-Customizer-PS`
4. ESXi670-202210001.zip `https://support.broadcom.com/` 需要先注册登陆账号

制作镜像:  
1. 首先，将下载的 `VMware-PowerCLI-12.7.0` 压缩包内文件解压至 `C:\Program Files\WindowsPowerShell\Modules`
2. 以D盘为例，创建 `D:\esxi\vib` 将 `ESXi670-202210001.zip` 离线包、`ESXi-Customizer-PS.ps1` 放入`D:\esxi`，`net55-r8168-8.045a-napi.x86_64.vib` 驱动文件放入 `D:\esxi\vib`
3. 管理员运行powershell
    ```shell
    Set-ExecutionPolicy RemoteSigned
    Import-Module VMware.PowerCLI
    Set-PowerCLIConfiguration -Scope AllUsers -ParticipateInCeip $false -InvalidCertificateAction Ignore
    ```
4. CMD执行
    ```shell
    .\ESXi-Customizer-PS.ps1 -ozip .\ESXi670-202210001.zip -pkgDir .\vib
    .\ESXi-Customizer-PS.ps1 -izip .\ESXi-6.7.0-20221004001-standard-customized.zip
    ```
5. 成功生成 `ESXi-6.7.0-20221004001-standard-customized.iso`

## UltraISO录盘


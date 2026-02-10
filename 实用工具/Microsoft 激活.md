# Microsoft激活

## Office安装

1. 访问Microsoft官网，下载官方部署工具Office Deployment Tool
微软官方地址：`https://www.microsoft.com/en-us/download/details.aspx?id=49117`
2. 运行 Office Depolyment Tool
3. 通过Microsoft Office 自定义工具制作配置文件 
   
    微软官方地址:`https://config.office.com/deploymentsettings`

    配置项介绍
    - 体系结构: 64位
    - Office套件: Office标准版2019
    - Visio: Visio标准版2019
    - Project: Project标准版2019
    - 语言简体中文

4. 将导出的config 文件存放到 office 文件中
5. 打开命令提示符以管理员身份运行，输入命令，下载安装office

```shell
cd D:\program\office
setup.exe /download config.xml
setup.exe /configure config.xml
```


## 激活

开源工具: `https://github.com/massgravel/Microsoft-Activation-Scripts/`

CMD根据命令行选项选择需要激活的Windows以及Office即可。


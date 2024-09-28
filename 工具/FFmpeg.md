# FFmpeg

## 安装

```shell
yum install -y epel-release libicu
yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
yum install -y ffmpeg ffmpeg-devel
ffmpeg -version
```
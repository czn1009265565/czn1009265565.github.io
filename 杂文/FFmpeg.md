# FFmpeg

## 安装

```shell
yum install -y epel-release libicu
yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
yum install -y ffmpeg ffmpeg-devel
ffmpeg -version
```

## 命令

### 合并ts

```python
def merge_ts(shard_num):
    with open("files.txt", "w") as f:
        for i in range(shard_num):
            f.write("file " + "%04d" % i + ".ts" + "\n")
```

```shell
ffmpeg -f concat -safe 0 -i files.txt -c copy out.mp4
```

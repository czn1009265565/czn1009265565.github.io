## Python 环境搭建
本文介绍Centos7 搭建Python3.6.8环境

### 依赖安装
```shell
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel gcc
```

### 下载源码包
浏览器打开 https://www.python.org/ftp/python/ 查看最新的Python版本，标记为3.6.8

```shell
wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
```

### 创建目录

```shell
mkdir /usr/local/python3
```

### 解压下载文件并切换目录

```shell
tar -zxvf Python-3.6.8.tgz
cd Python-3.6.8
```

### 编译

```shell
./configure --prefix=/usr/local/python3
make && make install
```

### 添加环境变量

```shell
vim /etc/profile

export PYTHON_HOME=/usr/local/python3/bin
export PATH=$PATH:$PYTHON_HOME

source /etc/profile
```

### 命令测试

```shell
python3
pip3 list
```

### 扩展包

```shell
# 安装扩展包
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy pandas matplotlib jupyter
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 输出扩展包依赖
pip freeze > requirements.txt
```
扩展包与Python版本兼容情况可以访问 `https://pypi.org/` 扩展包详情页 `Download files`查看

### C++依赖
问题: pip安装扩展包失败，提示缺少 `C++` 依赖。

解决: 下载 `Microsoft C++` 生成工具(https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/), 勾选 `使用C++的桌面开发`,完成安装。

### 虚拟环境 virtualenv

安装扩展包
```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple virtualenv
```

创建虚拟环境
```shell
virtualenv venv
```

激活虚拟环境
```shell
# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

退出虚拟环境
```shell
deactivate
```
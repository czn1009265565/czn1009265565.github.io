# Python环境搭建

本文介绍Centos7安装部署Python环境

## Python3.6.8

### 依赖安装
```shell
yum -y update
yum -y groupinstall "Development Tools"
yum -y install openssl-devel libffi-devel bzip2-devel
```

### 下载源码包
```shell
wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
tar -zxvf Python-3.6.8.tgz
cd Python-3.6.8
```

### 编译
```shell
mkdir /usr/local/python3
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

### 命令行测试
```shell
python3 --version
pip3 list
```

## Python3.10

### 依赖安装
```shell
yum -y update
yum -y groupinstall "Development Tools"
yum -y install openssl-devel libffi-devel bzip2-devel
```

### openssl >= 1.1.1
由于python3.7后使用ssl需要高版本的openssl支持，centos7.9默认1.0.2k-fips版本已经不支持，所以需要提前额外编译安装高版本openssl

```shell
wget https://www.openssl.org/source/openssl-1.1.1q.tar.gz --no-check-certificate
tar -zxvf openssl-1.1.1q.tar.gz
cd openssl-1.1.1q
mkdir /usr/local/openssl-1.1.1
./config --prefix=/usr/local/openssl-1.1.1
sudo make && sudo make altinstall
```

### 下载源码包
```shell
wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
tar -zxvf Python-3.10.14.tgz
cd Python-3.10.14
```

### 编译
```shell
mkdir /usr/local/python3
./configure --enable-optimizations --with-openssl=/usr/local/openssl-1.1.1 --with-openssl-rpath=auto --prefix=/usr/local/python3
sudo make && sudo make install
```

### 添加环境变量
```shell
vim /etc/profile

export PYTHON_HOME=/usr/local/python3/bin
export PATH=$PATH:$PYTHON_HOME

source /etc/profile
```

### 命令行测试
```shell
python3 --version
pip3 list
```

## 更换pip源
```shell
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
pip config set install.trusted-host mirrors.aliyun.com
```

## 安装扩展包

```shell
# 升级pip
pip3 install --upgrade pip

# 安装扩展包
pip3 install numpy pandas matplotlib jupyter
pip3 install -r requirements.txt

# 输出扩展包依赖
pip3 freeze > requirements.txt
```
扩展包与Python版本兼容情况可以访问 `https://pypi.org/` 扩展包详情页 `Download files`查看

常见问题:
1. Windows环境 `pip` 安装扩展包失败，提示缺少 `C++` 依赖  
   解决: 下载 `Microsoft C++` 生成工具(https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/), 勾选 `使用C++的桌面开发`,完成安装。

## 虚拟环境 virtualenv

### 安装 `virtualenv`
```shell
pip3 install virtualenv
```

### 创建虚拟环境
```shell
virtualenv venv
```

### 激活虚拟环境
```shell
# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 退出虚拟环境
```shell
deactivate
```
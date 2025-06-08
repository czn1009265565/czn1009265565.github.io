# Miniconda
Conda 是一个开源的软件包管理系统和环境管理系统，用于安装多个版本的软件包及其依赖关系，并在它们之间轻松切换。

下载地址: https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

## 安装Miniconda

```shell
# 下载并执行安装脚本(一路yes)
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# 加载环境变量
source ~/.bashrc

# 取消默认激活base环境
conda config --set auto_activate_base false
```


**配置国内镜像**  
```shell
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --set show_channel_urls yes
```

**查看镜像**
```shell
conda config --show channels

- https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
- https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
- defaults
```

**删除镜像源**  
```shell
conda config --remove-key channels
conda config --show channels

- defaults
```

## 常用命令

```shell
# 查看虚拟环境列表
conda env list

# 创建一个新的虚拟环境
conda create --name env_name python=3.10

# 激活环境
conda activate env_name

# 退出当前虚拟环境
conda deactivate

# 删除虚拟环境
conda remove --name env_name --all

# 复制虚拟环境
conda create --name new_env_name --clone old_env_name

# 分享/备份虚拟环境
# 首先激活要分享的环境
conda env export > environment.yml
conda env create -f environment.yml
```

包管理更推荐使用原生pip

```shell
# 升级pip
pip install --upgrade pip

# 安装扩展包
pip install numpy pandas matplotlib jupyter -i https://mirrors.aliyun.com/pypi/simple
pip install -r requirements.txt

# 输出扩展包依赖
pip freeze > requirements.txt
```
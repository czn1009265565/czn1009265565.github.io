# Qwen安装部署


## 环境准备

1. 更新系统  
   ```shell
   sudo apt update && sudo apt upgrade -y
   ```
   
2. 安装 NVIDIA 驱动（如果未安装）
   ```shell
   # 添加驱动 PPA
    sudo add-apt-repository ppa:graphics-drivers/ppa -y
    sudo apt update
    
    # 自动安装推荐驱动
    ubuntu-drivers devices
    sudo ubuntu-drivers autoinstall
    # 重启后验证:
    
    nvidia-smi
    # 应能看到对应显卡版本信息
   ```

3. 安装 CUDA Toolkit（可选，提升 GPU 利用率）  
   虽然 Ollama 使用 llama.cpp 后端支持 CUDA，但需确保有兼容版本：
   ```shell
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
    sudo mv cuda-ubuntu2004.pin /etc/apt/sources.list.d/cuda.repo
    sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
    sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
    sudo apt update
    sudo apt install -y cuda-toolkit-11-7
   ```
   
## 安装 Ollama

Ollama 官方提供 Linux 原生支持:

```shell
# 下载并安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 启动服务
systemctl --user start ollama

# 设置开机自启
systemctl --user enable ollama

# 将用户加入 ollama 组（可选）
sudo usermod -aG ollama $USER
```

## 检查 GPU 是否被识别 (关键)

Ollama 默认使用 CPU 推理。要启用 GPU，需要确认其是否检测到你的 NVIDIA 显卡。

查看日志:

```shell
journalctl --user -u ollama -f
```

启动一次任意模型（例如 Llama3）触发初始化:

```shell
ollama run llama3
```
然后退出，再看日志中是否有类似:

```shell
CUDA enabled
```
若看到此信息，则 GPU 可用，否则只能靠 CPU + RAM 推理(极慢)

## 拉取并运行

步骤 1：获取一个适配的 Qwen-7B-GGUF 模型
前往 Hugging Face 搜索: `https://huggingface.co/TheBloke/Qwen-7B-GGUF`

下载最小的量化版本（推荐 qwen-7b.Q4_K_M.gguf）：

大小：约 4.5 GB
显存需求：INT4，约 6~7GB（可勉强运行于 8GB 显存）
步骤 2：创建 Modelfile（告诉 Ollama 如何加载该模型）

```shell
# Modelfile
FROM ./qwen-7b.Q4_K_M.gguf

# 可选参数设置
PARAMETER num_ctx 4096    # 上下文长度
PARAMETER num_gpu 1       # 使用 GPU 层卸载（关键！）
PARAMETER num_thread 8    # 线程数
保存为 Modelfile（注意首字母大写无扩展名）
```

步骤 3：构建模型
```shell
# 将 .gguf 文件放在当前目录
mv qwen-7b.Q4_K_M.gguf ./model.gguf

# 创建 Modelfile 内容
cat > Modelfile << EOF
FROM ./model.gguf
PARAMETER num_gpu 1
PARAMETER num_ctx 4096
EOF

# 构建模型
ollama create qwen-7b-int4 -f Modelfile
```

步骤 4：运行模型
```shell
ollama run qwen-7b-int4
```
你应该能看到交互式对话界面！
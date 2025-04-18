# PaddleOCR
本文Python环境为3.10.10

### 环境部署

#### 安装PaddlePaddle

```shell
# 机器安装的是CUDA9或CUDA10，则安装GPU版
python3 -m pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple
# CPU版
python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```

#### 安装PaddleOCR whl包

```shell
pip install "paddleocr==2.7.0" -i https://mirror.baidu.com/pypi/simple
```

### 脚本示例

```python
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr支持的多语言通过修改lang参数进行切换 
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
# 只需要执行一次，将模型加载至内存中
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

img_path = './catch.png'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)
```

### 模型下载
[模型列表](https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_ch/models_list.md)

**中文检测模型:**  
ch_PP-OCRv4_server_det  

**中文识别模型:**  
ch_PP-OCRv4_server_rec

```python
ocr = PaddleOCR(use_angle_cls=True, lang="ch", 
                det_model_dir="./ch_PP-OCRv4_det_server_infer", 
                rec_model_dir="./ch_PP-OCRv4_rec_server_infer")
```
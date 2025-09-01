# PaddleOCR

## 环境部署
Python环境为3.10

### PaddlePaddle
PaddlePaddle（PArallel Distributed Deep LEarning）是百度开源的深度学习框架，
类似于 TensorFlow 和 PyTorch。它提供了一套完整的工具和接口，用于构建、训练和部署深度学习模型。


安装依赖包  
```shell
# CPU版
pip install paddlepaddle -i https://mirrors.aliyun.com/pypi/simple

# GPU版（需 CUDA 11.2+）
pip install paddlepaddle-gpu -i https://mirrors.aliyun.com/pypi/simple
```

### 安装PaddleOCR
PaddleOCR 是基于 PaddlePaddle 开发的 OCR 工具库，专注于文本检测、识别和方向分类

核心功能:  
- 文本检测（Detection）: 定位图像中的文本区域（如 DBNet、EAST）
- 文本识别（Recognition）: 将检测到的文本区域转换为可读文本（如 CRNN、SVTR）
- 方向分类（Classification）: 判断文本方向（0°、90°、180°、270°）
- 多语言支持: 中文、英文、法语、日语等 80+ 语言

模型系列:  
- PP-OCR系列: 轻量级模型（如 PP-OCRv4、PP-OCRv5）。
- PP-Structure: 文档结构化分析（表格、标题、段落提取）。

安装依赖包  
```shell
pip install "paddleocr" --upgrade -i https://mirrors.aliyun.com/pypi/simple
```

### 模型下载

文本检测模型
```
https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-OCRv5_server_det_infer.tar
```

文本识别模型
```
https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-OCRv5_server_rec_infer.tar
```


## 代码实例

自动下载模型
```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    text_detection_model_name="PP-OCRv5_server_det",
    text_recognition_model_name="PP-OCRv5_server_rec",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang="ch"
)

image_path = "img.png"
result = ocr.predict(image_path)
texts = result[0].json.get('res').get('rec_texts')
print(texts)
```

配置本地模型
```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    text_detection_model_dir=r"model/PP-OCRv5_server_det_infer",
    text_recognition_model_dir=r"model/PP-OCRv5_server_rec_infer",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang="ch"
)

image_path = "img.png"
result = ocr.predict(image_path)
texts = result[0].json.get('res').get('rec_texts')
print(texts)
```



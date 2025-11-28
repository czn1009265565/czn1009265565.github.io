# Python Path

## 路径拼接和分解

```python
import os

# 路径拼接
path = os.path.join('dir1', 'dir2', 'file.txt')  # 'dir1/dir2/file.txt'

# 路径分解
dirname = os.path.dirname('/home/user/file.txt')  # '/home/user'
basename = os.path.basename('/home/user/file.txt')  # 'file.txt'
split_result = os.path.split('/home/user/file.txt')  # ('/home/user', 'file.txt')
```

## 路径检查和属性

```python
import os

# 检查路径是否存在
exists = os.path.exists('/some/path')

# 检查是否为文件/目录
is_file = os.path.isfile('/some/file.txt')
is_dir = os.path.isdir('/some/directory')

# 获取文件大小（字节）
size = os.path.getsize('/some/file.txt')

# 获取最后修改时间
mtime = os.path.getmtime('/some/file.txt')
```

## 路径规范化

```python
import os

# 获取绝对路径
abs_path = os.path.abspath('relative/path/file.txt')

# 规范化路径（处理 .. 和 .）
norm_path = os.path.normpath('/home/.././user/file.txt')  # '/user/file.txt'

# 获取相对路径
rel_path = os.path.relpath('/home/user/file.txt', '/home')  # 'user/file.txt'
```

## 扩展名处理

```python
import os

# 分离文件名和扩展名
name, ext = os.path.splitext('document.pdf')  # ('document', '.pdf')

# 获取扩展名
extension = os.path.splitext('image.jpg')[1]  # '.jpg'
```

## 获取项目根路径

```python
from pathlib import Path
import os


def get_project_root():
    """递归向上查找包含特定标识文件（如 .git、requirements.txt）的目录作为项目根目录"""
    current_path = Path(__file__).resolve()

    # 常见的项目根目录标识文件
    root_indicators = ['.git', '.gitignore', 'requirements.txt', 'setup.py', 'pyproject.toml']

    for parent in current_path.parents:
        if any((parent / indicator).exists() for indicator in root_indicators):
            return parent
    # 如果没有找到标识，返回当前文件的父目录
    return current_path.parent


if __name__ == "__main__":
    root = get_project_root()
    print(root)
```
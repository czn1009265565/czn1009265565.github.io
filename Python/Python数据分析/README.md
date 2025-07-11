# Python数据分析

## Python库

### NumPy
NumPy（Numerical Python的简称）是Python科学计算的基础包

1. 核心数据结构: 多维数组对象 ndarray  
   - 底层由C实现，提升运算速度
   - 内存优化
   - 向量化操作，优化循环开销
2. 丰富的数学函数
   - 线性代数（np.linalg）
   - 傅里叶变换（np.fft）
   - 随机数生成（np.random）
3. 生态兼容
   - 作为Pandas、SciPy、Matplotlib等库的基础数据容器
   - 可无缝对接GPU计算（通过CuPy）和分布式计算（Dask）

### Pandas

Pandas提供了快速便捷处理结构化数据的大量数据结构和函数，
数据操作、准备、清洗是数据分析最重要的技能，因此Pandas也是重点模块。

1. 核心数据结构  
   - 二维表格型结构 DataFrame
   - 一维带标签数组 Series
2. 数据操作能力  
   - 支持复杂精细的索引
   - 切片、切块
   - 分组聚合
3. 时间序列  

### Matplotlib
matplotlib是最流行的用于绘制图表和其它二维数据可视化的Python库。

### IPython和Jupyter

Jupyter Notebook 是一种支持多种语言的交互式网络代码“笔记本”，来使用IPython。
IPython shell 和Jupyter notebooks特别适合进行数据探索和可视化。

Jupyter Notebook还可以编写Markdown和HTML内容，它提供了一种创建代码和文本的富文本方法。
其它编程语言也在Jupyter中植入了内核，好让在Jupyter中可以使用Python以外的语言。

### SciPy

SciPy是一组专门解决科学计算中各种标准问题域的包的集合，主要包括下面这些包：

* scipy.integrate：数值积分例程和微分方程求解器。
* scipy.linalg：扩展了由numpy.linalg提供的线性代数例程和矩阵分解功能。
* scipy.optimize：函数优化器（最小化器）以及根查找算法。
* scipy.signal：信号处理工具。
* scipy.sparse：稀疏矩阵和稀疏线性系统求解器。
* scipy.special：SPECFUN（这是一个实现了许多常用数学函数（如伽玛函数）的Fortran库）的包装器。
* scipy.stats：标准连续和离散概率分布（如密度函数、采样器、连续分布函数等）、各种统计检验方法，以及更好的描述统计法。

NumPy和SciPy结合使用，便形成了一个相当完备和成熟的计算平台，可以处理多种传统的科学计算问题。

### scikit-learn
scikit-learn 是一个基于 Python 的开源机器学习库，专注于简洁、高效的工具链和统一的 API 设计。子模块包括：

* 分类：SVM、近邻、随机森林、逻辑回归等等。
* 回归：Lasso、岭回归等等。
* 聚类：k-均值、谱聚类等等。
* 降维：PCA、特征选择、矩阵分解等等。
* 选型：网格搜索、交叉验证、度量。
* 预处理：特征提取、标准化。

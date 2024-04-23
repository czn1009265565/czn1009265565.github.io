# Matplotlib
matplotlib是一个用于创建出版质量图表的桌面绘图包(主要是2D方面)

**引入约定**  
```python
import matplotlib.pyplot as plt
```

## Figure和AxesSubplot
类比一下生活中用纸笔绘图，我们需要先找到一张白纸， 在白纸上绘图。
使用Matplotlib面向对象绘图，绘图前我们要先创建一个Figure对象，Figure对象就相当于是白纸，
AxesSubplot就相当于白纸上的绘图区，拥有自己独立的坐标系统。

**创建画布**  
```python
fig = plt.figure()
```

**新建子图**  
```python
# 图像为是2×2的（即最多4张图），且当前选中的是4个subplot中的第一个（编号从1开始）
axes_subplot1 = fig.add_subplot(2,2,1)
axes_subplot2 = fig.add_subplot(2,2,2)
axes_subplot3 = fig.add_subplot(2,2,3)
axes_subplot4 = fig.add_subplot(2,2,4)
```

**创建画布和子图 (最常用)**
```python
# 创建画布和单个子图
fig,axes = plt.subplots()

# 创建画布和多个子图
fig,axes = plt.subplots(1,2)

# 共享X轴或Y轴
fig,axes = plt.subplots(1,2, sharex=True, sharey=True)
```

AxesSubplot属性值

```python
fig,axes = plt.subplots()
plt.rcParams['font.sans-serif'] = ['SimHei'] # 显示中文设置
axes.set_title('近十个交易日收盘价') # 设置标题
axes.set_xlabel('日期') # 设置X坐标轴标签
axes.set_xticklabels(pd.date_range('1/1/2023', periods=10, freq='D'), rotation=25) # 设置刻度字体旋转角度
axes.set_ylabel('收盘价') # Y坐标轴标签
axes.set_ylim(27,35) # Y坐标轴取值范围
plt.show()
```

**绘图**  
plt都是对当前或最近创建的AxesSubplot起作用的，
对应AxesSubplot对象上的两个方法，以`xlim`为例，就是`ax.get_xlim`和`ax.set_xlim`
```python
x = np.arange(10)
y = random.rand(10) 
# 绘制绿色虚线 等价于 plt.plot(x, y, linestyle='--', color='g')
plt.plot(x, y, 'g--')

# 指定x、y轴范围
plt.xlim([0,15])
plt.ylim([-3,3])

# 设置x轴刻度
plt.xticks([2,4,6,8,10])
plt.yticks([-2,0,2])
plt.show()
```

```python
x = np.arange(10)
y = np.random.rand(10)
fig,axes = plt.subplots(1)
axes.plot(x, y)
axes.set_xlim([0,12])
axes.set_ylim([0,1.2])
plt.show()
```

**保存文件**  
```python
x = np.arange(10)
y = np.random.rand(10)
fig,axes = plt.subplots(1)
axes.plot(x, y)
axes.set_xlim([0,12])
axes.set_ylim([0,1.2])
fig.savefig('figpath.jpg')

# 关闭画布对象
plt.close(fig)
```









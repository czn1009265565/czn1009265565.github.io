# Matplotlib
matplotlib是一个用于创建出版质量图表的桌面绘图包(主要是2D方面)

**引入约定**  
```python
import matplotlib.pyplot as plt
```

## Figure和Subplot

matplotlib的图像都位于Figure对象中

**创建画板**  
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

**创建画板和子图**
```python
fig,axes = plt.subplots(1,2)

# 共享X轴或Y轴
fig,axes = plt.subplots(1,2, sharex=True, sharey=True)
```

**绘图**  
plt都是对当前或最近创建的AxesSubplot起作用的，
对应subplot对象上的两个方法，以`xlim`为例，就是`ax.get_xlim`和`ax.set_xlim`
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
y1 = np.random.rand(10)
y2 = np.random.rand(10)
fig,axes = plt.subplots(1)
axes.plot(x, y1)
axes.set_xlim([0,12])
axes.set_ylim([0,1.2])
plt.show()
```

**保存文件**  
```python
plt.savefig('figpath.svg')
```









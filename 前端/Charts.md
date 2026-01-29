# Charts

Chart.js 是一个基于 HTML5 Canvas 的开源 JavaScript 图表库，用于创建响应式、美观的统计图表。

官网地址: `https://www.chartjs.org/docs/latest/`

## CDN引入

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

## 基础图表
```html
<div>
  <canvas id="myChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: 'label',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
</script>
```

## 图表类型

### 柱状图

```javascript
const labels = ['January', 'February', 'March', 'April', 'May', 'June','July'];
const values = [65, 59, 80, 81, 56, 55, 40];

const data = {
  labels: labels,
  datasets: [{
    label: 'DatasetName',
    data: values,
    // 设置不同的背景色
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(201, 203, 207, 0.2)'
    ],
    // 设置不同的边框色
    borderColor: [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(201, 203, 207)'
    ],
    // 边框宽度
    borderWidth: 1
  }]
};

const config = {
    type: 'bar',
    data: data,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    },
};
```

### 折线图

```javascript
const labels = ['January', 'February', 'March', 'April', 'May', 'June','July'];
const data = {
  labels: labels,
  datasets: [{
    label: 'DatasetName',
    data: [65, 59, 80, 81, 56, 55, 40],
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1
  }]
};
const config = {
    type: 'line',
    data: data,
};
```

### 饼图

```javascript
const data = {
  labels: [
    'Red',
    'Blue',
    'Yellow'
  ],
  datasets: [{
    label: 'My First Dataset',
    data: [300, 50, 100],
    backgroundColor: [
      'rgb(255, 99, 132)',
      'rgb(54, 162, 235)',
      'rgb(255, 205, 86)'
    ],
    hoverOffset: 4
  }]
};
const config = {
    type: 'doughnut',
    data: data,
};
```

### 散点图

```javascript
const data = {
    datasets: [{
        label: 'Scatter Dataset',
        data: [{
            x: -10,
            y: 0
        }, {
            x: 0,
            y: 10
        }, {
            x: 10,
            y: 5
        }, {
            x: 0.5,
            y: 5.5
        }],
        backgroundColor: 'rgb(255, 99, 132)'
    }],
};
const config = {
    type: 'scatter',
    data: data,
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom'
            }
        }
    }
};
```

## 配置选项

### 通用配置
```
options: {
    responsive: true, // 响应式
    maintainAspectRatio: false, // 不保持宽高比
    plugins: {
        legend: {
            position: 'top', // 图例位置
        },
        title: {
            display: true,
            text: 'Chart Title'
        }
    }
}
```

### 坐标轴配置

```
scales: {
    x: {
        title: {
            display: true,
            text: 'X Axis Title'
        }
    },
    y: {
        title: {
            display: true,
            text: 'Y Axis Title'
        },
        min: 0,
        max: 100
    }
}
```
# Bootstrap 插件-模态框

Bootstrap的模态框（Modal）是一个灵活的可重复使用的对话框组件，用于显示内容、表单或其他交互元素。

## 基本结构

```html
<!-- 模态框 -->
<div class="modal fade" id="alertModal" tabindex="-1" aria-labelledby="alertModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <!-- 模态框头部 -->
            <div class="modal-header">
                <h5 class="modal-title" id="alertModalLabel">模态框标题</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>

            <!-- 模态框主体 -->
            <div class="modal-body">
                <p>这里是模态框的内容</p>
            </div>

            <!-- 模态框底部 -->
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                <button type="button" class="btn btn-primary">提交</button>
            </div>
        </div>
    </div>
</div>
```

- `.modal`	模态框容器
- `.fade`	添加淡入淡出动画效果
- `.modal-dialog`	模态框对话框容器
- `.modal-content`	模态框内容区域
- `.modal-header`	模态框头部
- `.modal-body`	模态框主体内容
- `.modal-footer`	模态框底部
- `data-bs-dismiss="modal"`	关闭模态框的触发器
- `aria-labelledby`	可访问性属性，关联标题
- `aria-hidden="true"`	可访问性属性，隐藏模态框

## 触发模态框

```html
<div class="container">
    <button id="alertButton">触发模态框</button>
</div>

<script>
    $("#alertButton").click(function() {
        $('#alertModal').modal('show');
    });
</script>
```

自动关闭模态框

```html
<script>
    $("#alertButton").click(function() {
        let alertModal = $('#alertModal');
        alertModal.modal('show');

        // 三秒后自动关闭
        setTimeout(function () {
            alertModal.modal('hide')
        }, 3000)
    });
</script>
```


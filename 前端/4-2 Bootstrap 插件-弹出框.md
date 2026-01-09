# Bootstrap 插件-弹出框
弹出框（Popover）是一种轻量级的弹出式提示组件，常用于展示额外的信息或交互选项

特性:
- 触发方式：支持点击、悬停（hover）、聚焦等触发方式。
- 自定义内容：支持标题和正文内容，可包含 HTML。
- 位置控制：可设置弹出方向（顶部、底部、左侧、右侧）


## 基本用法

```html
<div class="container" style="padding: 100px 50px 10px;">
    <button type="button"
            class="btn btn-primary"
            data-bs-toggle="popover"
            data-bs-placement="top"
            data-bs-trigger="hover"
            data-bs-title="提示标题"
            data-bs-content="这是弹出框内容">
        悬停触发
    </button>
</div>
```

- `data-bs-placement`: 弹出框的位置: 'top'、'bottom'、'left'、'right'，或自动调整（如 'auto'）
- `data-bs-trigger`: 触发事件（如 click、hover）
- `data-bs-title`: 弹出框的标题内容
- `data-bs-content`: 弹出框的内容

绑定鼠标悬停事件

```html
<script>
    $(function () {
        $("[data-bs-toggle='popover']").popover();
    });
</script>
```

## 事件委托
需要触发弹出框的元素是动态生成时，则不能简单直接基于元素绑定，需要通过事件委托的方式

```html
<script>
    $('.container')
            .on('mouseenter', '[data-bs-toggle="popover"]', function () {
                let $element = $(this);
                $element.popover('show');
            })
            .on('mouseleave', '[data-bs-toggle="popover"]', function () {
                let $element = $(this);
                $element.popover('hide');
            });
</script>
```

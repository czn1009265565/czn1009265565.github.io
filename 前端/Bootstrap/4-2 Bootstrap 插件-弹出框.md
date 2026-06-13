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

html样式

```html
<div class="container" style="padding: 100px 50px 10px;">
    <button type="button"
            class="btn btn-primary"
            data-bs-toggle="popover"
            data-bs-placement="top"
            data-bs-trigger="hover"
            data-bs-html="true"
            data-bs-title="<i>提示标题</i>"
            data-bs-content="这是弹出框内容">
        悬停触发
    </button>
</div>
```

- `data-bs-html`: 是否解析内容中的 HTML 标签。若为 false，内容会被转义为纯文本

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

如果弹出框的内容支持动态变更，则需要实时获取数据

```html
<script>
    $('.container')
            .on('mouseenter', '[data-bs-toggle="popover"]', function () {
                let $element = $(this);
                // 获取最新的数据 
                // data-title和data-content是自定义的属性
                let title = $element.attr('data-title');
                let content = $element.attr('data-content');
                // 更新 Popover 内容
                $element.attr('data-bs-title', title);
                $element.attr('data-bs-content', content);
                $element.popover('dispose').popover({
                    trigger: 'manual',
                    html: true
                });

                $element.popover('show');
            })
            .on('mouseleave', '[data-bs-toggle="popover"]', function () {
                let $element = $(this);
                $element.popover('hide');
            });

</script>
```
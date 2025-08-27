# Selenium
Selenium 是一个强大的 Web 自动化测试工具，可以模拟用户操作浏览器。

## 环境安装

### 1. 安装依赖包

```shell
pip install selenium -i https://mirrors.aliyun.com/pypi/simple
```

### 2. 下载浏览器驱动

Selenium 需要通过浏览器驱动来控制浏览器。不同的浏览器需要不同的驱动，这里以Chrome Driver为例

[ChromeDriver 介绍](https://www.runoob.com/w3cnote/chromedriver-intro.html)

下载地址: https://googlechromelabs.github.io/chrome-for-testing/

下载完成后需配置环境变量

## 基础使用

### Web Driver
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 普通模式启动 Chrome
driver = webdriver.Chrome()

# 也可以自定义指定路径 
# webdriver.Chrome('/path/to/chromedriver')

# 设置无头浏览器
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # 启用无头模式
# chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
# driver = webdriver.Chrome(options=chrome_options)

# 访问网页
driver.get("https://www.baidu.com")

# 获取当前标题
print(driver.title)  # 输出: 百度一下，你就知道

# 关闭浏览器
driver.quit()
```

### 元素定位

```python
from selenium.webdriver.common.by import By

# 通过ID
element = driver.find_element(By.ID, "kw")

# 通过name
element = driver.find_element(By.NAME, "wd")

# 通过class name
element = driver.find_element(By.CLASS_NAME, "s_ipt")

# 通过标签名
element = driver.find_element(By.TAG_NAME, "input")

# 通过CSS选择器
element = driver.find_element(By.CSS_SELECTOR, "#kw")

# 通过XPath
element = driver.find_element(By.XPATH, "//input[@id='kw']")
```

### 元素操作

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# 输入文本
search_box = driver.find_element(By.ID, "kw")
search_box.send_keys("Selenium教程")

# 点击元素
search_button = driver.find_element(By.ID, "su")
search_button.click()

# 清除输入
search_box.clear()

# 获取元素文本
text = driver.find_element(By.ID, "element_id").text

# 获取属性值
value = driver.find_element(By.ID, "element_id").get_attribute("value")

# 检查复选框或单选框是否被选中，并选中或取消选中
checkbox_element = driver.find_element_by_id("checkbox-id")
if not checkbox_element.is_selected():
    checkbox_element.click()

# 通过索引、值或可见文本选择下拉列表的选项
# 定位下拉列表元素
dropdown_element = driver.find_element_by_id("dropdown-id")
select = Select(dropdown_element)
# 通过可见文本选择选项
select.select_by_visible_text("Option 1")
# 通过值选择选项
select.select_by_value("1")
# 通过索引选择选项
select.select_by_index(0)

# 执行JavaScript
# 滚动到页面底部
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 修改元素属性
driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, "color: red;")
```

### 鼠标与键盘操作

鼠标操作
```python
# 定位元素
element = driver.find_element(By.ID, "element_id")
# 创建 ActionChains 对象
actions = ActionChains(driver)
# 点击操作
actions.click(element).perform()
# 双击操作
actions.double_click(element).perform()
# 右键点击操作
actions.context_click(element).perform()
# 悬停操作
actions.move_to_element(element).perform()
```

键盘操作
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 定位输入框
input_element = driver.find_element(By.ID, "input_element_id")
# 输入内容并发送组合键
input_element.send_keys("Hello, World!")
input_element.send_keys(Keys.CONTROL, 'a')  # 全选
input_element.send_keys(Keys.CONTROL, 'c')  # 复制
input_element.send_keys(Keys.CONTROL, 'v')  # 粘贴
```

## 等待机制
在 Selenium 中，等待机制是确保页面元素加载完成后再进行操作的关键。

由于网页加载速度受网络、服务器性能等因素影响，直接操作未加载完成的元素会导致脚本失败。

1. 隐式等待，是一种全局性的等待机制，它会在查找元素时等待一定的时间 `driver.implicitly_wait(3)`
2. 显式等待，是一种更为灵活的等待机制，它允许你为特定的操作设置等待条件  
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置显式等待，最多等待 10 秒，直到元素出现
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "element_id"))
)
```

## 浏览器操作

| 函数名称                                | 说明                  | 示例                                                   |
|-------------------------------------|---------------------|------------------------------------------------------|
| get(url)                            | 导航到指定URL            | driver.get("https://www.example.com")                |
| quit()                              | 关闭所有窗口并结束会话         | driver.quit()                                        |
| close()                             | 关闭当前窗口              | driver.close()                                       |
| back()                              | 后退到上一页              | driver.back()                                        |
| forward()                           | 前进到下一页              | driver.forward()                                     |
| refresh()                           | 刷新当前页面              | driver.refresh()                                     |
| maximize_window()                   | 最大化浏览器窗口            | driver.maximize_window()                             |
| minimize_window()                   | 最小化浏览器窗口            | driver.minimize_window()                             |
| fullscreen_window()                 | 全屏显示浏览器             | driver.fullscreen_window()                           |
| set_window_size(width, height)      | 设置浏览器窗口大小           | driver.set_window_size(1920, 1080)                   |
| set_window_position(x, y)           | 设置浏览器窗口位置           | driver.set_window_position(0, 0)                     |
| get_window_size()                   | 获取当前窗口尺寸            | size = driver.get_window_size()                      |
| get_window_position()               | 获取当前窗口位置            | position = driver.get_window_position()              |
| save_screenshot(filename)           | 截取当前页面保存为图片         | driver.save_screenshot("page.png")                   |
| execute_script(script, *args)       | 在当前页面执行JavaScript代码 | driver.execute_script("return document.title")       |
| execute_async_script(script, *args) | 执行异步JavaScript代码    | driver.execute_async_script("return document.title") |
| switch_to.window(window_handle)     | 切换到指定窗口             | driver.switch_to.window(handle)                      |
| switch_to.frame(frame_reference)    | 切换到指定frame          | driver.switch_to.frame("frame_name")                 |
| switch_to.default_content()         | 切换回主文档              | driver.switch_to.default_content()                   |
| switch_to.alert                     | 切换到弹出框              | alert = driver.switch_to.alert                       |
| get_cookies()                       | 获取所有Cookie          | cookies = driver.get_cookies()                       |
| get_cookie(name)                    | 获取指定名称的Cookie       | cookie = driver.get_cookie("sessionid")              |
| add_cookie(cookie_dict)             | 添加Cookie            | driver.add_cookie({"name": "key", "value": "value"}) |
| delete_cookie(name)                 | 删除指定Cookie          | driver.delete_cookie("key")                          |
| delete_all_cookies()                | 删除所有Cookie          | driver.delete_all_cookies()                          |
| current_url                         | 获取当前页面URL           | url = driver.current_url                             |
| title                               | 获取当前页面标题            | title = driver.title                                 |
| page_source                         | 获取当前页面源码            | source = driver.page_source                          |
| name                                | 获取当前浏览器名称           | browser_name = driver.name                           |
| current_window_handle               | 获取当前窗口句柄            | handle = driver.current_window_handle                |
| window_handles                      | 获取所有窗口句柄列表          | handles = driver.window_handles                      |

## 最佳实践

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# 初始化浏览器
chrome_options = Options()
chrome_options.add_argument("--headless")  # 启用无头模式
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
driver = webdriver.Chrome(options=chrome_options)

try:
    # 打开百度
    driver.get("https://www.baidu.com")
    
    # 定位搜索框并输入内容
    search_box = driver.find_element(By.ID, "kw")
    search_box.send_keys("Python Selenium教程")
    
    # 模拟回车键搜索
    search_box.send_keys(Keys.RETURN)
    
    # 等待结果加载
    results = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h3.c-title"))
    )
    for result in results[:5]:
        print(result.text)
        
finally:
    # 关闭浏览器
    driver.quit()
```
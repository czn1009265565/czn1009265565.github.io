# Scrapy Selenium

## 安装依赖

```shell
# 安装必要的包
pip install scrapy selenium webdriver-manager -i https://mirrors.aliyun.com/pypi/simple
```

## Selenium Middleware

```python
# middlewares.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from scrapy.http import HtmlResponse
import time
import logging

class SeleniumMiddleware:
    """Selenium Chrome 中间件"""
    
    def __init__(self, chrome_options=None):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.chrome_options = chrome_options or self.get_default_options()
    
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=scrapy.signals.spider_closed)
        return middleware
    
    def get_default_options(self):
        """获取默认 Chrome 选项"""
        options = Options()
        
        # 基础配置
        options.add_argument('--headless')  # 无头模式
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # 性能优化
        options.add_argument('--disable-images')  # 禁用图片加载
        options.add_argument('--disable-javascript')  # 可选：禁用JS（如不需要）
        
        # 反检测配置
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        return options
    
    def open_driver(self):
        """打开浏览器驱动"""
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            
            # 隐藏自动化特征
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("Chrome 浏览器启动成功")
        except Exception as e:
            self.logger.error(f"浏览器启动失败: {e}")
            raise
    
    def process_request(self, request, spider):
        """处理请求"""
        if not request.meta.get('selenium', False):
            return None  # 不使用 Selenium
            
        if self.driver is None:
            self.open_driver()
        
        try:
            # 设置超时
            self.driver.set_page_load_timeout(request.meta.get('selenium_timeout', 30))
            
            # 访问页面
            self.driver.get(request.url)
            
            # 等待页面加载（可配置）
            wait_time = request.meta.get('wait_time', 2)
            if wait_time > 0:
                time.sleep(wait_time)
            
            # 执行自定义JS（可选）
            if 'execute_script' in request.meta:
                self.driver.execute_script(request.meta['execute_script'])
            
            # 等待特定元素（可选）
            if 'wait_for' in request.meta:
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                
                wait = WebDriverWait(self.driver, request.meta.get('wait_timeout', 10))
                wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, request.meta['wait_for'])
                ))
            
            # 获取页面源码
            body = self.driver.page_source.encode('utf-8')
            
            # 关闭当前标签页（如果是新开的）
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            
            return HtmlResponse(
                url=self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )
            
        except TimeoutException:
            self.logger.error(f"页面加载超时: {request.url}")
            return HtmlResponse(url=request.url, status=500, request=request)
        except Exception as e:
            self.logger.error(f"Selenium 处理失败: {e}")
            return HtmlResponse(url=request.url, status=500, request=request)
    
    def spider_closed(self, spider):
        """爬虫关闭时清理资源"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Chrome 浏览器已关闭")
```

### Spider

```python
# spiders/interactive_spider.py
import scrapy
import json

class InteractiveSpider(scrapy.Spider):
    name = "interactive_spider"
    
    def start_requests(self):
        # 需要复杂交互的页面
        yield scrapy.Request(
            url='https://example.com/login-required-page',
            callback=self.parse_login,
            meta={
                'selenium': True,
                'wait_time': 2,
            }
        )
    
    def parse_login(self, response):
        """处理登录页面"""
        # 执行登录操作
        login_script = """
        document.querySelector('#username').value = 'my_username';
        document.querySelector('#password').value = 'my_password';
        document.querySelector('#login-btn').click();
        """
        
        yield scrapy.Request(
            url=response.url,  # 相同URL，但会执行登录脚本
            callback=self.after_login,
            meta={
                'selenium': True,
                'scripts': [login_script],
                'wait_time': 3,
                'wait_for': '.dashboard',  # 等待登录后页面
                'dont_redirect': True,
            }
        )
    
    def after_login(self, response):
        """登录后处理"""
        # 检查登录是否成功
        if 'dashboard' in response.text:
            # 继续爬取其他页面
            yield from self.crawl_after_login(response)
        else:
            self.logger.error("登录失败")
    
    def crawl_after_login(self, response):
        """登录后的爬取逻辑"""
        # 示例：爬取分页数据
        for page in range(1, 6):
            page_url = f'https://example.com/data?page={page}'
            yield scrapy.Request(
                url=page_url,
                callback=self.parse_data_page,
                meta={
                    'selenium': True,
                    'wait_time': 2,
                    'wait_for': '.data-table',
                }
            )
    
    def parse_data_page(self, response):
        """解析数据页面"""
        items = response.css('.data-item')
        for item in items:
            yield {
                'name': item.css('.name::text').get(),
                'value': item.css('.value::text').get(),
                'page_url': response.url,
            }
```
# PyQt6 库存管理系统

本文通过PyQt6 基于MVC架构实现一个库存管理系统

MVC架构说明:

1. 模型(Model):  
   - 负责数据存储和业务逻辑
   - 包含ProductModel、SupplierModel等
   - 直接与数据库交互
2. 视图(View):  
   - 负责用户界面展示
   - 包含各种QWidget子类
   - 不包含业务逻辑，只负责显示数据和接收用户输入
3. 控制器(Controller):  
   - 作为模型和视图之间的桥梁
   - 处理用户输入，更新模型，并刷新视图
   - 包含业务逻辑和事件处理

## 1. 系统概述
这个库存管理系统包含以下功能：

1. 产品管理（增删改查）
2. 库存跟踪
3. 供应商管理
4. 交易记录
5. 报表生成

## 2. 项目结构

```
inventory/
├── models/          # 模型层
│   ├── __init__.py
│   ├── product.py
│   ├── supplier.py
│   ├── inventory.py
│   └── database.py  # 数据库连接
├── views/           # 视图层
│   ├── __init__.py
│   ├── main_window.py
│   ├── product_view.py
│   ├── supplier_view.py
│   └── reports_view.py
├── controllers/     # 控制器层
│   ├── __init__.py
│   ├── main_controller.py
│   ├── product_controller.py
│   ├── supplier_controller.py
│   └── reports_controller.py
└── app.py           # 应用入口
```

## 3. 模型层实现

###  3.1 数据库模型 (models/database.py)

```python
import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name='inventory.db'):
        self.db_name = db_name
        self._init_db()
    
    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 创建产品表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    unit_price REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建供应商表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact_person TEXT,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建库存表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    location TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            # 创建交易记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    transaction_type TEXT CHECK(transaction_type IN ('IN', 'OUT')),
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    total_amount REAL NOT NULL,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
    
    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query, params=(), fetch=False):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
```

### 3.2 产品模型 (models/product.py)

```python
from datetime import datetime
from .database import Database

class ProductModel:
    def __init__(self):
        self.db = Database()
    
    def create_product(self, name, description, category, unit_price):
        query = '''
            INSERT INTO products (name, description, category, unit_price)
            VALUES (?, ?, ?, ?)
        '''
        self.db.execute_query(query, (name, description, category, unit_price))
        return self.get_last_inserted_product()
    
    def get_product(self, product_id):
        query = 'SELECT * FROM products WHERE id = ?'
        result = self.db.execute_query(query, (product_id,), fetch=True)
        return result[0] if result else None
    
    def get_all_products(self):
        query = 'SELECT * FROM products ORDER BY name'
        return self.db.execute_query(query, fetch=True)
    
    def update_product(self, product_id, name, description, category, unit_price):
        query = '''
            UPDATE products 
            SET name = ?, description = ?, category = ?, unit_price = ?
            WHERE id = ?
        '''
        self.db.execute_query(query, (name, description, category, unit_price, product_id))
    
    def delete_product(self, product_id):
        query = 'DELETE FROM products WHERE id = ?'
        self.db.execute_query(query, (product_id,))
    
    def get_last_inserted_product(self):
        query = 'SELECT * FROM products ORDER BY id DESC LIMIT 1'
        result = self.db.execute_query(query, fetch=True)
        return result[0] if result else None
    
    def search_products(self, search_term):
        query = '''
            SELECT * FROM products 
            WHERE name LIKE ? OR description LIKE ? OR category LIKE ?
            ORDER BY name
        '''
        search_param = f'%{search_term}%'
        return self.db.execute_query(query, (search_param, search_param, search_param), fetch=True)
```

## 4. 视图层实现

### 4.1 主窗口视图 (views/main_window.py)

```python
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QStatusBar, QMenuBar, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt
from .product_view import ProductView
from .supplier_view import SupplierView
from .reports_view import ReportsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("库存管理系统 - MVC架构")
        self.resize(1024, 768)
        
        # 初始化UI
        self._init_ui()
        
    def _init_ui(self):
        # 创建菜单栏
        self._create_menu_bar()
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")
        
        # 创建主选项卡
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # 添加各个功能视图
        self.product_view = ProductView()
        self.supplier_view = SupplierView()
        self.reports_view = ReportsView()
        
        self.tab_widget.addTab(self.product_view, "产品管理")
        self.tab_widget.addTab(self.supplier_view, "供应商管理")
        self.tab_widget.addTab(self.reports_view, "报表")
    
    def _create_menu_bar(self):
        menu_bar = QMenuBar()
        
        # 文件菜单
        file_menu = QMenu("文件(&F)", self)
        exit_action = file_menu.addAction("退出")
        exit_action.triggered.connect(self.close)
        menu_bar.addMenu(file_menu)
        
        # 帮助菜单
        help_menu = QMenu("帮助(&H)", self)
        about_action = help_menu.addAction("关于")
        about_action.triggered.connect(self._show_about)
        menu_bar.addMenu(help_menu)
        
        self.setMenuBar(menu_bar)
    
    def _show_about(self):
        QMessageBox.about(self, "关于", 
            "库存管理系统 v1.0\n\n"
            "使用PyQt6和MVC架构开发")
    
    def show_status_message(self, message, timeout=5000):
        self.statusBar().showMessage(message, timeout)
```

### 4.2 产品视图 (views/product_view.py)

```python
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QLabel, QComboBox, QFormLayout,
    QGroupBox, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal

class ProductView(QWidget):
    # 定义信号
    add_product_signal = pyqtSignal(dict)
    update_product_signal = pyqtSignal(dict)
    delete_product_signal = pyqtSignal(int)
    search_product_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        main_layout = QHBoxLayout()
        
        # 左侧表单区域
        form_group = QGroupBox("产品信息")
        form_layout = QFormLayout()
        
        self.product_id_input = QLineEdit()
        self.product_id_input.setReadOnly(True)
        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(["电子产品", "办公用品", "家居用品", "食品", "其他"])
        self.unit_price_input = QLineEdit()
        
        form_layout.addRow("ID:", self.product_id_input)
        form_layout.addRow("名称:", self.name_input)
        form_layout.addRow("描述:", self.description_input)
        form_layout.addRow("类别:", self.category_input)
        form_layout.addRow("单价:", self.unit_price_input)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加")
        self.update_button = QPushButton("更新")
        self.delete_button = QPushButton("删除")
        self.clear_button = QPushButton("清空")
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        
        form_group.setLayout(form_layout)
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(form_group)
        left_layout.addLayout(button_layout)
        
        # 右侧表格区域
        right_layout = QVBoxLayout()
        
        # 搜索区域
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索产品...")
        search_button = QPushButton("搜索")
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        
        # 产品表格
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels(
            ["ID", "名称", "描述", "类别", "单价", "创建时间"]
        )
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.product_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        right_layout.addLayout(search_layout)
        right_layout.addWidget(self.product_table)
        
        # 主布局
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        
        self.setLayout(main_layout)
        
        # 初始状态
        self._set_form_enabled(False)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
    
    def _connect_signals(self):
        self.add_button.clicked.connect(self._on_add_product)
        self.update_button.clicked.connect(self._on_update_product)
        self.delete_button.clicked.connect(self._on_delete_product)
        self.clear_button.clicked.connect(self._on_clear_form)
        self.product_table.itemSelectionChanged.connect(self._on_table_selection_changed)
    
    def _on_add_product(self):
        product_data = {
            'name': self.name_input.text(),
            'description': self.description_input.text(),
            'category': self.category_input.currentText(),
            'unit_price': float(self.unit_price_input.text())
        }
        self.add_product_signal.emit(product_data)
    
    def _on_update_product(self):
        product_data = {
            'id': int(self.product_id_input.text()),
            'name': self.name_input.text(),
            'description': self.description_input.text(),
            'category': self.category_input.currentText(),
            'unit_price': float(self.unit_price_input.text())
        }
        self.update_product_signal.emit(product_data)
    
    def _on_delete_product(self):
        product_id = int(self.product_id_input.text())
        reply = QMessageBox.question(
            self, '确认删除',
            f'确定要删除产品ID {product_id} 吗?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_product_signal.emit(product_id)
    
    def _on_clear_form(self):
        self.product_id_input.clear()
        self.name_input.clear()
        self.description_input.clear()
        self.category_input.setCurrentIndex(0)
        self.unit_price_input.clear()
        self.product_table.clearSelection()
        self._set_form_enabled(False)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
    
    def _on_table_selection_changed(self):
        selected_items = self.product_table.selectedItems()
        if selected_items:
            self._set_form_enabled(True)
            self.update_button.setEnabled(True)
            self.delete_button.setEnabled(True)
            
            self.product_id_input.setText(selected_items[0].text())
            self.name_input.setText(selected_items[1].text())
            self.description_input.setText(selected_items[2].text())
            
            category_index = self.category_input.findText(selected_items[3].text())
            if category_index >= 0:
                self.category_input.setCurrentIndex(category_index)
            
            self.unit_price_input.setText(selected_items[4].text())
    
    def _set_form_enabled(self, enabled):
        self.name_input.setEnabled(enabled)
        self.description_input.setEnabled(enabled)
        self.category_input.setEnabled(enabled)
        self.unit_price_input.setEnabled(enabled)
    
    def display_products(self, products):
        self.product_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.product_table.setItem(row, 0, QTableWidgetItem(str(product[0])))
            self.product_table.setItem(row, 1, QTableWidgetItem(product[1]))
            self.product_table.setItem(row, 2, QTableWidgetItem(product[2]))
            self.product_table.setItem(row, 3, QTableWidgetItem(product[3]))
            self.product_table.setItem(row, 4, QTableWidgetItem(f"{product[4]:.2f}"))
            self.product_table.setItem(row, 5, QTableWidgetItem(product[5]))
    
    def show_error(self, message):
        QMessageBox.critical(self, "错误", message)
    
    def show_success(self, message):
        QMessageBox.information(self, "成功", message)
```

## 5. 控制器层实现

### 5.1 主控制器 (controllers/main_controller.py)

```python
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from controllers.product_controller import ProductController
from controllers.supplier_controller import SupplierController
from controllers.reports_controller import ReportsController

class MainController:
    def __init__(self):
        self.app = QApplication([])
        self.main_window = MainWindow()
        
        # 初始化子控制器
        self.product_controller = ProductController(self.main_window.product_view)
        self.supplier_controller = SupplierController(self.main_window.supplier_view)
        self.reports_controller = ReportsController(self.main_window.reports_view)
        
        # 连接信号
        self._connect_signals()
    
    def _connect_signals(self):
        # 这里可以添加主窗口级别的信号连接
        pass
    
    def run(self):
        self.main_window.show()
        self.app.exec()
```

### 5.2 产品控制器 (controllers/product_controller.py)

```python
from models.product import ProductModel
from PyQt6.QtCore import QObject, pyqtSlot

class ProductController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = ProductModel()
        
        # 初始化数据
        self._load_products()
        
        # 连接信号和槽
        self._connect_signals()
    
    def _connect_signals(self):
        self.view.add_product_signal.connect(self.add_product)
        self.view.update_product_signal.connect(self.update_product)
        self.view.delete_product_signal.connect(self.delete_product)
        self.view.search_product_signal.connect(self.search_products)
    
    def _load_products(self):
        products = self.model.get_all_products()
        self.view.display_products(products)
    
    @pyqtSlot(dict)
    def add_product(self, product_data):
        try:
            self.model.create_product(
                product_data['name'],
                product_data['description'],
                product_data['category'],
                product_data['unit_price']
            )
            self._load_products()
            self.view.show_success("产品添加成功!")
            self.view._on_clear_form()
        except Exception as e:
            self.view.show_error(f"添加产品失败: {str(e)}")
    
    @pyqtSlot(dict)
    def update_product(self, product_data):
        try:
            self.model.update_product(
                product_data['id'],
                product_data['name'],
                product_data['description'],
                product_data['category'],
                product_data['unit_price']
            )
            self._load_products()
            self.view.show_success("产品更新成功!")
        except Exception as e:
            self.view.show_error(f"更新产品失败: {str(e)}")
    
    @pyqtSlot(int)
    def delete_product(self, product_id):
        try:
            self.model.delete_product(product_id)
            self._load_products()
            self.view.show_success("产品删除成功!")
            self.view._on_clear_form()
        except Exception as e:
            self.view.show_error(f"删除产品失败: {str(e)}")
    
    @pyqtSlot(str)
    def search_products(self, search_term):
        try:
            products = self.model.search_products(search_term)
            self.view.display_products(products)
        except Exception as e:
            self.view.show_error(f"搜索失败: {str(e)}")
```

## 6. 应用入口 (app.py)

```python
import sys
from controllers.main_controller import MainController

def main():
    controller = MainController()
    controller.run()

if __name__ == "__main__":
    main()
```



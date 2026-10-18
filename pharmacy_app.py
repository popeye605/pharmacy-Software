#!/usr/bin/env python3
"""
Pharmacy POS System - Fatima Tu Zahra Medical Centre
Complete professional pharmacy management system with RBAC, advanced billing, and inventory management.
"""

import sys
import sqlite3
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QFrame, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton,
    QSpinBox, QDoubleSpinBox, QComboBox, QDialog, QFormLayout, QMessageBox,
    QDateEdit, QTextEdit, QHeaderView, QTabWidget, QCheckBox, QStatusBar,
    QAbstractItemView, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QTimer, QSize, QMarginsF,QSizeF
from PyQt6.QtGui import QFont, QColor, QIcon, QPalette, QBrush, QPixmap
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QTimer, QSize, QMarginsF
from PyQt6.QtGui import QFont, QColor, QIcon, QPalette, QBrush, QPixmap, QTextDocument, QPageLayout,QPageSize
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# ==================== THEME & STYLING ====================
THEME_STYLESHEET = """
    QMainWindow {
        background-color: #f0f0f0;
    }
    
    QWidget {
        background-color: #f0f0f0;
        color: #333333;
    }
    
    QMainWindow > QWidget {
        background-color: #f0f0f0;
    }
    
    /* Sidebar Styling */
    #sidebar {
        background-color: #1e3a5f;
        border: none;
    }
    
    #sidebar QPushButton {
        background-color: #1e3a5f;
        color: white;
        border: none;
        padding: 12px;
        text-align: left;
        font-size: 12px;
        font-weight: 500;
        margin: 2px 0;
        border-radius: 4px;
    }
    
    #sidebar QPushButton:hover {
        background-color: #2c5282;
    }
    
    #sidebar QPushButton:pressed {
        background-color: #276749;
    }
    
    /* Header Styling */
    #header {
        background-color: #2c5282;
        border-bottom: 2px solid #1e3a5f;
    }
    
    #headerLabel {
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Button Styling - Default */
    QPushButton {
        background-color: #2c5282;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
    
    QPushButton:hover {
        background-color: #1e3a5f;
    }
    
    QPushButton:pressed {
        background-color: #0d1f35;
    }
    
    /* Success Button (Green) */
    QPushButton#successBtn {
        background-color: #276749;
    }
    
    QPushButton#successBtn:hover {
        background-color: #1d5035;
    }
    
    QPushButton#successBtn:pressed {
        background-color: #0f2d1b;
    }
    
    /* Danger Button (Red) */
    QPushButton#dangerBtn {
        background-color: #c53030;
    }
    
    QPushButton#dangerBtn:hover {
        background-color: #a02020;
    }
    
    QPushButton#dangerBtn:pressed {
        background-color: #7a1818;
    }
    
    /* Warning Button (Orange) */
    QPushButton#warningBtn {
        background-color: #d69e2e;
    }
    
    QPushButton#warningBtn:hover {
        background-color: #b8860b;
    }
    
    QPushButton#warningBtn:pressed {
        background-color: #92670f;
    }
    
    /* Input Styling */
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit, QTextEdit {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 6px;
        font-size: 11px;
    }
    
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
        border: 2px solid #2c5282;
        background-color: #ffffff;
    }
    
    /* Table Styling */
    QTableWidget {
        background-color: #ffffff;
        gridline-color: #e0e0e0;
        border: 1px solid #cccccc;
        border-radius: 4px;
    }
    
    QTableWidget::item {
        padding: 4px;
    }
    
    QTableWidget::item:selected {
        background-color: #2c5282;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #2c5282;
        color: white;
        padding: 6px;
        border: none;
        font-weight: bold;
    }
    
    /* Group Box & Frames */
    QGroupBox {
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 10px;
        margin-top: 10px;
        color: #333333;
        font-weight: 500;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
    }
    
    QFrame {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
    }
    
    /* Labels */
    QLabel {
        color: #333333;
    }
    
    /* Cards */
    #kpiCard {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
    }
    
    #kpiValue {
        color: #2c5282;
        font-size: 28px;
        font-weight: bold;
    }
    
    #kpiLabel {
        color: #666666;
        font-size: 12px;
    }
    
    /* Tabs */
    QTabBar::tab {
        background-color: #e0e0e0;
        color: #333333;
        padding: 6px 12px;
        margin: 2px;
        border: none;
        border-radius: 4px;
    }
    
    QTabBar::tab:selected {
        background-color: #2c5282;
        color: white;
    }
    
    /* Status bar */
    QStatusBar {
        background-color: #2c5282;
        color: white;
    }
"""

# ==================== DATABASE MANAGER ====================
# ==================== DATABASE MANAGER ====================
class PharmacyDB:
    """Database manager for pharmacy operations."""
    
    def __init__(self, db_path='pharmacy_pos.db'):
        self.db_path = db_path
        self.connect()
        self.initialize_tables()
    
    def connect(self):
        """Create database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def execute(self, query, params=None):
        """Execute query and return cursor."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except Exception as e:
            print(f"Database execution error: {e}")
            raise

    def fetch_one(self, query, params=None):
        """Fetch single row."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except Exception as e:
            print(f"Database fetch_one error: {e}")
            return None

    def fetch_all(self, query, params=None):
        """Fetch all rows - THIS WAS MISSING AND CAUSING THE CRASH."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Database fetch_all error: {e}")
            return []

    def get_next_bill_number(self):
        """Get next bill number."""
        result = self.fetch_one("SELECT MAX(bill_number) as max_num FROM bills")
        if result and result['max_num']:
            return result['max_num'] + 1
        return 1001

    def initialize_tables(self):
        """Create all necessary tables and default admin."""
        cursor = self.conn.cursor()
        # Users table
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE, password TEXT, full_name TEXT, 
            email TEXT, role TEXT, is_active INTEGER DEFAULT 1, 
            last_login TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        
        # Products table
        cursor.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    serial_no TEXT, 
    name TEXT, 
    category_id INTEGER, 
    vendor_id INTEGER, -- Make sure this line is here
    purchase_price REAL DEFAULT 0.0, 
    sale_price REAL DEFAULT 0.0, 
    quantity_stock INTEGER DEFAULT 0, 
    minimum_stock INTEGER DEFAULT 5, 
    expiry_date TEXT, 
    is_active INTEGER DEFAULT 1
)""")

        # Categories table (Dashboard needs this)
        cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)")
        
        # Vendors table
        cursor.execute("CREATE TABLE IF NOT EXISTS vendors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT)")

        # Bills table
        cursor.execute("""CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT, bill_id TEXT, bill_number INTEGER, 
            user_id INTEGER, customer_id INTEGER, bill_date TEXT, total_amount REAL, 
            discount_percent REAL, discount_amount REAL, payable_amount REAL, 
            received_amount REAL, balance_amount REAL, payment_method TEXT)""")
            
        # Bill Items table
        cursor.execute("""CREATE TABLE IF NOT EXISTS bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT, bill_id INTEGER, product_id INTEGER, 
            quantity INTEGER, unit_price REAL, discount_percent REAL, 
            discount_amount REAL, line_total REAL)""")

        # Held Bills table
        cursor.execute("CREATE TABLE IF NOT EXISTS held_bills (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, bill_data TEXT, held_at TEXT)")

        # Activity Logs table
        cursor.execute("""CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, 
            username TEXT, action TEXT, details TEXT, timestamp TEXT)""")

        # Insert Default Admin
        cursor.execute("""INSERT OR IGNORE INTO users (id, username, password, full_name, role, is_active) 
                       VALUES (1, 'admin', 'admin@123', 'admin', 'admin', 1)""")
        
        self.conn.commit()

    def log_activity(self, user_id, username, action, details):
        """Log user activity."""
        self.execute(
            """INSERT INTO activity_logs (user_id, username, action, details, timestamp)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, username, action, details, datetime.now().isoformat())
        )
# ==================== LOGIN SCREEN ====================
class LoginScreen(QWidget):
    """Login screen with authentication."""
    
    login_successful = pyqtSignal(dict)  # Emits user dict
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """Initialize login UI."""
        self.setWindowTitle('Fatima Tu Zahra Medical Centre Girote - Pharmacy Login')
        self.setGeometry(100, 100, 400, 500)
        
        # Set background with logo watermark
        pixmap = QPixmap('logo.jpg')
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation)
            palette = QPalette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_pixmap))
            self.setPalette(palette)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel('FATIMA TU ZAHRA MEDICAL CENTRE GIROTE')
        title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet('background-color: rgba(255, 255, 255, 200); padding: 10px; border-radius: 5px;')
        layout.addWidget(title)
        
        subtitle = QLabel('Pharmacy Management System')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet('background-color: rgba(255, 255, 255, 200); padding: 5px; border-radius: 5px;')
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Username
        username_label = QLabel('Username:')
        username_label.setStyleSheet('background-color: rgba(255, 255, 255, 200); padding: 5px; border-radius: 3px;')
        layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        self.username_input.returnPressed.connect(self.do_login)
        self.username_input.setStyleSheet('background-color: white; padding: 8px; border-radius: 3px;')
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel('Password:')
        password_label.setStyleSheet('background-color: rgba(255, 255, 255, 200); padding: 5px; border-radius: 3px;')
        layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.do_login)
        self.password_input.setStyleSheet('background-color: white; padding: 8px; border-radius: 3px;')
        layout.addWidget(self.password_input)
        
        layout.addSpacing(20)
        
        # Login button
        login_btn = QPushButton('Login')
        login_btn.setProperty('id', 'successBtn')
        login_btn.clicked.connect(self.do_login)
        login_btn.setStyleSheet('background-color: #27ae60; color: white; padding: 10px; font-weight: bold; border-radius: 3px;')
        layout.addWidget(login_btn)
        
        # Demo credentials hint
        hint = QLabel()
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet('background-color: rgba(255, 255, 255, 200); color: #333; font-size: 10px; padding: 5px; border-radius: 3px;')
        layout.addWidget(hint)
        
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet(THEME_STYLESHEET)
    
    def do_login(self):
        """Authenticate user."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, 'Input Error', 'Please enter username and password')
            return
        
        # Query user
        user = self.db.fetch_one(
            "SELECT * FROM users WHERE username = ? AND password = ? AND is_active = 1",
            (username, password)
        )
        
        if user:
            # Update last login
            self.db.execute(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (datetime.now().isoformat(), user['id'])
            )
            
            # Log activity
            self.db.log_activity(user['id'], user['username'], 'LOGIN', 'User logged in')
            
            # Emit signal
            self.login_successful.emit(dict(user))
            self.username_input.clear()
            self.password_input.clear()
        else:
            QMessageBox.critical(self, 'Login Failed', 'Invalid username or password')
            self.password_input.clear()

# ==================== DASHBOARD ====================
class DashboardWidget(QWidget):
    """Dashboard with KPI cards and recent transactions."""
    
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize dashboard UI."""
        layout = QVBoxLayout()
        
        # KPI Cards
        cards_layout = QHBoxLayout()
        
        self.kpi_cards = {}
        kpi_titles = ['Visited Customers', 'Purchase', 'Sale', 'Sale Return', 
                      'Customer Balance', 'Low Stock', 'Total Products', 'Revenue Today']
        
        for title in kpi_titles:
            card = self.create_kpi_card(title)
            cards_layout.addWidget(card)
            self.kpi_cards[title] = card
        
        layout.addLayout(cards_layout)
        layout.addSpacing(10)
        
        # Recent Transactions
        layout.addWidget(QLabel('Recent Transactions'))
        
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(['Bill ID', 'Date', 'Amount', 'Type', 'User'])
        self.transactions_table.setMaximumHeight(200)
        layout.addWidget(self.transactions_table)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_kpi_card(self, title):
        """Create KPI card."""
        frame = QFrame()
        frame.setObjectName('kpiCard')
        
        layout = QVBoxLayout()
        
        label = QLabel(title)
        label.setObjectName('kpiLabel')
        label.setFont(QFont('Arial', 10))
        
        value = QLabel('0')
        value.setObjectName('kpiValue')
        value.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        
        layout.addWidget(value)
        layout.addWidget(label)
        
        frame.setLayout(layout)
        frame.value_label = value
        
        return frame
    
    def load_data(self):
        """Load dashboard data."""
        # Visited Customers (count total bills as transactions)
        customers = self.db.fetch_one("SELECT COUNT(*) as count FROM bills")
        self.kpi_cards['Visited Customers'].value_label.setText(str(customers['count'] if customers else 0))
        
        # Today's sales - use proper SQLite date comparison
        today_sales = self.db.fetch_one(
            "SELECT SUM(total_amount) as sum FROM bills WHERE DATE(bill_date) = DATE('now', 'localtime')"
        )
        self.kpi_cards['Sale'].value_label.setText(f"Rs. {today_sales['sum'] or 0:.2f}")
        
        # Total products
        products = self.db.fetch_one("SELECT COUNT(*) as count FROM products WHERE is_active = 1")
        self.kpi_cards['Total Products'].value_label.setText(str(products['count'] if products else 0))
        
        # Low stock
        low_stock = self.db.fetch_one(
            "SELECT COUNT(*) as count FROM products WHERE quantity_stock <= minimum_stock AND is_active = 1"
        )
        self.kpi_cards['Low Stock'].value_label.setText(str(low_stock['count'] if low_stock else 0))
        
        # Recent transactions
        self.load_recent_transactions()
    
    def load_recent_transactions(self):
        """Load recent transactions."""
        self.transactions_table.setRowCount(0)
        
        bills = self.db.fetch_all(
            """SELECT b.bill_id, b.bill_date, b.total_amount, u.username 
               FROM bills b
               LEFT JOIN users u ON b.user_id = u.id
               ORDER BY b.bill_date DESC LIMIT 5"""
        )
        
        for row_idx, bill in enumerate(bills):
            self.transactions_table.insertRow(row_idx)
            self.transactions_table.setItem(row_idx, 0, QTableWidgetItem(bill['bill_id']))
            self.transactions_table.setItem(row_idx, 1, QTableWidgetItem(bill['bill_date'][:10]))
            self.transactions_table.setItem(row_idx, 2, QTableWidgetItem(f"Rs. {bill['total_amount']:.2f}"))
            self.transactions_table.setItem(row_idx, 3, QTableWidgetItem('Sale'))
            self.transactions_table.setItem(row_idx, 4, QTableWidgetItem(bill['username'] or 'N/A'))

# ==================== POS SCREEN ====================
class POSScreen(QWidget):
    """Advanced Point of Sale screen."""
    
    def __init__(self, db, current_user, main_app=None):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.main_app = main_app
        self.cart = []
        self.init_ui()
        self.load_products()
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            # If search field has focus, search for product
            if self.product_search.hasFocus():
                self.filter_products()
                # Focus on products table
                if self.products_table.rowCount() > 0:
                    self.products_table.setCurrentCell(0, 0)
                    self.products_table.setFocus()
            # If products table has focus, add selected product
            elif self.products_table.hasFocus():
                self.add_to_cart()
                self.product_search.setFocus()
                self.product_search.clear()
        else:
            super().keyPressEvent(event)
    
    def init_ui(self):
        """Initialize POS UI."""
        main_layout = QHBoxLayout()
        
        # Left side - Product selection
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)
        
        # Search
        search_lbl = QLabel('Search Product:')
        search_lbl.setStyleSheet('font-size: 13px; font-weight: bold;')
        left_layout.addWidget(search_lbl)
        self.product_search = QLineEdit()
        self.product_search.setPlaceholderText('Name or Serial Number')
        self.product_search.setMinimumHeight(35)
        self.product_search.setStyleSheet('font-size: 13px; padding: 8px; border: 2px solid #ddd; border-radius: 4px;')
        self.product_search.textChanged.connect(self.filter_products)
        left_layout.addWidget(self.product_search)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        headers = ['Serial #', 'Name', 'Price', 'Stock', 'Action']
        self.products_table.setHorizontalHeaderLabels(headers)
        self.products_table.setColumnWidth(0, 85)   # Serial #
        self.products_table.setColumnWidth(1, 155)  # Name
        self.products_table.setColumnWidth(2, 80)   # Price
        self.products_table.setColumnWidth(3, 75)   # Stock
        self.products_table.setColumnWidth(4, 85)   # Action
        self.products_table.setStyleSheet('font-size: 11px;')
        self.products_table.verticalHeader().setDefaultSectionSize(35)
        self.products_table.horizontalHeader().setStretchLastSection(False)
        left_layout.addWidget(self.products_table)
        
        main_layout.addLayout(left_layout, 1)
        
        # Right side - Cart
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)
        
        cart_lbl = QLabel('Shopping Cart')
        cart_lbl.setStyleSheet('font-size: 15px; font-weight: bold;')
        right_layout.addWidget(cart_lbl)
        
        # Cart table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(8)
        headers = ['Serial #', 'Name', 'Qty', 'Sale Price', 'Purchased Price', 'Discount %', 'Subtotal', 'Action']
        self.cart_table.setHorizontalHeaderLabels(headers)
        self.cart_table.setStyleSheet('font-size: 11px;')
        self.cart_table.verticalHeader().setDefaultSectionSize(40)
        # Hide horizontal scrollbar
        self.cart_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # Set optimized column widths for side-by-side visibility
        self.cart_table.setColumnWidth(0, 65)   # Serial #
        self.cart_table.setColumnWidth(1, 110)  # Name
        self.cart_table.setColumnWidth(2, 75)   # Qty - increased for better visibility
        self.cart_table.setColumnWidth(3, 75)   # Sale Price
        self.cart_table.setColumnWidth(4, 85)   # Purchased Price
        self.cart_table.setColumnWidth(5, 70)   # Discount %
        self.cart_table.setColumnWidth(6, 75)   # Subtotal
        self.cart_table.setColumnWidth(7, 70)   # Action
        self.cart_table.horizontalHeader().setStretchLastSection(False)
        right_layout.addWidget(self.cart_table)
        
        # Totals section - Horizontal layout at bottom
        totals_layout = QHBoxLayout()
        totals_layout.setSpacing(12)
        totals_layout.setContentsMargins(10, 10, 10, 10)
        
        # Subtotal
        subtotal_vbox = QVBoxLayout()
        subtotal_lbl = QLabel('Subtotal')
        subtotal_lbl.setStyleSheet('font-size: 11px; color: #666;')
        self.subtotal_label = QLabel('Rs. 0.00')
        self.subtotal_label.setStyleSheet('font-weight: bold; font-size: 18px; color: #2c5282;')
        subtotal_vbox.addWidget(subtotal_lbl)
        subtotal_vbox.addWidget(self.subtotal_label)
        subtotal_vbox.setSpacing(3)
        totals_layout.addLayout(subtotal_vbox)
        
        # Discount %
        discount_pct_vbox = QVBoxLayout()
        discount_pct_lbl = QLabel('Discount %')
        discount_pct_lbl.setStyleSheet('font-size: 11px; color: #666;')
        self.discount_percent = QDoubleSpinBox()
        self.discount_percent.setRange(0, 100)
        self.discount_percent.setSingleStep(0.5)
        self.discount_percent.setMaximumWidth(100)
        self.discount_percent.setStyleSheet('font-size: 13px; padding: 8px; border: 1px solid #bbb; border-radius: 3px;')
        self.discount_percent.valueChanged.connect(self.on_discount_percent_changed)
        discount_pct_vbox.addWidget(discount_pct_lbl)
        discount_pct_vbox.addWidget(self.discount_percent)
        discount_pct_vbox.setSpacing(3)
        totals_layout.addLayout(discount_pct_vbox)
        
        # Discount Amount (now editable)
        discount_amt_vbox = QVBoxLayout()
        discount_amt_lbl = QLabel('Discount Amount')
        discount_amt_lbl.setStyleSheet('font-size: 11px; color: #666;')
        self.discount_amount = QDoubleSpinBox()
        self.discount_amount.setRange(0, 999999)
        self.discount_amount.setSingleStep(1)
        self.discount_amount.setDecimals(2)
        self.discount_amount.setMaximumWidth(100)
        self.discount_amount.setStyleSheet('font-size: 13px; padding: 8px; border: 1px solid #bbb; border-radius: 3px;')
        self.discount_amount.valueChanged.connect(self.on_discount_amount_changed)
        discount_amt_vbox.addWidget(discount_amt_lbl)
        discount_amt_vbox.addWidget(self.discount_amount)
        discount_amt_vbox.setSpacing(3)
        totals_layout.addLayout(discount_amt_vbox)
        
        # Payable amount
        payable_vbox = QVBoxLayout()
        payable_lbl = QLabel('Payable Amount')
        payable_lbl.setStyleSheet('font-size: 11px; color: #666;')
        self.payable_label = QLabel('Rs. 0.00')
        self.payable_label.setStyleSheet('font-weight: bold; color: #276749; font-size: 20px;')
        payable_vbox.addWidget(payable_lbl)
        payable_vbox.addWidget(self.payable_label)
        payable_vbox.setSpacing(3)
        totals_layout.addLayout(payable_vbox)
        
        # Add stretch to center the items
        totals_layout.addStretch()
        
        totals_frame = QFrame()
        totals_frame.setLayout(totals_layout)
        totals_frame.setStyleSheet('background-color: #f9f9f9; border: 2px solid #ddd; border-radius: 5px;')
        totals_frame.setMinimumHeight(95)
        totals_frame.setMaximumHeight(110)
        right_layout.addWidget(totals_frame)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        hold_btn = QPushButton('Hold Bill')
        hold_btn.setMinimumHeight(42)
        hold_btn.setStyleSheet('font-size: 12px; font-weight: bold; padding: 8px;')
        hold_btn.clicked.connect(self.hold_bill)
        btn_layout.addWidget(hold_btn)
        
        clear_btn = QPushButton('Clear Cart')
        clear_btn.setProperty('id', 'dangerBtn')
        clear_btn.setMinimumHeight(42)
        clear_btn.setStyleSheet('font-size: 12px; font-weight: bold; padding: 8px;')
        clear_btn.clicked.connect(self.clear_cart)
        btn_layout.addWidget(clear_btn)
        
        save_btn = QPushButton('Pay & Save')
        save_btn.setProperty('id', 'successBtn')
        save_btn.setMinimumHeight(42)
        save_btn.setStyleSheet('font-size: 12px; font-weight: bold; padding: 8px;')
        save_btn.clicked.connect(self.save_bill)
        btn_layout.addWidget(save_btn)
        
        right_layout.addLayout(btn_layout)
        
        main_layout.addLayout(right_layout, 1)
        
        self.setLayout(main_layout)
    
    def load_products(self):
        """Load products from database."""
        self.update_products_table()
    
    def filter_products(self):
        """Filter products by search."""
        self.update_products_table()
    
    def update_products_table(self):
        """Update products table with current filter."""
        self.products_table.setRowCount(0)
        
        search_text = self.product_search.text().lower()
        
        products = self.db.fetch_all(
            """SELECT p.*, c.name as category_name 
               FROM products p
               LEFT JOIN categories c ON p.category_id = c.id
               WHERE p.is_active = 1"""
        )
        
        for row_idx, product in enumerate(products):
            # Filter by search
            if search_text and search_text not in product['serial_no'].lower() and search_text not in product['name'].lower():
                continue
            
            self.products_table.insertRow(self.products_table.rowCount())
            row = self.products_table.rowCount() - 1
            
            self.products_table.setItem(row, 0, QTableWidgetItem(product['serial_no']))
            self.products_table.setItem(row, 1, QTableWidgetItem(product['name']))
            self.products_table.setItem(row, 2, QTableWidgetItem(f"Rs. {product['sale_price']:.2f}"))
            self.products_table.setItem(row, 3, QTableWidgetItem(str(product['quantity_stock'])))
            
            # Add to cart button
            add_btn = QPushButton('Add')
            add_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 6px;')
            add_btn.clicked.connect(lambda checked, p=product: self.add_to_cart(p))
            self.products_table.setCellWidget(row, 4, add_btn)
    
    def add_to_cart(self, product):
        """Add product to cart."""
        # Check if already in cart
        for item in self.cart:
            if item['product_id'] == product['id']:
                item['quantity'] += 1
                self.update_cart_table()
                return
        
        # Add new item
        self.cart.append({
            'product_id': product['id'],
            'serial_no': product['serial_no'],
            'name': product['name'],
            'quantity': 1,
            'sale_price': product['sale_price'],
            'purchase_price': product['purchase_price'],
            'discount_percent': 0,
            'stock': product['quantity_stock']
        })
        
        self.update_cart_table()
    
    def update_cart_table(self):
        """Update cart table."""
        self.cart_table.setRowCount(len(self.cart))
        
        for row_idx, item in enumerate(self.cart):
            try:
                # Set row height for visibility
                self.cart_table.setRowHeight(row_idx, 45)
                
                # Get values with defaults for safety
                serial_no = item.get('serial_no', '')
                name = item.get('name', '')
                quantity = item.get('quantity', 1)
                sale_price = item.get('sale_price', 0)
                purchase_price = item.get('purchase_price', 0)
                discount_percent = item.get('discount_percent', 0)
                
                self.cart_table.setItem(row_idx, 0, QTableWidgetItem(str(serial_no)))
                self.cart_table.setItem(row_idx, 1, QTableWidgetItem(str(name)))
                
                qty = QSpinBox()
                qty.setValue(int(quantity))
                qty.setMinimum(1)
                qty.setMinimumWidth(65)
                qty.setMaximumWidth(75)
                qty.setStyleSheet('font-size: 13px; padding: 8px; font-weight: bold;')
                qty.valueChanged.connect(lambda v, r=row_idx: self.update_qty(r, v))
                self.cart_table.setCellWidget(row_idx, 2, qty)
                
                # Sale Price (read-only display)
                sale_price_item = QTableWidgetItem(f"Rs. {float(sale_price):.2f}")
                sale_price_item.setFlags(sale_price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.cart_table.setItem(row_idx, 3, sale_price_item)
                
                # Purchased Price (read-only display)
                purchase_price_item = QTableWidgetItem(f"Rs. {float(purchase_price):.2f}")
                purchase_price_item.setFlags(purchase_price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.cart_table.setItem(row_idx, 4, purchase_price_item)
                
                disc = QDoubleSpinBox()
                disc.setValue(float(discount_percent))
                disc.setRange(0, 100)
                disc.setSingleStep(0.5)
                disc.setMaximumWidth(70)
                disc.setStyleSheet('font-size: 12px; padding: 5px;')
                disc.valueChanged.connect(lambda v, r=row_idx: self.update_discount(r, v))
                self.cart_table.setCellWidget(row_idx, 5, disc)
                
                subtotal = quantity * sale_price * (1 - discount_percent / 100)
                self.cart_table.setItem(row_idx, 6, QTableWidgetItem(f"Rs. {subtotal:.2f}"))
                
                remove_btn = QPushButton('Remove')
                remove_btn.setProperty('id', 'dangerBtn')
                remove_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 6px;')
                remove_btn.clicked.connect(lambda checked, r=row_idx: self.remove_from_cart(r))
                self.cart_table.setCellWidget(row_idx, 7, remove_btn)
            except Exception as e:
                print(f"Error updating cart row {row_idx}: {e}")
                continue
        
        self.calculate_totals()
    
    def update_qty(self, row, value):
        """Update quantity in cart."""
        if row < len(self.cart):
            self.cart[row]['quantity'] = value
            self.update_cart_table()
    
    def update_discount(self, row, value):
        """Update discount percent."""
        if row < len(self.cart):
            self.cart[row]['discount_percent'] = value
            self.update_cart_table()
    
    def remove_from_cart(self, row):
        """Remove item from cart."""
        if row < len(self.cart):
            self.cart.pop(row)
            self.update_cart_table()
    
    def calculate_totals(self):
        """Calculate and display totals."""
        subtotal = sum(item['quantity'] * item['sale_price'] * (1 - item['discount_percent'] / 100) 
                      for item in self.cart)
        
        discount_amount = self.discount_amount.value()
        discount_percent = self.discount_percent.value()
        payable = subtotal - discount_amount
        
        self.subtotal_label.setText(f"Rs. {subtotal:.2f}")
        self.payable_label.setText(f"Rs. {payable:.2f}")
    
    def on_discount_percent_changed(self, value):
        """Handle discount percentage change and calculate discount amount."""
        # Block signals to avoid recursion
        self.discount_amount.blockSignals(True)
        
        subtotal = sum(item['quantity'] * item['sale_price'] * (1 - item['discount_percent'] / 100) 
                      for item in self.cart)
        
        discount_amount = subtotal * value / 100
        self.discount_amount.setValue(discount_amount)
        
        self.discount_amount.blockSignals(False)
        self.calculate_totals()
    
    def on_discount_amount_changed(self, value):
        """Handle discount amount change and calculate discount percentage."""
        # Block signals to avoid recursion
        self.discount_percent.blockSignals(True)
        
        subtotal = sum(item['quantity'] * item['sale_price'] * (1 - item['discount_percent'] / 100) 
                      for item in self.cart)
        
        if subtotal > 0:
            discount_percent = (value / subtotal) * 100
            self.discount_percent.setValue(discount_percent)
        else:
            self.discount_percent.setValue(0)
        
        self.discount_percent.blockSignals(False)
        self.calculate_totals()
    
    def clear_cart(self):
        """Clear shopping cart."""
        self.cart.clear()
        self.update_cart_table()
        self.discount_percent.setValue(0)
        self.discount_amount.setValue(0)
    
    def load_cart_to_ui(self):
        """Load cart items to UI after reopening held bill."""
        try:
            self.update_cart_table()
            self.calculate_totals()
            # Ensure all rows are visible by scrolling to top
            self.cart_table.scrollToTop()
            # Resize columns to content
            self.cart_table.resizeColumnsToContents()
        except Exception as e:
            print(f"Error loading cart to UI: {e}")
    
    def hold_bill(self):
        """Hold current bill."""
        if not self.cart:
            QMessageBox.warning(self, 'Empty Cart', 'Please add items before holding')
            return
        
        # Serialize cart as JSON
        bill_data = json.dumps(self.cart)
        
        self.db.execute(
            """INSERT INTO held_bills (user_id, bill_data, held_at)
               VALUES (?, ?, ?)""",
            (self.current_user['id'], bill_data, datetime.now().isoformat())
        )
        
        self.db.log_activity(self.current_user['id'], self.current_user['username'], 
                           'HOLD_BILL', f'Held bill with {len(self.cart)} items')
        
        QMessageBox.information(self, 'Success', f'Bill held with {len(self.cart)} items')
        self.clear_cart()
    
    def save_bill(self):
        """Save bill to database."""
        try:
            if not self.cart:
                QMessageBox.warning(self, 'Empty Cart', 'Please add items before saving')
                return
            
            payable = float(self.payable_label.text().replace('Rs. ', ''))
            
            # Generate bill ID with timestamp for uniqueness
            import time
            timestamp = int(time.time())  # seconds for uniqueness
            bill_id = f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            bill_number = self.db.get_next_bill_number()
            
            subtotal = float(self.subtotal_label.text().replace('Rs. ', ''))
            discount_amt = float(self.discount_amount.value())
            discount_pct = float(self.discount_percent.value())
            
            # Create bill with all required fields
            try:
                print(f"Saving bill with values: bill_id={bill_id}, bill_number={int(bill_number)}, user_id={int(self.current_user['id'])}")
                cursor = self.db.execute(
                    """INSERT INTO bills (bill_id, bill_number, user_id, customer_id, bill_date,
                                         total_amount, discount_percent, discount_amount, payable_amount,
                                         received_amount, balance_amount, payment_method)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (bill_id, int(bill_number), int(self.current_user['id']), None, datetime.now().isoformat(),
                     float(subtotal), float(discount_pct), float(discount_amt), float(payable), float(payable), 0.0, 'CASH')
                )
                bill_db_id = cursor.lastrowid
                print(f'Bill {bill_id} created with DB ID {bill_db_id}')
            except Exception as e:
                print(f'Error creating bill: {e}')
                raise
            
            # Add bill items and update inventory
            try:
                for item in self.cart:
                    qty = int(item['quantity'])
                    unit_price = float(item['sale_price'])
                    disc_pct = float(item['discount_percent'])
                    disc_amt = float(qty * unit_price * disc_pct / 100)
                    line_total = float(qty * unit_price * (1 - disc_pct / 100))
                    
                    self.db.execute(
                        """INSERT INTO bill_items (bill_id, product_id, quantity, unit_price, 
                                                  discount_percent, discount_amount, line_total)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (int(bill_db_id), int(item['product_id']), float(qty), float(unit_price),
                         float(disc_pct), float(disc_amt), float(line_total))
                    )
                    
                    # Update product quantity
                    self.db.execute(
                        "UPDATE products SET quantity_stock = quantity_stock - ? WHERE id = ?",
                        (int(qty), int(item['product_id']))
                    )
            except Exception as e:
                print(f'Error adding bill items: {e}')
                raise
            
            # Log activity
            self.db.log_activity(self.current_user['id'], self.current_user['username'],
                               'SALE', f'Bill {bill_id}: Rs. {payable:.2f}')
            
            # Commit all changes to database
            self.db.conn.commit()
            
            # Print receipt
            self.print_receipt(bill_id, payable)
            
            QMessageBox.information(self, 'Success', f'Bill saved successfully!\nBill ID: {bill_id}')
            self.clear_cart()
            
            # Update dashboard if available - with small delay to ensure commit
            if self.main_app and 'dashboard' in self.main_app.modules:
                import time
                time.sleep(0.2)  # Small delay to ensure database commit
                self.main_app.modules['dashboard'].load_data()
        except Exception as e:
            print(f'Detailed error: {str(e)}')
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, 'Error', f'Failed to save bill: {str(e)}')
            print(f'Error in save_bill: {e}')
            import traceback
            traceback.print_exc()
    
    def print_receipt(self, bill_id, payable):
        """Professional 80mm receipt: Fixed for Bixolon hardware resolution."""
        logo_path = resource_path('logo.jpg')
        
        # Calculate values
        try:
            subtotal_val = float(self.subtotal_label.text().replace('Rs. ', '').replace(',', ''))
        except:
            subtotal_val = 0.0
            
        discount_amt = self.discount_amount.value()
        discount_pct = self.discount_percent.value()

        # HTML with optimized thermal padding (4px)
        receipt_html = f"""
        <html>
        <head>
            <style>
                @page {{ margin: 0; }}
                body {{ 
                    font-family: 'Arial', sans-serif; 
                    width: auto; 
                    margin: 0; 
                    padding: 0; 
                    font-size: 9pt; 
                }}
                .header {{ text-align: center;
                  margin-bottom: 6px; }}
                .hospital-name {{ font-size: 14pt; font-weight: bold; }}
                
                table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                     
                }}
                th {{ 
                border-bottom: 1px solid black;
                    font-size: 9pt; 
                    text-align: left; 
                }}
                td {{
                    padding: 4px 0; 
                    font-size: 9pt;
                }}
                
                .text-right {{ text-align: right; }}
                .grand-total {{ 
                    font-size: 11pt; 
                    font-weight: bold; 
                    border-top: 2px solid #000; 
                     
                }}
                .footer {{ text-align: center; margin-top: 6px; font-size: 8pt; }}
            </style>
        </head>
        <body>
            <div class="header">
                <center><img src="{logo_path}" width="80"></center>
                <div class="hospital-name">FATIMA TU ZAHRA<br>MEDICAL CENTRE</div>
                <div style="font-size: 8pt;">Girote, Khushab | 0306-5111806</div>
            </div>

            <div style="font-size: 8pt;">
                <b>BILL ID:</b> {bill_id}<br>
                <b>DATE:</b> {datetime.now().strftime('%d-%m-%Y %I:%M %p')}
            </div>

            <table>
                <thead>
                    <tr>
                        <th width="55">ITEM</th>
                        <th width="20" class="text-right">QTY</th>
                        <th width="35" class="text-right">TOTAL</th>
                    </tr>
                </thead>
                <tbody>
        """

        for item in self.cart:
            receipt_html += f"""
                    <tr>
                        <td style="font-weight: bold;">{item['name']}</td>
                        <td class="text-right">{item['quantity']}</td>
                        <td class="text-right">{(item['quantity'] * item['sale_price']):,.2f}</td>
                    </tr>
            """

        receipt_html += f"""
                </tbody>
            </table>
            <div style="border-top: 1px solid #000; ;"></div>
            <table style="width: 100%;">
                <tr><td>Subtotal:</td><td class="text-right">{subtotal_val:,.2f}</td></tr>
                <tr class="grand-total"><td><b>PAYABLE:</b></td><td class="text-right"><b>Rs {payable:,.2f}</b></td></tr>
            </table>
            <div class="footer">THANK YOU FOR YOUR VISIT!</div>
        </body>
        </html>
        """

       # 1. Setup Document
        doc = QTextDocument()
        doc.setHtml(receipt_html)
        
        

        # 2. Setup Printer with high-res specs
        printer = QPrinter(QPrinter.PrinterMode.PrinterResolution)
        printer.setResolution(203) # Bixolon native DPI
        page_size = QPageSize(QSizeF(80, 297), QPageSize.Unit.Millimeter)
        printer.setPageSize(page_size)
    
        # 4. Remove all padding/margins
        printer.setFullPage(True)
        printer.setPageMargins(QMarginsF(0, 0, 0, 0), QPageLayout.Unit.Millimeter)

        # 5. Dynamic Height Calculation
        # (doc_height / resolution) * 25.4mm per inch
        height_mm = (doc.size().height() * 25.4 / 203) + 10
        printer.pageRect(QPrinter.Unit.DevicePixel)


        # 6. Execute Print
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            # Force the painter to scale to the full paper width
            doc.print(printer)
# ==================== INVENTORY ====================
class InventoryWidget(QWidget):
    """Inventory management."""
    
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        
        if current_user['role'] != 'admin':
            layout = QVBoxLayout()
            label = QLabel('Access Denied - Admin Only')
            layout.addWidget(label)
            self.setLayout(layout)
            return
        
        self.init_ui()
        self.load_inventory()
    
    def init_ui(self):
        """Initialize inventory UI."""
        layout = QVBoxLayout()
        
        # Search
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel('Search:'))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Name or Serial Number')
        self.search_input.textChanged.connect(self.filter_inventory)
        search_layout.addWidget(self.search_input)
        
        add_btn = QPushButton('Add Product')
        add_btn.setProperty('id', 'successBtn')
        add_btn.clicked.connect(self.add_product)
        search_layout.addWidget(add_btn)
        
        layout.addLayout(search_layout)
        
        # Table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(10)
        headers = ['Serial #', 'Name', 'Category', 'Purchase Price', 'Sale Price', 
                   'Stock', 'Min Stock', 'Expiry', 'Action Edit', 'Action Delete']
        self.inventory_table.setHorizontalHeaderLabels(headers)
        layout.addWidget(self.inventory_table)
        
        self.setLayout(layout)
    
    def load_inventory(self):
        """Load inventory."""
        self.filter_inventory()
    
    def filter_inventory(self):
        """Filter inventory by search."""
        self.inventory_table.setRowCount(0)
        
        search_text = self.search_input.text().lower()
        
        products = self.db.fetch_all(
            """SELECT p.*, c.name as category_name FROM products p
               LEFT JOIN categories c ON p.category_id = c.id
               WHERE p.is_active = 1"""
        )
        
        for product in products:
            if search_text and search_text not in product['serial_no'].lower() and search_text not in product['name'].lower():
                continue
            
            row = self.inventory_table.rowCount()
            self.inventory_table.insertRow(row)
            self.inventory_table.setRowHeight(row, 40)
            
            self.inventory_table.setItem(row, 0, QTableWidgetItem(product['serial_no']))
            self.inventory_table.setItem(row, 1, QTableWidgetItem(product['name']))
            self.inventory_table.setItem(row, 2, QTableWidgetItem(product['category_name'] or 'N/A'))
            self.inventory_table.setItem(row, 3, QTableWidgetItem(f"Rs. {product['purchase_price']:.2f}"))
            self.inventory_table.setItem(row, 4, QTableWidgetItem(f"Rs. {product['sale_price']:.2f}"))
            
            # Stock with color coding
            stock_item = QTableWidgetItem(str(product['quantity_stock']))
            if product['quantity_stock'] <= product['minimum_stock']:
                stock_item.setBackground(QColor('#c53030'))
                stock_item.setForeground(QColor('white'))
            elif product['quantity_stock'] < 20:
                stock_item.setBackground(QColor('#f6ad55'))
            else:
                stock_item.setBackground(QColor('#276749'))
                stock_item.setForeground(QColor('white'))
            self.inventory_table.setItem(row, 5, stock_item)
            
            self.inventory_table.setItem(row, 6, QTableWidgetItem(str(product['minimum_stock'])))
            self.inventory_table.setItem(row, 7, QTableWidgetItem(product['expiry_date'][:10]))
            
            edit_btn = QPushButton('Edit')
            edit_btn.setProperty('id', 'warningBtn')
            edit_btn.setMinimumHeight(35)
            edit_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 4px 8px; border: none;')
            edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
            self.inventory_table.setCellWidget(row, 8, edit_btn)
            
            delete_btn = QPushButton('Delete')
            delete_btn.setProperty('id', 'dangerBtn')
            delete_btn.setMinimumHeight(35)
            delete_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 4px 8px; border: none;')
            delete_btn.clicked.connect(lambda checked, p=product: self.delete_product(p))
            self.inventory_table.setCellWidget(row, 9, delete_btn)
    
    def add_product(self):
        """Add new product."""
        dialog = ProductDialog(self.db, None, self)
        if dialog.exec():
            self.load_inventory()
    
    def edit_product(self, product):
        """Edit product."""
        dialog = ProductDialog(self.db, dict(product), self)
        if dialog.exec():
            self.load_inventory()
    
    def delete_product(self, product):
        """Delete product."""
        reply = QMessageBox.question(self, 'Delete', f'Delete {product["name"]}?')
        if reply == QMessageBox.StandardButton.Yes:
            self.db.execute("UPDATE products SET is_active = 0 WHERE id = ?", (product['id'],))
            self.db.log_activity(self.current_user['id'], self.current_user['username'],
                               'DELETE_PRODUCT', f'Deleted product: {product["name"]}')
            self.load_inventory()

# ==================== PRODUCT DIALOG ====================
class ProductDialog(QDialog):
    """Product add/edit dialog."""
    
    def __init__(self, db, product=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.product = product
        self.setWindowTitle('Product' if not product else f'Edit - {product["name"]}')
        self.setGeometry(100, 100, 500, 400)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog."""
        layout = QFormLayout()
        
        # Serial Number
        self.serial_input = QLineEdit()
        if self.product:
            self.serial_input.setText(self.product['serial_no'])
            self.serial_input.setReadOnly(True)
        layout.addRow('Serial Number:', self.serial_input)
        
        # Name
        self.name_input = QLineEdit()
        if self.product:
            self.name_input.setText(self.product['name'])
        layout.addRow('Product Name:', self.name_input)
        
        # Category
        self.category_combo = QComboBox()
        self.category_combo.addItem('-- Select Category --', None)
        categories = self.db.fetch_all("SELECT id, name FROM categories ORDER BY name")
        for cat in categories:
            self.category_combo.addItem(cat['name'], cat['id'])
        if self.product and self.product['category_id']:
            index = self.category_combo.findData(self.product['category_id'])
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        layout.addRow('Category:', self.category_combo)
        
        # Vendor
        self.vendor_combo = QComboBox()
        self.vendor_combo.addItem('-- Select Vendor --', None)
        vendors = self.db.fetch_all("SELECT id, name FROM vendors ORDER BY name")
        for ven in vendors:
            self.vendor_combo.addItem(ven['name'], ven['id'])
        if self.product and self.product['vendor_id']:
            index = self.vendor_combo.findData(self.product['vendor_id'])
            if index >= 0:
                self.vendor_combo.setCurrentIndex(index)
        layout.addRow('Vendor:', self.vendor_combo)
        
        # Purchase Price
        self.purchase_price = QDoubleSpinBox()
        self.purchase_price.setRange(0, 999999)
        self.purchase_price.setDecimals(2)
        if self.product:
            self.purchase_price.setValue(self.product['purchase_price'])
        layout.addRow('Purchase Price:', self.purchase_price)
        
        # Sale Price
        self.sale_price = QDoubleSpinBox()
        self.sale_price.setRange(0, 999999)
        self.sale_price.setDecimals(2)
        if self.product:
            self.sale_price.setValue(self.product['sale_price'])
        layout.addRow('Sale Price:', self.sale_price)
        
        # Quantity
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 99999)
        if self.product:
            self.quantity_input.setValue(self.product['quantity_stock'])
        layout.addRow('Quantity:', self.quantity_input)
        
        # Minimum Stock
        self.minimum_stock = QSpinBox()
        self.minimum_stock.setRange(0, 99999)
        if self.product:
            self.minimum_stock.setValue(self.product['minimum_stock'])
        layout.addRow('Minimum Stock:', self.minimum_stock)
        
        # Expiry Date
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        if self.product:
            self.expiry_date.setDate(QDate.fromString(self.product['expiry_date'], 'yyyy-MM-dd'))
        else:
            self.expiry_date.setDate(QDate.currentDate().addMonths(6))
        layout.addRow('Expiry Date:', self.expiry_date)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton('💾 Save')
        save_btn.setProperty('id', 'successBtn')
        save_btn.setStyleSheet('font-size: 12px; font-weight: bold;')
        save_btn.clicked.connect(self.save)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton('❌ Cancel')
        cancel_btn.setStyleSheet('font-size: 12px; font-weight: bold;')
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
        self.setStyleSheet(THEME_STYLESHEET)
    
    def save(self):
        """Save product."""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, 'Validation', 'Product name is required')
            return
        
        try:
            if self.product:
                # Update existing product
                self.db.execute(
                    """UPDATE products SET name=?, category_id=?, vendor_id=?,
                       purchase_price=?, sale_price=?, quantity_stock=?,
                       minimum_stock=?, expiry_date=? WHERE id=?""",
                    (self.name_input.text(), 
                     self.category_combo.currentData() if self.category_combo.currentData() else None,
                     self.vendor_combo.currentData() if self.vendor_combo.currentData() else None,
                     self.purchase_price.value(),
                     self.sale_price.value(), 
                     self.quantity_input.value(),
                     self.minimum_stock.value(), 
                     self.expiry_date.date().toString('yyyy-MM-dd'),
                     self.product['id'])
                )
                QMessageBox.information(self, 'Success', 'Product updated successfully')
            else:
                # Insert new product
                serial = self.serial_input.text().strip()
                if not serial:
                    QMessageBox.warning(self, 'Validation', 'Serial number is required')
                    return
                
                self.db.execute(
                    """INSERT INTO products (serial_no, name, category_id, vendor_id,
                       purchase_price, sale_price, quantity_stock, minimum_stock, expiry_date)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (serial, self.name_input.text(), 
                     self.category_combo.currentData() if self.category_combo.currentData() else None,
                     self.vendor_combo.currentData() if self.vendor_combo.currentData() else None,
                     self.purchase_price.value(),
                     self.sale_price.value(), 
                     self.quantity_input.value(),
                     self.minimum_stock.value(), 
                     self.expiry_date.date().toString('yyyy-MM-dd'))
                )
                QMessageBox.information(self, 'Success', 'Product added successfully')
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save product: {str(e)}')

# ==================== CATEGORIES MANAGEMENT ====================
class CategoriesWidget(QWidget):
    """Categories management widget."""
    
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.init_ui()
        self.load_categories()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        header_label = QLabel('Category Management')
        header_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        header.addWidget(header_label)
        
        add_btn = QPushButton('➕ Add Category')
        add_btn.setProperty('id', 'successBtn')
        add_btn.setMinimumHeight(40)
        add_btn.clicked.connect(self.add_category)
        header.addStretch()
        header.addWidget(add_btn)
        
        layout.addLayout(header)
        
        # Categories table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Name', 'Description', 'Actions'])
        self.table.setStyleSheet('font-size: 12px;')
        self.table.verticalHeader().setDefaultSectionSize(40)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_categories(self):
        """Load categories from database."""
        self.table.setRowCount(0)
        categories = self.db.fetch_all("SELECT id, name, description FROM categories ORDER BY name")
        
        for idx, cat in enumerate(categories):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(cat['name']))
            self.table.setItem(idx, 1, QTableWidgetItem(cat['description'] or ''))
            
            # Actions
            btn_layout = QHBoxLayout()
            
            edit_btn = QPushButton('Edit')
            edit_btn.setMinimumHeight(35)
            edit_btn.setMinimumWidth(70)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #d69e2e;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 6px 12px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #b8860b;
                }
                QPushButton:pressed {
                    background-color: #92670f;
                }
            """)
            edit_btn.clicked.connect(lambda checked, c=cat: self.edit_category(c))
            btn_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton('Delete')
            delete_btn.setMinimumHeight(35)
            delete_btn.setMinimumWidth(70)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #c53030;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 6px 12px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #a02020;
                }
                QPushButton:pressed {
                    background-color: #7a1818;
                }
            """)
            delete_btn.clicked.connect(lambda checked, c=cat: self.delete_category(c))
            btn_layout.addWidget(delete_btn)
            
            widget = QWidget()
            widget.setLayout(btn_layout)
            self.table.setCellWidget(idx, 2, widget)
    
    def add_category(self):
        """Add new category."""
        dialog = QDialog(self)
        dialog.setWindowTitle('Add Category')
        dialog.setGeometry(100, 100, 400, 200)
        
        layout = QFormLayout()
        
        name_input = QLineEdit()
        desc_input = QTextEdit()
        
        layout.addRow('Category Name:', name_input)
        layout.addRow('Description:', desc_input)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton('💾 Save')
        save_btn.setProperty('id', 'successBtn')
        save_btn.setStyleSheet('font-size: 12px; font-weight: bold;')
        cancel_btn = QPushButton('❌ Cancel')
        cancel_btn.setStyleSheet('font-size: 12px; font-weight: bold;')
        
        def save_category():
            if not name_input.text():
                QMessageBox.warning(self, 'Validation', 'Please enter category name')
                return
            try:
                self.db.execute(
                    "INSERT INTO categories (name, description) VALUES (?, ?)",
                    (name_input.text(), desc_input.toPlainText())
                )
                self.db.log_activity(self.current_user['id'], self.current_user['username'],
                                   'ADD_CATEGORY', f'Added category: {name_input.text()}')
                QMessageBox.information(self, 'Success', f'Category {name_input.text()} added successfully!')
                dialog.close()
                self.load_categories()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to add category: {str(e)}')
        
        save_btn.clicked.connect(save_category)
        cancel_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def edit_category(self, category):
        """Edit category."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Edit {category["name"]}')
        dialog.setGeometry(100, 100, 400, 200)
        
        layout = QFormLayout()
        
        name_input = QLineEdit()
        name_input.setText(category['name'])
        layout.addRow('Name:', name_input)
        
        desc_input = QTextEdit()
        desc_input.setText(category['description'] or '')
        layout.addRow('Description:', desc_input)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton('Save')
        cancel_btn = QPushButton('Cancel')
        
        def save_changes():
            try:
                self.db.execute(
                    "UPDATE categories SET name = ?, description = ? WHERE id = ?",
                    (name_input.text(), desc_input.toPlainText(), category['id'])
                )
                self.db.log_activity(self.current_user['id'], self.current_user['username'],
                                   'EDIT_CATEGORY', f'Updated category: {name_input.text()}')
                QMessageBox.information(self, 'Success', 'Category updated successfully!')
                dialog.close()
                self.load_categories()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update category: {str(e)}')
        
        save_btn.clicked.connect(save_changes)
        cancel_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def delete_category(self, category):
        """Delete category."""
        reply = QMessageBox.question(self, 'Confirm', f'Delete category {category["name"]}?')
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.execute("DELETE FROM categories WHERE id = ?", (category['id'],))
                self.db.log_activity(self.current_user['id'], self.current_user['username'],
                                   'DELETE_CATEGORY', f'Deleted category: {category["name"]}')
                QMessageBox.information(self, 'Success', 'Category deleted successfully!')
                self.load_categories()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete category: {str(e)}')

# ==================== VENDORS MANAGEMENT ====================
class VendorsWidget(QWidget):
    """Vendors management widget."""
    
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.init_ui()
        self.load_vendors()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        header_label = QLabel('Vendor Management')
        header_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        header.addWidget(header_label)
        
        add_btn = QPushButton('➕ Add Vendor')
        add_btn.setProperty('id', 'successBtn')
        add_btn.setMinimumHeight(40)
        add_btn.clicked.connect(self.add_vendor)
        header.addStretch()
        header.addWidget(add_btn)
        
        layout.addLayout(header)
        
        # Vendors table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Name', 'Phone', 'Email', 'Actions'])
        self.table.setStyleSheet('font-size: 12px;')
        self.table.verticalHeader().setDefaultSectionSize(40)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_vendors(self):
        """Load vendors from database."""
        self.table.setRowCount(0)
        vendors = self.db.fetch_all("SELECT id, name, phone, email FROM vendors ORDER BY name")
        
        for idx, vendor in enumerate(vendors):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(vendor['name']))
            self.table.setItem(idx, 1, QTableWidgetItem(vendor['phone'] or ''))
            self.table.setItem(idx, 2, QTableWidgetItem(vendor['email'] or ''))
            
            # Actions
            btn_layout = QHBoxLayout()
            
            edit_btn = QPushButton('Edit')
            edit_btn.setMinimumHeight(35)
            edit_btn.setMinimumWidth(70)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #d69e2e;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 6px 12px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #b8860b;
                }
                QPushButton:pressed {
                    background-color: #92670f;
                }
            """)
            edit_btn.clicked.connect(lambda checked, v=vendor: self.edit_vendor(v))
            btn_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton('Delete')
            delete_btn.setMinimumHeight(35)
            delete_btn.setMinimumWidth(70)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #c53030;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 6px 12px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #a02020;
                }
                QPushButton:pressed {
                    background-color: #7a1818;
                }
            """)
            delete_btn.clicked.connect(lambda checked, v=vendor: self.delete_vendor(v))
            btn_layout.addWidget(delete_btn)
            
            widget = QWidget()
            widget.setLayout(btn_layout)
            self.table.setCellWidget(idx, 3, widget)
    
    def add_vendor(self):
        """Add new vendor."""
        dialog = QDialog(self)
        dialog.setWindowTitle('Add Vendor')
        dialog.setGeometry(100, 100, 400, 300)
        
        layout = QFormLayout()
        
        name_input = QLineEdit()
        phone_input = QLineEdit()
        email_input = QLineEdit()
        
        layout.addRow('Vendor Name:', name_input)
        layout.addRow('Phone:', phone_input)
        layout.addRow('Email:', email_input)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton('Save')
        cancel_btn = QPushButton('Cancel')
        
        def save_vendor():
            if not name_input.text():
                QMessageBox.warning(self, 'Validation', 'Please enter vendor name')
                return
            try:
                self.db.execute(
                    "INSERT INTO vendors (name, phone, email) VALUES (?, ?, ?)",
                    (name_input.text(), phone_input.text(), email_input.text())
                )
                self.db.log_activity(self.current_user['id'], self.current_user['username'],
                                   'ADD_VENDOR', f'Added vendor: {name_input.text()}')
                QMessageBox.information(self, 'Success', f'Vendor {name_input.text()} added successfully!')
                dialog.close()
                self.load_vendors()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to add vendor: {str(e)}')
        
        save_btn.clicked.connect(save_vendor)
        cancel_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def edit_vendor(self, vendor):
        """Edit vendor."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Edit {vendor["name"]}')
        dialog.setGeometry(100, 100, 400, 300)
        
        layout = QFormLayout()
        
        name_input = QLineEdit()
        name_input.setText(vendor['name'])
        phone_input = QLineEdit()
        phone_input.setText(vendor['phone'] or '')
        email_input = QLineEdit()
        email_input.setText(vendor['email'] or '')
        
        layout.addRow('Vendor Name:', name_input)
        layout.addRow('Phone:', phone_input)
        layout.addRow('Email:', email_input)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton('Save')
        cancel_btn = QPushButton('Cancel')
        
        def save_changes():
            try:
                self.db.execute(
                    "UPDATE vendors SET name = ?, phone = ?, email = ? WHERE id = ?",
                    (name_input.text(), phone_input.text(), email_input.text(), vendor['id'])
                )
                self.db.log_activity(self.current_user['id'], self.current_user['username'],
                                   'EDIT_VENDOR', f'Updated vendor: {name_input.text()}')
                QMessageBox.information(self, 'Success', 'Vendor updated successfully!')
                dialog.close()
                self.load_vendors()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update vendor: {str(e)}')
        
        save_btn.clicked.connect(save_changes)
        cancel_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def delete_vendor(self, vendor):
        """Delete vendor."""
        reply = QMessageBox.question(self, 'Confirm', f'Delete vendor {vendor["name"]}?')
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.execute("DELETE FROM vendors WHERE id = ?", (vendor['id'],))
                self.db.log_activity(self.current_user['id'], self.current_user['username'],
                                   'DELETE_VENDOR', f'Deleted vendor: {vendor["name"]}')
                QMessageBox.information(self, 'Success', 'Vendor deleted successfully!')
                self.load_vendors()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete vendor: {str(e)}')

# ==================== LOW STOCK MANAGEMENT ====================
class LowStockWidget(QWidget):
    """Low stock management widget."""
    
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.init_ui()
        self.load_low_stock()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        header_label = QLabel('Low Stock Medicines')
        header_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        header.addWidget(header_label)
        
        refresh_btn = QPushButton('🔄 Refresh')
        refresh_btn.setMinimumHeight(40)
        refresh_btn.clicked.connect(self.load_low_stock)
        header.addStretch()
        header.addWidget(refresh_btn)
        
        layout.addLayout(header)
        
        # Low stock table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Name', 'Current Stock', 'Min Stock', 'Stock Status', 'Create Demand', 'View Notes'])
        self.table.setStyleSheet('font-size: 12px;')
        self.table.verticalHeader().setDefaultSectionSize(40)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_low_stock(self):
        """Load low stock medicines from database."""
        self.table.setRowCount(0)
        
        # Get all products where quantity_stock <= minimum_stock
        products = self.db.fetch_all(
            """SELECT id, name, quantity_stock, minimum_stock FROM products 
               WHERE quantity_stock <= minimum_stock AND is_active = 1
               ORDER BY quantity_stock ASC"""
        )
        
        for idx, product in enumerate(products):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(product['name']))
            self.table.setItem(idx, 1, QTableWidgetItem(str(product['quantity_stock'])))
            self.table.setItem(idx, 2, QTableWidgetItem(str(product['minimum_stock'])))
            
            # Status with color coding
            status_item = QTableWidgetItem('CRITICAL' if product['quantity_stock'] == 0 else 'LOW')
            if product['quantity_stock'] == 0:
                status_item.setBackground(QColor('#c53030'))
                status_item.setForeground(QColor('white'))
            else:
                status_item.setBackground(QColor('#f6ad55'))
            self.table.setItem(idx, 3, status_item)
            
            # Create demand button
            demand_btn = QPushButton('➕ Create Demand')
            demand_btn.setMinimumHeight(35)
            demand_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 5px;')
            demand_btn.clicked.connect(lambda checked, p=product: self.create_demand(p))
            self.table.setCellWidget(idx, 4, demand_btn)
            
            # View notes button
            notes_btn = QPushButton('📝 Notes')
            notes_btn.setMinimumHeight(35)
            notes_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 5px;')
            notes_btn.clicked.connect(lambda checked, p=product: self.view_notes(p))
            self.table.setCellWidget(idx, 5, notes_btn)
    
    def create_demand(self, product):
        """Create demand note for low stock medicine."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Create Demand - {product["name"]}')
        dialog.setGeometry(100, 100, 500, 300)
        
        layout = QFormLayout()
        
        quantity_input = QSpinBox()
        quantity_input.setMinimum(1)
        quantity_input.setValue(product['minimum_stock'] * 2)  # Default: 2x minimum stock
        
        notes_input = QTextEdit()
        notes_input.setPlaceholderText('Enter any specific notes or requirements...')
        
        layout.addRow('Required Quantity:', quantity_input)
        layout.addRow('Notes:', notes_input)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton('Create Demand')
        cancel_btn = QPushButton('Cancel')
        
        def save_demand():
            try:
                self.db.execute(
                    """INSERT INTO demand_notes (product_id, required_quantity, notes, created_by, status)
                       VALUES (?, ?, ?, ?, ?)""",
                    (product['id'], quantity_input.value(), notes_input.toPlainText(),
                     self.current_user['id'], 'PENDING')
                )
                self.db.log_activity(self.current_user['id'], self.current_user['username'],
                                   'CREATE_DEMAND', f'Created demand for: {product["name"]}, Qty: {quantity_input.value()}')
                QMessageBox.information(self, 'Success', 'Demand note created successfully!')
                dialog.close()
                self.load_low_stock()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to create demand: {str(e)}')
        
        save_btn.clicked.connect(save_demand)
        cancel_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def view_notes(self, product):
        """View demand notes for a product."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Demand Notes - {product["name"]}')
        dialog.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Notes table
        notes_table = QTableWidget()
        notes_table.setColumnCount(5)
        notes_table.setHorizontalHeaderLabels(['Date', 'Required Qty', 'Status', 'Notes', 'Actions'])
        notes_table.setStyleSheet('font-size: 12px;')
        
        demands = self.db.fetch_all(
            """SELECT id, created_at, required_quantity, status, notes FROM demand_notes 
               WHERE product_id = ? ORDER BY created_at DESC""",
            (product['id'],)
        )
        
        for idx, demand in enumerate(demands):
            notes_table.insertRow(idx)
            notes_table.setItem(idx, 0, QTableWidgetItem(demand['created_at'][:10]))
            notes_table.setItem(idx, 1, QTableWidgetItem(str(demand['required_quantity'])))
            
            status_item = QTableWidgetItem(demand['status'])
            if demand['status'] == 'FULFILLED':
                status_item.setBackground(QColor('#276749'))
                status_item.setForeground(QColor('white'))
            elif demand['status'] == 'PENDING':
                status_item.setBackground(QColor('#f6ad55'))
            self.table.setItem(idx, 3, status_item)
            
            notes_table.setItem(idx, 3, QTableWidgetItem(demand['notes'] or ''))
            
            # Mark as fulfilled button
            btn_layout = QHBoxLayout()
            if demand['status'] != 'FULFILLED':
                fulfill_btn = QPushButton('✓ Fulfill')
                fulfill_btn.setMinimumHeight(30)
                fulfill_btn.setStyleSheet('font-size: 10px; font-weight: bold; padding: 4px;')
                fulfill_btn.clicked.connect(lambda checked, d=demand: self.mark_fulfilled(d))
                btn_layout.addWidget(fulfill_btn)
            
            widget = QWidget()
            widget.setLayout(btn_layout)
            notes_table.setCellWidget(idx, 4, widget)
        
        layout.addWidget(notes_table)
        
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def mark_fulfilled(self, demand):
        """Mark demand as fulfilled."""
        try:
            self.db.execute(
                "UPDATE demand_notes SET status = ? WHERE id = ?",
                ('FULFILLED', demand['id'])
            )
            self.db.log_activity(self.current_user['id'], self.current_user['username'],
                               'FULFILL_DEMAND', f'Marked demand {demand["id"]} as fulfilled')
            QMessageBox.information(self, 'Success', 'Demand marked as fulfilled!')
            self.load_low_stock()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to mark demand: {str(e)}')

# ==================== BILL HISTORY ====================
class BillHistoryWidget(QWidget):
    """Bill history and search."""
    
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.init_ui()
        self.load_bills()
    
    def init_ui(self):
        """Initialize bill history UI."""
        layout = QVBoxLayout()
        
        # Filters
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel('Bill ID:'))
        self.bill_id_input = QLineEdit()
        self.bill_id_input.setMaximumWidth(150)
        self.bill_id_input.textChanged.connect(self.filter_bills)
        filter_layout.addWidget(self.bill_id_input)
        
        filter_layout.addWidget(QLabel('From Date:'))
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addDays(-30))
        self.from_date.dateChanged.connect(self.filter_bills)
        filter_layout.addWidget(self.from_date)
        
        filter_layout.addWidget(QLabel('To Date:'))
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        self.to_date.dateChanged.connect(self.filter_bills)
        filter_layout.addWidget(self.to_date)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # Bills table
        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(7)
        headers = ['Bill ID', 'Date', 'Total', 'Discount', 'Payable', 'User', 'Actions']
        self.bills_table.setHorizontalHeaderLabels(headers)
        self.bills_table.horizontalHeader().setStretchLastSection(False)
        self.bills_table.setColumnWidth(0, 120)  # Bill ID
        self.bills_table.setColumnWidth(1, 100)  # Date
        self.bills_table.setColumnWidth(2, 100)  # Total
        self.bills_table.setColumnWidth(3, 100)  # Discount
        self.bills_table.setColumnWidth(4, 100)  # Payable
        self.bills_table.setColumnWidth(5, 80)   # User
        self.bills_table.setColumnWidth(6, 280)  # Actions - increased width for visible buttons
        self.bills_table.setRowHeight(0, 35)
        layout.addWidget(self.bills_table)
        
        self.setLayout(layout)
    
    def load_bills(self):
        """Load bills."""
        self.filter_bills()
    
    def filter_bills(self):
        """Filter bills."""
        self.bills_table.setRowCount(0)
        
        bill_id = self.bill_id_input.text().strip()
        from_date = self.from_date.date().toString('yyyy-MM-dd')
        to_date = self.to_date.date().toString('yyyy-MM-dd')
        
        query = "SELECT * FROM bills WHERE bill_date >= ? AND bill_date <= ?"
        params = [from_date + ' 00:00:00', to_date + ' 23:59:59']
        
        if bill_id:
            query += " AND bill_id LIKE ?"
            params.append(f'%{bill_id}%')
        
        query += " ORDER BY bill_date DESC"
        
        bills = self.db.fetch_all(query, params)
        
        for bill in bills:
            row = self.bills_table.rowCount()
            self.bills_table.insertRow(row)
            self.bills_table.setRowHeight(row, 40)
            
            self.bills_table.setItem(row, 0, QTableWidgetItem(bill['bill_id']))
            self.bills_table.setItem(row, 1, QTableWidgetItem(bill['bill_date'][:10]))
            self.bills_table.setItem(row, 2, QTableWidgetItem(f"Rs. {bill['total_amount']:.2f}"))
            self.bills_table.setItem(row, 3, QTableWidgetItem(f"Rs. {bill['discount_amount']:.2f}"))
            self.bills_table.setItem(row, 4, QTableWidgetItem(f"Rs. {bill['payable_amount']:.2f}"))
            
            user = self.db.fetch_one("SELECT username FROM users WHERE id = ?", (bill['user_id'],))
            self.bills_table.setItem(row, 5, QTableWidgetItem(user['username'] if user else 'N/A'))
            
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(5, 5, 5, 5)
            btn_layout.setSpacing(8)
            
            view_btn = QPushButton('👁️ View')
            view_btn.setMinimumHeight(35)
            view_btn.setMinimumWidth(65)
            view_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 5px; background-color: #2c5282; color: white; border: none; border-radius: 3px;')
            view_btn.clicked.connect(lambda checked, b=bill: self.view_bill(b))
            btn_layout.addWidget(view_btn)
            
            reopen_btn = QPushButton('🛒 Cart')
            reopen_btn.setMinimumHeight(35)
            reopen_btn.setMinimumWidth(65)
            reopen_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 5px; background-color: #276749; color: white; border: none; border-radius: 3px;')
            reopen_btn.clicked.connect(lambda checked, b=bill: self.reopen_bill_in_cart(b, None))
            btn_layout.addWidget(reopen_btn)
            
            reprint_btn = QPushButton('🖨️ Reprint')
            reprint_btn.setMinimumHeight(35)
            reprint_btn.setMinimumWidth(75)
            reprint_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 5px; background-color: #744210; color: white; border: none; border-radius: 3px;')
            reprint_btn.clicked.connect(lambda checked, b=bill: self.reprint_bill(b))
            btn_layout.addWidget(reprint_btn)
            
            widget = QWidget()
            widget.setLayout(btn_layout)
            self.bills_table.setCellWidget(row, 6, widget)
    
    def view_bill(self, bill):
        """View bill details."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Bill {bill["bill_id"]}')
        dialog.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Bill header
        header_text = f"""
        Bill ID: {bill['bill_id']}
        Bill Number: {bill['bill_number']}
        Date: {bill['bill_date']}
        
        Total: Rs. {bill['total_amount']:.2f}
        Discount ({bill['discount_percent']}%): Rs. {bill['discount_amount']:.2f}
        Payable: Rs. {bill['payable_amount']:.2f}
        Received: Rs. {bill['received_amount']:.2f}
        Change: Rs. {bill['balance_amount']:.2f}
        """
        
        header_label = QLabel(header_text)
        layout.addWidget(header_label)
        
        # Items table
        items_table = QTableWidget()
        items_table.setColumnCount(5)
        items_table.setHorizontalHeaderLabels(['Product', 'Qty', 'Unit Price', 'Discount', 'Total'])
        
        items = self.db.fetch_all(
            "SELECT * FROM bill_items WHERE bill_id = ?", (bill['id'],)
        )
        
        for idx, item in enumerate(items):
            items_table.insertRow(idx)
            
            product = self.db.fetch_one("SELECT name FROM products WHERE id = ?", (item['product_id'],))
            items_table.setItem(idx, 0, QTableWidgetItem(product['name'] if product else 'N/A'))
            items_table.setItem(idx, 1, QTableWidgetItem(str(item['quantity'])))
            items_table.setItem(idx, 2, QTableWidgetItem(f"Rs. {item['unit_price']:.2f}"))
            items_table.setItem(idx, 3, QTableWidgetItem(f"Rs. {item['discount_amount']:.2f}"))
            items_table.setItem(idx, 4, QTableWidgetItem(f"Rs. {item['line_total']:.2f}"))
        
        layout.addWidget(items_table)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        reopen_btn = QPushButton('✏️ Reopen in Cart')
        reopen_btn.setProperty('id', 'successBtn')
        reopen_btn.setStyleSheet('font-size: 12px; font-weight: bold;')
        reopen_btn.clicked.connect(lambda: self.reopen_bill_in_cart(bill, dialog))
        button_layout.addWidget(reopen_btn)
        
        close_btn = QPushButton('❌ Close')
        close_btn.setStyleSheet('font-size: 12px; font-weight: bold;')
        close_btn.clicked.connect(dialog.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.setStyleSheet(THEME_STYLESHEET)
        dialog.exec()
    
    def reprint_bill(self, bill):
        """Reprint bill receipt."""
        items = self.db.fetch_all(
            "SELECT bi.*, p.name FROM bill_items bi LEFT JOIN products p ON bi.product_id = p.id WHERE bi.bill_id = ?",
            (bill['id'],)
        )
        
        receipt_html = f"""
        <html>
        <body style="font-family: monospace; font-size: 12px;">
        <center><h2>FATIMA TU ZAHRA MEDICAL CENTRE</h2></center>
        <hr>
        <center><b>RECEIPT (REPRINT)</b></center>
        <hr>
        <p><b>Bill ID:</b> {bill['bill_id']}</p>
        <p><b>Date:</b> {bill['bill_date']}</p>
        <hr>
        <table style="width: 100%;">
        <tr><td><b>Item</b></td><td align="right"><b>Qty</b></td><td align="right"><b>Price</b></td></tr>
        """
        
        for item in items:
            receipt_html += f"<tr><td>{item['name'][:20]}</td><td align='right'>{item['quantity']}</td><td align='right'>Rs. {item['line_total']:.2f}</td></tr>"
        
        receipt_html += f"""
        </table>
        <hr>
        <p><b>Total:</b> Rs. {bill['total_amount']:.2f}</p>
        <p><b>Discount:</b> Rs. {bill['discount_amount']:.2f}</p>
        <p><b>Payable:</b> Rs. {bill['payable_amount']:.2f}</p>
        <p><b>Change:</b> Rs. {bill['balance_amount']:.2f}</p>
        <hr>
        <center><p>Thank you for your business!</p></center>
        </body>
        </html>
        """
        
        doc = QTextDocument()
        doc.setHtml(receipt_html)
        
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            doc.print(printer)
    
    def reopen_bill_in_cart(self, bill, dialog):
        """Reopen a previous bill in the shopping cart."""
        try:
            # Get bill items with serial_no and purchase_price
            items = self.db.fetch_all(
                "SELECT bi.*, p.name, p.serial_no, p.sale_price, p.purchase_price FROM bill_items bi LEFT JOIN products p ON bi.product_id = p.id WHERE bi.bill_id = ?",
                (bill['id'],)
            )
            
            # Convert to cart format
            cart = []
            for item in items:
                cart_item = {
                    'product_id': item['product_id'],
                    'serial_no': item['serial_no'] if item['serial_no'] else 'N/A',
                    'name': item['name'],
                    'quantity': item['quantity'],
                    'sale_price': item['unit_price'],  # Use unit_price from bill_items
                    'purchase_price': item['purchase_price'] if item['purchase_price'] else item['unit_price'],
                    'discount_percent': item['discount_percent'] if item['discount_percent'] else 0,
                    'stock': 999  # Placeholder for stock availability
                }
                cart.append(cart_item)
            
            # Access main app to load into POS
            parent = self.parent()
            while parent and not hasattr(parent, 'modules'):
                parent = parent.parent()
            
            if parent and hasattr(parent, 'modules'):
                # Initialize POS if not already done
                if 'pos' not in parent.modules:
                    from datetime import datetime
                    parent.modules['pos'] = POSScreen(self.db, self.current_user, parent)
                    parent.stacked_widget.addWidget(parent.modules['pos'])
                
                # Load cart data into POS
                parent.modules['pos'].cart = cart
                parent.modules['pos'].load_cart_to_ui()
                
                # Close the dialog if provided
                if dialog:
                    dialog.close()
                
                # Switch to POS screen
                parent.stacked_widget.setCurrentWidget(parent.modules['pos'])
                
                QMessageBox.information(self, 'Success', 'Bill reopened in shopping cart!\nYou can now edit items and save as a new bill')
            else:
                QMessageBox.critical(self, 'Error', 'Could not access POS screen')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to reopen bill: {str(e)}')
            print(f"Error details: {e}")
            import traceback
            traceback.print_exc()
    
    def preview_held_bill(self, cart_data):
        """Preview a held bill before reopening."""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle('Preview Held Bill')
            dialog.setGeometry(200, 200, 600, 400)
            
            layout = QVBoxLayout()
            
            # Title
            title_label = QLabel('Held Bill Preview')
            title_label.setStyleSheet('font-size: 14px; font-weight: bold; color: #2c5282;')
            layout.addWidget(title_label)
            
            # Items table
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(['Item Name', 'Qty', 'Unit Price', 'Subtotal'])
            table.setColumnWidth(0, 250)
            table.setColumnWidth(1, 60)
            table.setColumnWidth(2, 100)
            table.setColumnWidth(3, 100)
            
            total_amount = 0
            for idx, item in enumerate(cart_data):
                table.insertRow(idx)
                table.setRowHeight(idx, 30)
                
                table.setItem(idx, 0, QTableWidgetItem(item['name']))
                table.setItem(idx, 1, QTableWidgetItem(str(item['quantity'])))
                table.setItem(idx, 2, QTableWidgetItem(f"Rs. {item['unit_price']:.2f}"))
                
                item_total = item['quantity'] * item['unit_price']
                table.setItem(idx, 3, QTableWidgetItem(f"Rs. {item_total:.2f}"))
                
                total_amount += item_total
            
            layout.addWidget(table)
            
            # Total
            total_frame = QFrame()
            total_frame.setStyleSheet('background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 3px;')
            total_layout = QHBoxLayout()
            
            total_label = QLabel(f"Total Amount:")
            total_label.setStyleSheet('font-size: 12px; font-weight: bold;')
            total_value = QLabel(f"Rs. {total_amount:.2f}")
            total_value.setStyleSheet('font-size: 14px; font-weight: bold; color: #276749;')
            
            total_layout.addWidget(total_label)
            total_layout.addStretch()
            total_layout.addWidget(total_value)
            total_frame.setLayout(total_layout)
            layout.addWidget(total_frame)
            
            # Close button
            close_btn = QPushButton('Close')
            close_btn.setMinimumHeight(35)
            close_btn.setStyleSheet('font-size: 12px; font-weight: bold;')
            close_btn.clicked.connect(dialog.close)
            layout.addWidget(close_btn)
            
            dialog.setLayout(layout)
            dialog.setStyleSheet(THEME_STYLESHEET)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to preview bill: {str(e)}')

# ==================== ACTIVITY LOGS ====================
class ActivityLogsWidget(QWidget):
    """Activity logs for admin."""
    
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        
        if current_user['role'] != 'admin':
            layout = QVBoxLayout()
            label = QLabel('Access Denied - Admin Only')
            layout.addWidget(label)
            self.setLayout(layout)
            return
        
        self.init_ui()
        self.load_logs()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout()
        
        # Filters
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel('User:'))
        self.user_combo = QComboBox()
        self.user_combo.addItem('All', '')
        users = self.db.fetch_all("SELECT id, username FROM users WHERE is_active = 1 ORDER BY username")
        for user in users:
            self.user_combo.addItem(user['username'], user['id'])
        self.user_combo.currentIndexChanged.connect(self.load_logs)
        filter_layout.addWidget(self.user_combo)
        
        filter_layout.addWidget(QLabel('Action:'))
        self.action_combo = QComboBox()
        self.action_combo.addItem('All', '')
        for action in ['LOGIN', 'LOGOUT', 'SALE', 'DELETE_PRODUCT', 'HOLD_BILL']:
            self.action_combo.addItem(action, action)
        self.action_combo.currentIndexChanged.connect(self.load_logs)
        filter_layout.addWidget(self.action_combo)
        
        export_btn = QPushButton('Export CSV')
        export_btn.clicked.connect(self.export_csv)
        filter_layout.addWidget(export_btn)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # Logs table
        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(5)
        self.logs_table.setHorizontalHeaderLabels(['User', 'Action', 'Details', 'Timestamp', 'Type'])
        layout.addWidget(self.logs_table)
        
        self.setLayout(layout)
    
    def load_logs(self):
        """Load activity logs."""
        self.logs_table.setRowCount(0)
        
        user_id = self.user_combo.currentData()
        action = self.action_combo.currentData()
        
        query = "SELECT * FROM activity_logs WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if action:
            query += " AND action = ?"
            params.append(action)
        
        query += " ORDER BY timestamp DESC LIMIT 1000"
        
        logs = self.db.fetch_all(query, params)
        
        for log in logs:
            row = self.logs_table.rowCount()
            self.logs_table.insertRow(row)
            
            self.logs_table.setItem(row, 0, QTableWidgetItem(log['username']))
            self.logs_table.setItem(row, 1, QTableWidgetItem(log['action']))
            self.logs_table.setItem(row, 2, QTableWidgetItem(log['details'][:50]))
            self.logs_table.setItem(row, 3, QTableWidgetItem(log['timestamp'][:19]))
            
            type_item = QTableWidgetItem(log['action'])
            if log['action'] == 'LOGIN':
                type_item.setBackground(QColor('#276749'))
                type_item.setForeground(QColor('white'))
            elif log['action'] == 'LOGOUT':
                type_item.setBackground(QColor('#c53030'))
                type_item.setForeground(QColor('white'))
            self.logs_table.setItem(row, 4, type_item)
    
    def export_csv(self):
        """Export logs to CSV."""
        user_id = self.user_combo.currentData()
        action = self.action_combo.currentData()
        
        query = "SELECT * FROM activity_logs WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if action:
            query += " AND action = ?"
            params.append(action)
        
        query += " ORDER BY timestamp DESC LIMIT 10000"
        
        logs = self.db.fetch_all(query, params)
        
        filename = f"activity_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['User', 'Action', 'Details', 'Timestamp'])
            for log in logs:
                writer.writerow([log['username'], log['action'], log['details'], log['timestamp']])
        
        QMessageBox.information(self, 'Success', f'Exported {len(logs)} logs to {filename}')

# ==================== USER MANAGEMENT ====================
class UserManagementWidget(QWidget):
    """User management for admin."""
    
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        
        if current_user['role'] != 'admin':
            layout = QVBoxLayout()
            label = QLabel('Access Denied - Admin Only')
            layout.addWidget(label)
            self.setLayout(layout)
            return
        
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout()
        
        # Add button
        add_btn = QPushButton('Add New User')
        add_btn.setProperty('id', 'successBtn')
        add_btn.clicked.connect(self.add_user)
        layout.addWidget(add_btn)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(8)
        headers = ['Username', 'Full Name', 'Email', 'Role', 'Status', 'Last Login', 'Action Edit', 'Action Disable']
        self.users_table.setHorizontalHeaderLabels(headers)
        layout.addWidget(self.users_table)
        
        self.setLayout(layout)
    
    def load_users(self):
        """Load users."""
        self.users_table.setRowCount(0)
        
        users = self.db.fetch_all("SELECT * FROM users ORDER BY created_at DESC")
        
        for user in users:
            row = self.users_table.rowCount()
            self.users_table.insertRow(row)
            
            self.users_table.setItem(row, 0, QTableWidgetItem(user['username']))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['full_name']))
            self.users_table.setItem(row, 2, QTableWidgetItem(user['email'] or 'N/A'))
            self.users_table.setItem(row, 3, QTableWidgetItem(user['role']))
            
            status = 'Active' if user['is_active'] else 'Inactive'
            status_item = QTableWidgetItem(status)
            if user['is_active']:
                status_item.setBackground(QColor('#276749'))
            else:
                status_item.setBackground(QColor('#cccccc'))
            status_item.setForeground(QColor('white'))
            self.users_table.setItem(row, 4, status_item)
            
            last_login = user['last_login'][:10] if user['last_login'] else 'Never'
            self.users_table.setItem(row, 5, QTableWidgetItem(last_login))
            
            edit_btn = QPushButton('Edit')
            edit_btn.setMinimumHeight(35)
            edit_btn.setMinimumWidth(70)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #d69e2e;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 6px 12px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #b8860b;
                }
                QPushButton:pressed {
                    background-color: #92670f;
                }
            """)
            edit_btn.clicked.connect(lambda checked, u=user: self.edit_user(u))
            self.users_table.setCellWidget(row, 6, edit_btn)
            
            status_btn = QPushButton('Disable' if user['is_active'] else 'Enable')
            status_btn.setMinimumHeight(35)
            status_btn.setMinimumWidth(75)
            if user['is_active']:
                status_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #c53030;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 6px 12px;
                        border: none;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #a02020;
                    }
                    QPushButton:pressed {
                        background-color: #7a1818;
                    }
                """)
            else:
                status_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #276749;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 6px 12px;
                        border: none;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #1d5035;
                    }
                    QPushButton:pressed {
                        background-color: #0f2d1b;
                    }
                """)
            status_btn.clicked.connect(lambda checked, u=user: self.toggle_status(u))
            self.users_table.setCellWidget(row, 7, status_btn)
    
    def add_user(self):
        """Add new user."""
        dialog = UserDialog(self.db, None, self)
        if dialog.exec():
            self.load_users()
    
    def edit_user(self, user):
        """Edit user."""
        dialog = UserDialog(self.db, dict(user), self)
        if dialog.exec():
            self.load_users()
    
    def toggle_status(self, user):
        """Toggle user status."""
        new_status = not user['is_active']
        self.db.execute("UPDATE users SET is_active = ? WHERE id = ?", (new_status, user['id']))
        self.load_users()

# ==================== USER DIALOG ====================
class UserDialog(QDialog):
    """User add/edit dialog."""
    
    def __init__(self, db, user=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.user = user
        self.setWindowTitle('New User' if not user else f'Edit - {user["username"]}')
        self.setGeometry(100, 100, 400, 350)
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog."""
        layout = QFormLayout()
        
        # Username
        self.username_input = QLineEdit()
        if self.user:
            self.username_input.setText(self.user['username'])
            self.username_input.setReadOnly(True)
        layout.addRow('Username:', self.username_input)
        
        # Full Name
        self.fullname_input = QLineEdit()
        if self.user:
            self.fullname_input.setText(self.user['full_name'])
        layout.addRow('Full Name:', self.fullname_input)
        
        # Email
        self.email_input = QLineEdit()
        if self.user:
            self.email_input.setText(self.user['email'] or '')
        layout.addRow('Email:', self.email_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        if self.user:
            self.password_input.setPlaceholderText('Leave blank to keep current password')
        else:
            self.password_input.setPlaceholderText('Required for new users')
        layout.addRow('Password:', self.password_input)
        
        # Role
        self.role_combo = QComboBox()
        self.role_combo.addItems(['admin', 'staff'])
        if self.user:
            self.role_combo.setCurrentText(self.user['role'])
        layout.addRow('Role:', self.role_combo)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton('Save')
        save_btn.setProperty('id', 'successBtn')
        save_btn.clicked.connect(self.save)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
        self.setStyleSheet(THEME_STYLESHEET)
    
    def save(self):
        """Save user."""
        username = self.username_input.text().strip()
        fullname = self.fullname_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()
        
        if not username or not fullname:
            QMessageBox.warning(self, 'Validation', 'Username and Full Name are required')
            return
        
        if self.user:
            # Update
            self.db.execute(
                "UPDATE users SET full_name=?, email=?, role=? WHERE id=?",
                (fullname, email, role, self.user['id'])
            )
            if password:
                self.db.execute("UPDATE users SET password=? WHERE id=?", (password, self.user['id']))
        else:
            # Create new user
            if not password:
                QMessageBox.warning(self, 'Validation', 'Password is required for new users')
                return
            
            self.db.execute(
                """INSERT INTO users (username, password, full_name, email, role)
                   VALUES (?, ?, ?, ?, ?)""",
                (username, password, fullname, email, role)
            )
        
        self.accept()

# ==================== PROFILE WIDGET ====================
class ProfileWidget(QWidget):
    """User profile and settings."""
    
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.init_ui()
        self.load_profile()
    
    def init_ui(self):
        """Initialize profile UI."""
        layout = QVBoxLayout()
        
        # Profile Info
        profile_layout = QVBoxLayout()
        profile_layout.addWidget(QLabel('Profile Information'))
        
        form_layout = QFormLayout()
        
        self.fullname_input = QLineEdit()
        form_layout.addRow('Full Name:', self.fullname_input)
        
        self.email_input = QLineEdit()
        form_layout.addRow('Email:', self.email_input)
        
        self.role_label = QLabel()
        form_layout.addRow('Role:', self.role_label)
        
        update_btn = QPushButton('Update Profile')
        update_btn.setProperty('id', 'successBtn')
        update_btn.clicked.connect(self.update_profile)
        form_layout.addRow(update_btn)
        
        profile_layout.addLayout(form_layout)
        layout.addLayout(profile_layout)
        
        layout.addSpacing(20)
        
        # Password Change
        password_layout = QVBoxLayout()
        password_layout.addWidget(QLabel('Change Password'))
        
        form_layout2 = QFormLayout()
        
        self.current_pwd = QLineEdit()
        self.current_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout2.addRow('Current Password:', self.current_pwd)
        
        self.new_pwd = QLineEdit()
        self.new_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout2.addRow('New Password:', self.new_pwd)
        
        self.confirm_pwd = QLineEdit()
        self.confirm_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout2.addRow('Confirm Password:', self.confirm_pwd)
        
        change_btn = QPushButton('Change Password')
        change_btn.setProperty('id', 'successBtn')
        change_btn.clicked.connect(self.change_password)
        form_layout2.addRow(change_btn)
        
        password_layout.addLayout(form_layout2)
        layout.addLayout(password_layout)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def load_profile(self):
        """Load profile data."""
        self.fullname_input.setText(self.current_user['full_name'])
        self.email_input.setText(self.current_user['email'] or '')
        self.role_label.setText(self.current_user['role'].upper())
    
    def update_profile(self):
        """Update profile."""
        fullname = self.fullname_input.text().strip()
        email = self.email_input.text().strip()
        
        if not fullname:
            QMessageBox.warning(self, 'Validation', 'Full Name is required')
            return
        
        self.db.execute(
            "UPDATE users SET full_name=?, email=? WHERE id=?",
            (fullname, email, self.current_user['id'])
        )
        
        QMessageBox.information(self, 'Success', 'Profile updated successfully')
    
    def change_password(self):
        """Change password."""
        current = self.current_pwd.text()
        new_pwd = self.new_pwd.text()
        confirm = self.confirm_pwd.text()
        
        if len(new_pwd) < 6:
            QMessageBox.warning(self, 'Validation', 'Password must be at least 6 characters')
            return
        
        if new_pwd != confirm:
            QMessageBox.warning(self, 'Validation', 'Passwords do not match')
            return
        
        # Verify current password
        user = self.db.fetch_one(
            "SELECT * FROM users WHERE id = ? AND password = ?",
            (self.current_user['id'], current)
        )
        
        if not user:
            QMessageBox.critical(self, 'Error', 'Current password is incorrect')
            return
        
        # Update password
        self.db.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (new_pwd, self.current_user['id'])
        )
        
        QMessageBox.information(self, 'Success', 'Password changed successfully')
        self.current_pwd.clear()
        self.new_pwd.clear()
        self.confirm_pwd.clear()

# ==================== MAIN APPLICATION ====================
class PharmacyPOSApp(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.db = PharmacyDB()
        self.current_user = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize main UI."""
        self.setWindowTitle('Pharmacy POS - Fatima Tu Zahra Medical Centre')
        self.setGeometry(0, 0, 1400, 900)
        
        # Show login screen
        self.show_login()
    
    def show_login(self):
        """Show login screen."""
        self.login_screen = LoginScreen(self.db)
        self.login_screen.login_successful.connect(self.on_login_success)
        self.setCentralWidget(self.login_screen)
        self.setWindowTitle('Fatima Tu Zahra Medical Centre Girote- Pharmacy POS Login')
    
    def on_login_success(self, user_data):
        """Handle successful login."""
        self.current_user = user_data
        self.show_dashboard()
    
    def show_dashboard(self):
        """Show main dashboard after login."""
        # Main container
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName('sidebar')
        sidebar.setMaximumWidth(200)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo at top
        logo_pixmap = QPixmap('logo.jpg')
        if not logo_pixmap.isNull():
            logo_label = QLabel()
            scaled_logo = logo_pixmap.scaledToWidth(180, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_logo)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setStyleSheet('padding: 10px;')
            sidebar_layout.addWidget(logo_label)
        
        # Hospital name in sidebar
        
        # Navigation buttons
        self.modules = {}
        
        # Dashboard
        dashboard_btn = QPushButton('📊 Dashboard')
        dashboard_btn.clicked.connect(self.show_module_dashboard)
        sidebar_layout.addWidget(dashboard_btn)
        
        # Sale/POS
        pos_btn = QPushButton('🛒 Sale ')
        pos_btn.clicked.connect(self.show_module_pos)
        sidebar_layout.addWidget(pos_btn)
        
        # Held Bills (for all users)
        held_bills_btn = QPushButton('📂 Held Bills')
        held_bills_btn.clicked.connect(self.show_held_bills)
        sidebar_layout.addWidget(held_bills_btn)
        
        # Admin-only modules
        if self.current_user['role'] == 'admin':
            inventory_btn = QPushButton('📦 Inventory')
            inventory_btn.clicked.connect(self.show_module_inventory)
            sidebar_layout.addWidget(inventory_btn)
            
            low_stock_btn = QPushButton('⚠️ Low Stock')
            low_stock_btn.clicked.connect(self.show_module_low_stock)
            sidebar_layout.addWidget(low_stock_btn)
            
            categories_btn = QPushButton('📂 Categories')
            categories_btn.clicked.connect(self.show_module_categories)
            sidebar_layout.addWidget(categories_btn)
            
            vendors_btn = QPushButton('🏢 Vendors')
            vendors_btn.clicked.connect(self.show_module_vendors)
            sidebar_layout.addWidget(vendors_btn)
            
            bills_btn = QPushButton('📋 Bill History')
            bills_btn.clicked.connect(self.show_module_bills)
            sidebar_layout.addWidget(bills_btn)
            
            logs_btn = QPushButton('📝 Activity Logs')
            logs_btn.clicked.connect(self.show_module_logs)
            sidebar_layout.addWidget(logs_btn)
            
            users_btn = QPushButton('👥 Users')
            users_btn.clicked.connect(self.show_module_users)
            sidebar_layout.addWidget(users_btn)
        
        # Profile (all users)
        profile_btn = QPushButton('👤 Profile')
        profile_btn.clicked.connect(self.show_module_profile)
        sidebar_layout.addWidget(profile_btn)
        
        sidebar_layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton('🚪 Logout')
        logout_btn.setProperty('id', 'dangerBtn')
        logout_btn.clicked.connect(self.do_logout)
        sidebar_layout.addWidget(logout_btn)
        
        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)
        
        # Content area
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle(f'Pharmacy POS - {self.current_user["username"]} ({self.current_user["role"]})')
        
        # Show dashboard by default
        self.show_module_dashboard()
        
        self.setStyleSheet(THEME_STYLESHEET)
    
    def show_module_dashboard(self):
        """Show dashboard module."""
        if 'dashboard' not in self.modules:
            self.modules['dashboard'] = DashboardWidget(self.db, self.current_user)
            self.stacked_widget.addWidget(self.modules['dashboard'])
        
        self.stacked_widget.setCurrentWidget(self.modules['dashboard'])
    
    def show_module_pos(self):
        """Show POS module."""
        if 'pos' not in self.modules:
            self.modules['pos'] = POSScreen(self.db, self.current_user, self)
            self.stacked_widget.addWidget(self.modules['pos'])
        
        self.stacked_widget.setCurrentWidget(self.modules['pos'])
    
    def show_module_inventory(self):
        """Show inventory module."""
        if 'inventory' not in self.modules:
            self.modules['inventory'] = InventoryWidget(self.db, self.current_user)
            self.stacked_widget.addWidget(self.modules['inventory'])
        
        self.stacked_widget.setCurrentWidget(self.modules['inventory'])
    
    def show_module_low_stock(self):
        """Show low stock management module."""
        if 'low_stock' not in self.modules:
            self.modules['low_stock'] = LowStockWidget(self.db, self.current_user)
            self.stacked_widget.addWidget(self.modules['low_stock'])
        
        self.stacked_widget.setCurrentWidget(self.modules['low_stock'])
    
    def show_module_categories(self):
        """Show categories management module."""
        if 'categories' not in self.modules:
            self.modules['categories'] = CategoriesWidget(self.db, self.current_user)
            self.stacked_widget.addWidget(self.modules['categories'])
        
        self.stacked_widget.setCurrentWidget(self.modules['categories'])
    
    def show_module_vendors(self):
        """Show vendors management module."""
        if 'vendors' not in self.modules:
            self.modules['vendors'] = VendorsWidget(self.db, self.current_user)
            self.stacked_widget.addWidget(self.modules['vendors'])
        
        self.stacked_widget.setCurrentWidget(self.modules['vendors'])
    
    def show_module_bills(self):
        """Show bill history module."""
        if 'bills' not in self.modules:
            self.modules['bills'] = BillHistoryWidget(self.db, self.current_user)
            self.stacked_widget.addWidget(self.modules['bills'])
        
        self.stacked_widget.setCurrentWidget(self.modules['bills'])
    
    def show_module_logs(self):
        """Show activity logs module."""
        if 'logs' not in self.modules:
            self.modules['logs'] = ActivityLogsWidget(self.db, self.current_user)
            self.stacked_widget.addWidget(self.modules['logs'])
        
        self.stacked_widget.setCurrentWidget(self.modules['logs'])
    
    def show_module_users(self):
        """Show user management module."""
        if 'users' not in self.modules:
            self.modules['users'] = UserManagementWidget(self.db, self.current_user)
            self.stacked_widget.addWidget(self.modules['users'])
        
        self.stacked_widget.setCurrentWidget(self.modules['users'])
    
    def show_module_profile(self):
        """Show profile module."""
        if 'profile' not in self.modules:
            self.modules['profile'] = ProfileWidget(self.db, self.current_user)
            self.stacked_widget.addWidget(self.modules['profile'])
        
        self.stacked_widget.setCurrentWidget(self.modules['profile'])
    
    def show_held_bills(self):
        """Show held bills management."""
        try:
            # Fetch held bills for current user
            bills = self.db.fetch_all(
                "SELECT id, bill_data, held_at FROM held_bills WHERE user_id = ? ORDER BY held_at DESC",
                (self.current_user['id'],)
            )
            
            if not bills:
                QMessageBox.information(self, 'No Held Bills', 'You have no held bills')
                return
            
            # Create dialog to select bill
            dialog = QDialog(self)
            dialog.setWindowTitle('Held Bills Management')
            dialog.setGeometry(200, 200, 700, 500)
            
            layout = QVBoxLayout()
            
            # Table to show held bills
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(['Items', 'Total Amount', 'Held At', 'Actions'])
            table.horizontalHeader().setStretchLastSection(False)
            table.setColumnWidth(0, 80)
            table.setColumnWidth(1, 120)
            table.setColumnWidth(2, 160)
            table.setColumnWidth(3, 280)  # Increased for visible buttons
            
            for idx, bill in enumerate(bills):
                try:
                    import json
                    cart_data = json.loads(bill['bill_data'])
                    total_items = len(cart_data) if isinstance(cart_data, list) else 0
                    
                    # Calculate total amount with safety checks
                    total_amount = 0
                    if isinstance(cart_data, list):
                        for item in cart_data:
                            quantity = item.get('quantity', 1)
                            unit_price = item.get('sale_price', 0)
                            total_amount += quantity * unit_price
                    
                    table.insertRow(idx)
                    table.setRowHeight(idx, 40)
                    table.setItem(idx, 0, QTableWidgetItem(str(total_items)))
                    table.setItem(idx, 1, QTableWidgetItem(f"Rs. {total_amount:.2f}"))
                    table.setItem(idx, 2, QTableWidgetItem(str(bill['held_at'])))
                    
                    # Action buttons
                    btn_widget = QWidget()
                    btn_layout = QHBoxLayout(btn_widget)
                    btn_layout.setContentsMargins(5, 5, 5, 5)
                    btn_layout.setSpacing(8)
                    
                    reopen_btn = QPushButton('✏️ Reopen')
                    reopen_btn.setMinimumHeight(35)
                    reopen_btn.setMinimumWidth(70)
                    reopen_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 5px; background-color: #276749; color: white; border: none; border-radius: 3px;')
                    
                    preview_btn = QPushButton('👁️ Preview')
                    preview_btn.setMinimumHeight(35)
                    preview_btn.setMinimumWidth(75)
                    preview_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 5px; background-color: #2c5282; color: white; border: none; border-radius: 3px;')
                    
                    delete_btn = QPushButton('🗑️ Delete')
                    delete_btn.setMinimumHeight(35)
                    delete_btn.setMinimumWidth(70)
                    delete_btn.setStyleSheet('font-size: 11px; font-weight: bold; padding: 5px; background-color: #c53030; color: white; border: none; border-radius: 3px;')
                    
                    reopen_btn.clicked.connect(lambda checked, bid=bill['id']: self.reopen_held_bill(bid, dialog))
                    preview_btn.clicked.connect(lambda checked, data=cart_data: self.preview_held_bill(data))
                    delete_btn.clicked.connect(lambda checked, bid=bill['id'], r=idx: self.delete_held_bill(bid, table, r))
                    
                    btn_layout.addWidget(reopen_btn)
                    btn_layout.addWidget(preview_btn)
                    btn_layout.addWidget(delete_btn)
                    btn_layout.addStretch()
                    table.setCellWidget(idx, 3, btn_widget)
                except Exception as e:
                    print(f"Error processing held bill {bill['id']}: {e}")
                    continue
            
            layout.addWidget(table)
            
            close_btn = QPushButton('Close')
            close_btn.clicked.connect(dialog.close)
            layout.addWidget(close_btn)
            
            dialog.setLayout(layout)
            dialog.setStyleSheet(THEME_STYLESHEET)
            dialog.exec()
        except Exception as e:
            import traceback
            print(f"Error in show_held_bills: {traceback.format_exc()}")
            QMessageBox.critical(self, 'Error', f'Failed to load held bills: {str(e)}')
    
    def reopen_held_bill(self, bill_id, dialog):
        """Reopen a held bill in POS screen."""
        try:
            bill = self.db.fetch_one(
                "SELECT bill_data FROM held_bills WHERE id = ?",
                (bill_id,)
            )
            
            if bill:
                import json
                cart_data = json.loads(bill['bill_data'])
                
                # Validate and ensure all required keys exist in cart items
                for item in cart_data:
                    # Ensure all required keys exist with defaults
                    if 'discount_percent' not in item:
                        item['discount_percent'] = 0
                    if 'purchase_price' not in item:
                        item['purchase_price'] = item.get('sale_price', 0)
                    if 'sale_price' not in item:
                        item['sale_price'] = 0
                    if 'quantity' not in item:
                        item['quantity'] = 1
                    if 'serial_no' not in item:
                        item['serial_no'] = ''
                    if 'name' not in item:
                        item['name'] = ''
                    if 'product_id' not in item:
                        item['product_id'] = 0
                    if 'stock' not in item:
                        item['stock'] = 0
                
                # Create POS module if it doesn't exist
                if 'pos' not in self.modules:
                    self.modules['pos'] = POSScreen(self.db, self.current_user, self)
                    self.stacked_widget.addWidget(self.modules['pos'])
                
                # Load cart data and switch to POS screen
                self.modules['pos'].cart = cart_data
                self.modules['pos'].load_cart_to_ui()
                # Delete from held bills
                self.db.execute("DELETE FROM held_bills WHERE id = ?", (bill_id,))
                dialog.close()
                self.stacked_widget.setCurrentWidget(self.modules['pos'])
                QMessageBox.information(self, 'Success', 'Bill reopened! You can now edit and save it')
        except Exception as e:
            import traceback
            print(f"Error reopening bill: {traceback.format_exc()}")
            QMessageBox.critical(self, 'Error', f'Failed to reopen bill: {str(e)}')
    
    def delete_held_bill(self, bill_id, table, row):
        """Delete a held bill."""
        try:
            if QMessageBox.question(self, 'Confirm Delete', 'Delete this held bill?') == QMessageBox.StandardButton.Yes:
                self.db.execute("DELETE FROM held_bills WHERE id = ?", (bill_id,))
                table.removeRow(row)
                QMessageBox.information(self, 'Success', 'Held bill deleted')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to delete bill: {str(e)}')
    
    def do_logout(self):
        """Logout current user."""
        self.db.log_activity(self.current_user['id'], self.current_user['username'], 'LOGOUT', 'User logged out')
        self.current_user = None
        self.modules = {}
        self.show_login()

# ==================== MAIN ====================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PharmacyPOSApp()
    window.show()
    sys.exit(app.exec())


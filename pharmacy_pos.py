#!/usr/bin/env python3
"""
Pharmacy POS System - Fatima Tu Zahra Medical Centre
Professional Point of Sale System with Role-Based Access Control
Supports: Dashboard, Sales, Inventory, Bills History, User Management, Activity Logs
"""

import sys
import sqlite3
import json
from datetime import datetime, timedelta
from decimal import Decimal

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QMessageBox, QStackedWidget, QHeaderView, QFrame, QTabWidget,
    QInputDialog, QDialog, QFormLayout, QComboBox, QSpinBox,
    QDoubleSpinBox, QDateEdit, QTextEdit, QScrollArea, QGridLayout,
    QTreeWidget, QTreeWidgetItem, QCheckBox, QGroupBox,
    QMenuBar, QMenu, QStatusBar, QSplitter, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QDate, QDateTime, QSize, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QFont, QPixmap, QColor, QIcon, QTextDocument, QTextCursor,
    QTextFormat, QPalette, QBrush
)
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QAction

# --- ENHANCED DATABASE ---
class PharmacyDB:
    def __init__(self):
        # Using a new filename to ensure a fresh, clean start
        self.conn = sqlite3.connect("hospital_management_v3.db")
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        # 1. Create Users Table (THIS WAS MISSING)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)""")
            
        # 2. Create Medicines Table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS medicines 
            (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)""")
            
        # 3. Create Demand/Shortage Table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS demand 
            (id INTEGER PRIMARY KEY, med_name TEXT, request_count INTEGER, date TEXT)""")
            
        # 4. Create Sales Table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sales 
            (id INTEGER PRIMARY KEY, date TEXT, total REAL)""")
        
        # 5. Create Bills History Table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS bills 
            (id INTEGER PRIMARY KEY, date TEXT, items TEXT, total REAL)""")
        
        # 6. Create Activity Logs Table (Login/Logout events)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS activity_logs 
            (id INTEGER PRIMARY KEY, username TEXT, action TEXT, timestamp TEXT)""")
        
        # 7. Insert default admin
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin')")
        
        self.conn.commit()

class ModernPharmacyPOS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = PharmacyDB()
        self.cart = []
        self.current_user = None
        self.current_role = None
        self.setWindowTitle("FATIMA TU ZAHRA MEDICAL CENTRE Pharmacy - Advanced POS & Stock Management")
        self.setMinimumSize(1250, 850)
        self.setStyleSheet(self.get_global_stylesheet())
        
        # UI Stack
        self.main_stack = QStackedWidget()
        self.setCentralWidget(self.main_stack)
        self.init_login()

    def get_global_stylesheet(self):
        return """
            QMainWindow {
                background-color: #f5f6fa;
            }
            
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #f0f8ff;
            }
            
            QPushButton {
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            
            QPushButton:hover {
                opacity: 0.9;
            }
            
            QPushButton:pressed {
                opacity: 0.8;
            }
            
            QLabel {
                color: #2c3e50;
                font-family: 'Segoe UI', Arial;
            }
            
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                gridline-color: #ecf0f1;
            }
            
            QTableWidget::item {
                padding: 5px;
            }
            
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            
            QMessageBox {
                background-color: white;
            }
            
            QMessageBox QLabel {
                color: #2c3e50;
            }
            
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
            }
            
            QTabBar::tab {
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 8px 20px;
                border: 1px solid #bdc3c7;
            }
            
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
        """

    def init_login(self):
        login_page = QWidget()
        layout = QVBoxLayout(login_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("🏥 FATIMA TU ZAHRA PHARMACY\nLogin")
        title.setStyleSheet("font-size: 22px; font-weight: bold; text-align: center; padding: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Login Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        user_label = QLabel("Username:")
        self.login_user = QLineEdit()
        self.login_user.setMinimumWidth(300)
        self.login_user.setText("admin")  # Pre-fill admin
        self.login_user.returnPressed.connect(self.handle_login)  # Enter key to login
        
        pass_label = QLabel("Password:")
        self.login_pass = QLineEdit()
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_pass.setMinimumWidth(300)
        self.login_pass.setText("admin123")  # Pre-fill password
        self.login_pass.returnPressed.connect(self.handle_login)  # Enter key to login
        
        form_layout.addWidget(user_label)
        form_layout.addWidget(self.login_user)
        form_layout.addWidget(pass_label)
        form_layout.addWidget(self.login_pass)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        login_btn = QPushButton("🔓 Login (or press Enter)")
        login_btn.setFixedWidth(200)
        login_btn.setStyleSheet("background: #27ae60; color: white; height: 40px; font-size: 14px;")
        login_btn.clicked.connect(self.handle_login)
        
        btn_layout.addWidget(login_btn)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        self.main_stack.addWidget(login_page)
        self.main_stack.setCurrentIndex(0)

    def handle_login(self):
        username = self.login_user.text()
        password = self.login_pass.text()
        
        self.db.cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        result = self.db.cursor.fetchone()
        
        if result:
            self.current_user = username
            self.current_role = result[0]
            
            # Log the login event
            self.db.cursor.execute(
                "INSERT INTO activity_logs (username, action, timestamp) VALUES (?, ?, ?)",
                (username, "LOGIN", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.db.conn.commit()
            
            self.init_dashboard()
            self.main_stack.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")

    def init_dashboard(self):
        main_page = QWidget()
        layout = QHBoxLayout(main_page)

        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background: #1a2a3a; color: white;")
        s_layout = QVBoxLayout(sidebar)

        # Logo and Hospital Name Section
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add Logo
        logo_label = QLabel()
        try:
            logo_pixmap = QPixmap("logo.jpg")
            scaled_logo = logo_pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_logo)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except:
            logo_label.setText("[Logo not found]")
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)
        
        # Professional Branding with Hospital Name
        hospital_lbl = QLabel("🏥 FATIMA TU ZAHRA \nPHARMACY")
        hospital_lbl.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px; text-align: center;")
        hospital_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(hospital_lbl)
        
        s_layout.addWidget(header_widget)
        
        # Current User Info
        user_info = QLabel(f"👤 {self.current_user}\n({self.current_role.upper()})")
        user_info.setStyleSheet("font-size: 12px; padding: 10px; background: #0d1b2a; border-radius: 5px;")
        s_layout.addWidget(user_info)

        btn_pos = QPushButton("🛒 POS / Billing")
        btn_restock = QPushButton("⚠️ Restock & Demand")
        btn_history = QPushButton("📋 Bills History")
        
        buttons = [btn_pos, btn_restock, btn_history]
        
        # Admin-only buttons
        if self.current_role == "admin":
            btn_inv = QPushButton("📦 Inventory Management")
            btn_users = QPushButton("👥 Manage Users")
            btn_logs = QPushButton("📜 Activity Logs")
            btn_sales = QPushButton("📊 Daily Sales Report")
            buttons.insert(1, btn_inv)
            buttons.append(btn_users)
            buttons.append(btn_logs)
            buttons.append(btn_sales)
        
        for b in buttons:
            b.setStyleSheet("text-align: left; padding: 15px; color: #ecf0f1; border: none; font-size: 14px;")
            s_layout.addWidget(b)
        
        # Connect buttons
        btn_pos.clicked.connect(lambda: self.sub_stack.setCurrentIndex(0))
        btn_restock.clicked.connect(self.load_restock_data)
        btn_history.clicked.connect(self.load_bill_history)
        
        if self.current_role == "admin":
            buttons[1].clicked.connect(lambda: self.sub_stack.setCurrentIndex(1))
            buttons[-3].clicked.connect(lambda: self.sub_stack.setCurrentIndex(4))
            buttons[-2].clicked.connect(self.load_activity_logs)
            buttons[-1].clicked.connect(self.load_daily_sales)
        
        s_layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet("background: #e74c3c; color: white; padding: 10px;")
        logout_btn.clicked.connect(self.handle_logout)
        s_layout.addWidget(logout_btn)
        
        layout.addWidget(sidebar)

        # --- SUB-PAGES ---
        self.sub_stack = QStackedWidget()
        self.sub_stack.addWidget(self.ui_pos())
        
        if self.current_role == "admin":
            self.sub_stack.addWidget(self.ui_inventory())
        
        self.sub_stack.addWidget(self.ui_restock())
        self.sub_stack.addWidget(self.ui_bill_history())
        
        if self.current_role == "admin":
            self.sub_stack.addWidget(self.ui_manage_users())
            self.sub_stack.addWidget(self.ui_activity_logs())
            self.sub_stack.addWidget(self.ui_daily_sales())
        
        layout.addWidget(self.sub_stack)
        self.main_stack.addWidget(main_page)

    def handle_logout(self):
        # Log the logout event
        self.db.cursor.execute(
            "INSERT INTO activity_logs (username, action, timestamp) VALUES (?, ?, ?)",
            (self.current_user, "LOGOUT", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.db.conn.commit()
        
        self.current_user = None
        self.current_role = None
        self.login_user.clear()
        self.login_pass.clear()
        self.main_stack.setCurrentIndex(0)

    # --- FEATURE 1: POS / BILLING ---
    def ui_pos(self):
        page = QWidget()
        page.setStyleSheet("background-color: #f5f6fa;")
        layout = QHBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Left Section - Medicine Finder
        left = QVBoxLayout()
        
        finder_title = QLabel("🔍 Medicine Finder")
        finder_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; padding-bottom: 10px;")
        left.addWidget(finder_title)
        
        self.pos_search = QLineEdit()
        self.pos_search.setPlaceholderText("🔎 Search by medicine name...")
        self.pos_search.setMinimumHeight(40)
        self.pos_search.textChanged.connect(self.refresh_pos_list)
        left.addWidget(self.pos_search)
        
        self.pos_table = QTableWidget(0, 4)
        self.pos_table.setHorizontalHeaderLabels(["ID", "Medicine Name", "Stock", "Price (Rs.)"])
        self.pos_table.setColumnWidth(1, 150)
        self.pos_table.doubleClicked.connect(self.add_to_cart)
        self.pos_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; }")
        left.addWidget(self.pos_table)
        
        # New Feature: Add to Shortage Button
        demand_btn = QPushButton("📝 Record Not-in-Stock Demand")
        demand_btn.setMinimumHeight(40)
        demand_btn.clicked.connect(self.record_demand)
        demand_btn.setStyleSheet("background: #f39c12; color: white; font-weight: bold; border-radius: 5px;")
        left.addWidget(demand_btn)

        # Right Section - Current Bill
        right = QVBoxLayout()
        
        bill_title = QLabel("🧾 Current Bill")
        bill_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; padding-bottom: 10px;")
        right.addWidget(bill_title)
        
        self.cart_table = QTableWidget(0, 3)
        self.cart_table.setHorizontalHeaderLabels(["Item", "Qty", "Subtotal (Rs.)"])
        self.cart_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; }")
        right.addWidget(self.cart_table)
        
        self.total_lbl = QLabel("Total: Rs.0.00")
        self.total_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #27ae60; text-align: center; padding: 15px; background: #d5f4e6; border-radius: 5px;")
        self.total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right.addWidget(self.total_lbl)
        
        print_btn = QPushButton("✓ COMPLETE SALE")
        print_btn.setMinimumHeight(60)
        print_btn.setStyleSheet("background: #27ae60; color: white; font-size: 13px; font-weight: bold; border-radius: 5px;")
        print_btn.clicked.connect(self.finalize_sale)
        right.addWidget(print_btn)
        
        layout.addLayout(left, 2)
        layout.addLayout(right, 1)
        self.refresh_pos_list()
        return page

    # --- FEATURE 2: INVENTORY WITH PLUS/MINUS ---
    def ui_inventory(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Admin only warning (this page is only added for admin, but safety check)
        if self.current_role != "admin":
            warning = QLabel("❌ Admin Access Only!")
            warning.setStyleSheet("color: red; font-weight: bold; font-size: 16px;")
            layout.addWidget(warning)
            return page

        # Title
        title = QLabel("📦 Inventory Management")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; color: #2c3e50;")
        layout.addWidget(title)

        # Action buttons layout
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add New Medicine")
        add_btn.setStyleSheet("background: #27ae60; color: white; padding: 10px; font-size: 12px; font-weight: bold; border-radius: 5px;")
        add_btn.clicked.connect(self.show_add_medicine_dialog)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Inventory Table with better styling
        self.inv_table = QTableWidget(0, 6)
        self.inv_table.setHorizontalHeaderLabels(["ID", "Medicine Name", "Stock", "Price (Rs.)", "Status", "Actions"])
        self.inv_table.setColumnWidth(1, 200)
        self.inv_table.setColumnWidth(4, 120)
        self.inv_table.setColumnWidth(5, 150)
        self.inv_table.horizontalHeader().setStyleSheet("background-color: #34495e; color: white; font-weight: bold; padding: 5px;")
        self.inv_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; } QTableWidgetItem { padding: 5px; }")
        layout.addWidget(self.inv_table)
        
        self.refresh_inv_list()
        return page

    def show_add_medicine_dialog(self):
        dialog = QWidget()
        dialog.setWindowTitle("Add New Medicine")
        dialog.setGeometry(400, 200, 500, 450)
        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Add New Medicine to Inventory")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Form fields
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        # Medicine Name
        name_label = QLabel("Medicine Name:")
        name_label.setStyleSheet("font-weight: bold; color: #34495e;")
        name_input = QLineEdit()
        name_input.setPlaceholderText("e.g., Aspirin, Paracetamol...")
        name_input.setMinimumHeight(35)
        form_layout.addWidget(name_label)
        form_layout.addWidget(name_input)
        
        # Price
        price_label = QLabel("Price (₨):")
        price_label.setStyleSheet("font-weight: bold; color: #34495e;")
        price_input = QLineEdit()
        price_input.setPlaceholderText("e.g., 150.50")
        price_input.setMinimumHeight(35)
        form_layout.addWidget(price_label)
        form_layout.addWidget(price_input)
        
        # Stock
        stock_label = QLabel("Stock Quantity:")
        stock_label.setStyleSheet("font-weight: bold; color: #34495e;")
        stock_input = QLineEdit()
        stock_input.setPlaceholderText("e.g., 100")
        stock_input.setMinimumHeight(35)
        form_layout.addWidget(stock_label)
        form_layout.addWidget(stock_input)
        
        layout.addLayout(form_layout)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("✓ Save Medicine (or press Enter)")
        save_btn.setStyleSheet("background: #27ae60; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        save_btn.setMinimumHeight(40)
        
        cancel_btn = QPushButton("✕ Cancel")
        cancel_btn.setStyleSheet("background: #95a5a6; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        cancel_btn.setMinimumHeight(40)
        
        def save_medicine():
            name = name_input.text().strip()
            price_text = price_input.text().strip()
            stock_text = stock_input.text().strip()
            
            # Validation
            if not name:
                QMessageBox.warning(dialog, "Validation Error", "Please enter medicine name!")
                return
            
            if not price_text:
                QMessageBox.warning(dialog, "Validation Error", "Please enter price!")
                return
            
            if not stock_text:
                QMessageBox.warning(dialog, "Validation Error", "Please enter stock quantity!")
                return
            
            try:
                price = float(price_text)
                stock = int(stock_text)
                
                if price < 0:
                    QMessageBox.warning(dialog, "Validation Error", "Price cannot be negative!")
                    return
                
                if stock < 0:
                    QMessageBox.warning(dialog, "Validation Error", "Stock cannot be negative!")
                    return
                
                # Add to database
                self.db.cursor.execute(
                    "INSERT INTO medicines (name, price, stock) VALUES (?, ?, ?)",
                    (name, price, stock)
                )
                self.db.conn.commit()
                
                QMessageBox.information(dialog, "Success", f"Medicine '{name}' added successfully!")
                self.refresh_inv_list()
                dialog.close()
                
            except ValueError:
                QMessageBox.warning(dialog, "Validation Error", "Price must be a number and stock must be an integer!")
        
        # Add Enter key handlers to all input fields
        name_input.returnPressed.connect(save_medicine)
        price_input.returnPressed.connect(save_medicine)
        stock_input.returnPressed.connect(save_medicine)
        
        save_btn.clicked.connect(save_medicine)
        cancel_btn.clicked.connect(dialog.close)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        dialog.show()

    def refresh_inv_list(self):
        self.db.cursor.execute("SELECT * FROM medicines")
        rows = self.db.cursor.fetchall()
        self.inv_table.setRowCount(0)
        for r in rows:
            pos = self.inv_table.rowCount()
            self.inv_table.insertRow(pos)
            
            # ID
            self.inv_table.setItem(pos, 0, QTableWidgetItem(str(r[0])))
            
            # Medicine Name
            self.inv_table.setItem(pos, 1, QTableWidgetItem(r[1]))
            
            # Stock
            stock_item = QTableWidgetItem(str(r[3]))
            if r[3] < 10:
                stock_item.setBackground(QColor("#fadbd8"))  # Red background for low stock
            elif r[3] < 20:
                stock_item.setBackground(QColor("#ffeaa7"))  # Yellow background for warning
            else:
                stock_item.setBackground(QColor("#d5f4e6"))  # Green for good stock
            self.inv_table.setItem(pos, 2, stock_item)
            
            # Price
            price_item = QTableWidgetItem(f"Rs.{r[2]:.2f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.inv_table.setItem(pos, 3, price_item)
            
            # Status
            if r[3] < 10:
                status = "⚠️ LOW STOCK"
                status_color = "#e74c3c"
            elif r[3] < 20:
                status = "⚡ MEDIUM"
                status_color = "#f39c12"
            else:
                status = "✓ GOOD"
                status_color = "#27ae60"
            
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor(status_color))
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.inv_table.setItem(pos, 4, status_item)
            
            # Action buttons (Edit and Delete)
            action_layout = QHBoxLayout()
            action_widget = QWidget()
            
            edit_btn = QPushButton("✏️ Edit")
            edit_btn.setStyleSheet("background: #3498db; color: white; padding: 5px; font-size: 11px; border-radius: 3px;")
            edit_btn.setMaximumWidth(70)
            edit_btn.clicked.connect(lambda _, med_id=r[0], name=r[1], price=r[2], stock=r[3]: 
                                    self.show_edit_medicine_dialog(med_id, name, price, stock))
            
            del_btn = QPushButton("🗑️ Delete")
            del_btn.setStyleSheet("background: #e74c3c; color: white; padding: 5px; font-size: 11px; border-radius: 3px;")
            del_btn.setMaximumWidth(75)
            del_btn.clicked.connect(lambda _, med_id=r[0], name=r[1]: self.delete_med(med_id, name))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(del_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)
            action_widget.setLayout(action_layout)
            self.inv_table.setCellWidget(pos, 5, action_widget)

    def show_edit_medicine_dialog(self, med_id, name, price, stock):
        dialog = QWidget()
        dialog.setWindowTitle("Edit Medicine")
        dialog.setGeometry(400, 200, 500, 450)
        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel(f"Edit Medicine: {name}")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Form fields
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        # Medicine Name
        name_label = QLabel("Medicine Name:")
        name_label.setStyleSheet("font-weight: bold; color: #34495e;")
        name_input = QLineEdit()
        name_input.setText(name)
        name_input.setMinimumHeight(35)
        form_layout.addWidget(name_label)
        form_layout.addWidget(name_input)
        
        # Price
        price_label = QLabel("Price (Rs.):")
        price_label.setStyleSheet("font-weight: bold; color: #34495e;")
        price_input = QLineEdit()
        price_input.setText(str(price))
        price_input.setMinimumHeight(35)
        form_layout.addWidget(price_label)
        form_layout.addWidget(price_input)
        
        # Stock
        stock_label = QLabel("Stock Quantity:")
        stock_label.setStyleSheet("font-weight: bold; color: #34495e;")
        stock_input = QLineEdit()
        stock_input.setText(str(stock))
        stock_input.setMinimumHeight(35)
        form_layout.addWidget(stock_label)
        form_layout.addWidget(stock_input)
        
        layout.addLayout(form_layout)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("✓ Update Medicine")
        save_btn.setStyleSheet("background: #27ae60; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        save_btn.setMinimumHeight(40)
        
        cancel_btn = QPushButton("✕ Cancel")
        cancel_btn.setStyleSheet("background: #95a5a6; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        cancel_btn.setMinimumHeight(40)
        
        def update_medicine():
            upd_name = name_input.text().strip()
            upd_price_text = price_input.text().strip()
            upd_stock_text = stock_input.text().strip()
            
            # Validation
            if not upd_name:
                QMessageBox.warning(dialog, "Validation Error", "Please enter medicine name!")
                return
            
            if not upd_price_text:
                QMessageBox.warning(dialog, "Validation Error", "Please enter price!")
                return
            
            if not upd_stock_text:
                QMessageBox.warning(dialog, "Validation Error", "Please enter stock quantity!")
                return
            
            try:
                upd_price = float(upd_price_text)
                upd_stock = int(upd_stock_text)
                
                if upd_price < 0:
                    QMessageBox.warning(dialog, "Validation Error", "Price cannot be negative!")
                    return
                
                if upd_stock < 0:
                    QMessageBox.warning(dialog, "Validation Error", "Stock cannot be negative!")
                    return
                
                # Update database
                self.db.cursor.execute(
                    "UPDATE medicines SET name = ?, price = ?, stock = ? WHERE id = ?",
                    (upd_name, upd_price, upd_stock, med_id)
                )
                self.db.conn.commit()
                
                QMessageBox.information(dialog, "Success", f"Medicine '{upd_name}' updated successfully!")
                self.refresh_inv_list()
                dialog.close()
                
            except ValueError:
                QMessageBox.warning(dialog, "Validation Error", "Price must be a number and stock must be an integer!")
        
        # Add Enter key handlers to all input fields
        name_input.returnPressed.connect(update_medicine)
        price_input.returnPressed.connect(update_medicine)
        stock_input.returnPressed.connect(update_medicine)
        
        save_btn.clicked.connect(update_medicine)
        cancel_btn.clicked.connect(dialog.close)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        dialog.show()

    # --- FEATURE 3: RESTOCK & DEMAND ---
    def ui_restock(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Tabs for separating automated shortage vs user-recorded demand
        tabs = QTabWidget()
        
        # 1. Automated Restock (Low Stock Alert)
        self.restock_table = QTableWidget(0, 3)
        self.restock_table.setHorizontalHeaderLabels(["Medicine", "Current Stock", "Status"])
        tabs.addTab(self.restock_table, "⚠️ Low Stock Alert")
        
        # 2. Demand Tracker (What customers asked for)
        self.demand_table = QTableWidget(0, 3)
        self.demand_table.setHorizontalHeaderLabels(["Medicine Name", "Request Count", "Last Requested"])
        tabs.addTab(self.demand_table, "📝 Shortage / Demand Book")
        
        layout.addWidget(QLabel("Supply Chain Management"))
        layout.addWidget(tabs)
        return page

    # --- FEATURE 4: BILL HISTORY ---
    def ui_bill_history(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("📋 Bills History")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Search/Filter
        search_layout = QHBoxLayout()
        self.history_search = QLineEdit()
        self.history_search.setPlaceholderText("Search by date (YYYY-MM-DD) or medicine name...")
        self.history_search.textChanged.connect(self.refresh_bill_history)
        search_layout.addWidget(self.history_search)
        layout.addLayout(search_layout)
        
        # Bill History Table
        self.bill_history_table = QTableWidget(0, 4)
        self.bill_history_table.setHorizontalHeaderLabels(["Bill ID", "Date", "Items", "Total"])
        self.bill_history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.bill_history_table)
        
        # Clear History Button
        clear_btn = QPushButton("🗑️ Clear Old History (30+ days)")
        clear_btn.clicked.connect(self.clear_old_history)
        clear_btn.setStyleSheet("background: #e74c3c; color: white;")
        layout.addWidget(clear_btn)
        
        return page

    def load_bill_history(self):
        self.sub_stack.setCurrentIndex(3)
        self.refresh_bill_history()

    def refresh_bill_history(self):
        search = self.history_search.text()
        if search:
            self.db.cursor.execute(
                "SELECT id, date, items, total FROM bills WHERE date LIKE ? OR items LIKE ? ORDER BY date DESC",
                (f'%{search}%', f'%{search}%')
            )
        else:
            self.db.cursor.execute("SELECT id, date, items, total FROM bills ORDER BY date DESC")
        
        rows = self.db.cursor.fetchall()
        self.bill_history_table.setRowCount(0)
        
        for r in rows:
            pos = self.bill_history_table.rowCount()
            self.bill_history_table.insertRow(pos)
            self.bill_history_table.setItem(pos, 0, QTableWidgetItem(str(r[0])))
            self.bill_history_table.setItem(pos, 1, QTableWidgetItem(r[1]))
            self.bill_history_table.setItem(pos, 2, QTableWidgetItem(r[2]))
            self.bill_history_table.setItem(pos, 3, QTableWidgetItem(f"Rs.{r[3]:.2f}"))

    def clear_old_history(self):
        from datetime import timedelta
        old_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        reply = QMessageBox.question(self, "Confirm", f"Clear bills older than {old_date}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.cursor.execute("DELETE FROM bills WHERE date < ?", (old_date,))
            self.db.conn.commit()
            self.refresh_bill_history()
            QMessageBox.information(self, "Success", "Old bills cleared.")

    # --- FEATURE 5: USER MANAGEMENT (ADMIN ONLY) ---
    def ui_manage_users(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("👥 User Management (Admin Only)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Add new user form
        form_layout = QHBoxLayout()
        self.new_user_field = QLineEdit()
        self.new_user_field.setPlaceholderText("New username...")
        self.new_user_field.setMaximumWidth(150)
        
        self.new_pass_field = QLineEdit()
        self.new_pass_field.setPlaceholderText("Password...")
        self.new_pass_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pass_field.setMaximumWidth(150)
        
        self.new_role_field = QLineEdit()
        self.new_role_field.setText("user")
        self.new_role_field.setPlaceholderText("Role: user or admin")
        self.new_role_field.setMaximumWidth(150)
        
        add_user_btn = QPushButton("➕ Add User")
        add_user_btn.setStyleSheet("background: #27ae60; color: white;")
        add_user_btn.clicked.connect(self.add_new_user)
        
        form_layout.addWidget(QLabel("Username:"))
        form_layout.addWidget(self.new_user_field)
        form_layout.addWidget(QLabel("Password:"))
        form_layout.addWidget(self.new_pass_field)
        form_layout.addWidget(QLabel("Role:"))
        form_layout.addWidget(self.new_role_field)
        form_layout.addWidget(add_user_btn)
        form_layout.addStretch()
        layout.addLayout(form_layout)
        
        # Users table
        self.users_table = QTableWidget(0, 4)
        self.users_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Action"])
        layout.addWidget(self.users_table)
        
        self.refresh_users_list()
        return page

    def refresh_users_list(self):
        self.db.cursor.execute("SELECT id, username, role FROM users")
        rows = self.db.cursor.fetchall()
        self.users_table.setRowCount(0)
        
        for r in rows:
            pos = self.users_table.rowCount()
            self.users_table.insertRow(pos)
            self.users_table.setItem(pos, 0, QTableWidgetItem(str(r[0])))
            self.users_table.setItem(pos, 1, QTableWidgetItem(r[1]))
            self.users_table.setItem(pos, 2, QTableWidgetItem(r[2]))
            
            del_btn = QPushButton("❌ Delete")
            del_btn.clicked.connect(lambda _, uid=r[0], uname=r[1]: self.delete_user(uid, uname))
            self.users_table.setCellWidget(pos, 3, del_btn)

    def add_new_user(self):
        username = self.new_user_field.text()
        password = self.new_pass_field.text()
        role = self.new_role_field.text()
        
        if not all([username, password, role]):
            QMessageBox.warning(self, "Error", "Please fill all fields!")
            return
        
        if role not in ["user", "admin"]:
            QMessageBox.warning(self, "Error", "Role must be 'user' or 'admin'!")
            return
        
        try:
            self.db.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                 (username, password, role))
            self.db.conn.commit()
            QMessageBox.information(self, "Success", f"User '{username}' added as {role}!")
            self.new_user_field.clear()
            self.new_pass_field.clear()
            self.new_role_field.setText("user")
            self.refresh_users_list()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists!")

    def delete_user(self, user_id, username):
        if username == self.current_user:
            QMessageBox.warning(self, "Error", "Cannot delete your own account!")
            return
        
        reply = QMessageBox.question(self, "Confirm", f"Delete user '{username}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.db.conn.commit()
            self.refresh_users_list()
            QMessageBox.information(self, "Success", "User deleted!")

    # --- FEATURE 6: ACTIVITY LOGS (ADMIN ONLY) ---
    def ui_activity_logs(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("📜 Activity Logs (Admin Only)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Filter options
        filter_layout = QHBoxLayout()
        self.logs_search = QLineEdit()
        self.logs_search.setPlaceholderText("Search by username or action (LOGIN/LOGOUT)...")
        self.logs_search.textChanged.connect(self.refresh_activity_logs)
        
        clear_logs_btn = QPushButton("🗑️ Clear All Logs")
        clear_logs_btn.setStyleSheet("background: #e74c3c; color: white;")
        clear_logs_btn.clicked.connect(self.clear_all_logs)
        
        filter_layout.addWidget(self.logs_search)
        filter_layout.addWidget(clear_logs_btn)
        layout.addLayout(filter_layout)
        
        # Activity Logs Table
        self.activity_logs_table = QTableWidget(0, 4)
        self.activity_logs_table.setHorizontalHeaderLabels(["ID", "Username", "Action", "Timestamp"])
        self.activity_logs_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.activity_logs_table)
        
        self.refresh_activity_logs()
        return page

    def load_activity_logs(self):
        self.sub_stack.setCurrentIndex(5)
        self.refresh_activity_logs()

    def refresh_activity_logs(self):
        search = self.logs_search.text()
        if search:
            self.db.cursor.execute(
                "SELECT id, username, action, timestamp FROM activity_logs WHERE username LIKE ? OR action LIKE ? ORDER BY id DESC",
                (f'%{search}%', f'%{search}%')
            )
        else:
            self.db.cursor.execute("SELECT id, username, action, timestamp FROM activity_logs ORDER BY id DESC")
        
        rows = self.db.cursor.fetchall()
        self.activity_logs_table.setRowCount(0)
        
        for r in rows:
            pos = self.activity_logs_table.rowCount()
            self.activity_logs_table.insertRow(pos)
            self.activity_logs_table.setItem(pos, 0, QTableWidgetItem(str(r[0])))
            self.activity_logs_table.setItem(pos, 1, QTableWidgetItem(r[1]))
            
            # Color code actions
            action_item = QTableWidgetItem(r[2])
            if r[2] == "LOGIN":
                action_item.setBackground(QColor("#d5f4e6"))
                action_item.setForeground(QColor("#27ae60"))
            elif r[2] == "LOGOUT":
                action_item.setBackground(QColor("#fadbd8"))
                action_item.setForeground(QColor("#e74c3c"))
            self.activity_logs_table.setItem(pos, 2, action_item)
            
            self.activity_logs_table.setItem(pos, 3, QTableWidgetItem(r[3]))

    def clear_all_logs(self):
        reply = QMessageBox.question(
            self, "Confirm", "Are you sure you want to clear all activity logs? This cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.cursor.execute("DELETE FROM activity_logs")
            self.db.conn.commit()
            self.refresh_activity_logs()
            QMessageBox.information(self, "Success", "All activity logs have been cleared.")

    # --- FEATURE 7: DAILY SALES REPORT (ADMIN ONLY) ---
    def ui_daily_sales(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("📊 Daily Sales Report")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Summary Stats
        stats_layout = QHBoxLayout()
        
        self.total_sales_lbl = QLabel("Total Sales Today: $0.00")
        self.total_sales_lbl.setStyleSheet("font-size: 14px; padding: 10px; background: #d5f4e6; border-radius: 5px; min-width: 200px;")
        
        self.transaction_count_lbl = QLabel("Total Transactions: 0")
        self.transaction_count_lbl.setStyleSheet("font-size: 14px; padding: 10px; background: #dfe6e9; border-radius: 5px; min-width: 200px;")
        
        self.avg_transaction_lbl = QLabel("Avg per Transaction: $0.00")
        self.avg_transaction_lbl.setStyleSheet("font-size: 14px; padding: 10px; background: #ffeaa7; border-radius: 5px; min-width: 200px;")
        
        stats_layout.addWidget(self.total_sales_lbl)
        stats_layout.addWidget(self.transaction_count_lbl)
        stats_layout.addWidget(self.avg_transaction_lbl)
        layout.addLayout(stats_layout)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh Sales Data")
        refresh_btn.setStyleSheet("background: #3498db; color: white;")
        refresh_btn.clicked.connect(self.refresh_daily_sales)
        layout.addWidget(refresh_btn)
        
        # Daily Sales Table
        self.daily_sales_table = QTableWidget(0, 4)
        self.daily_sales_table.setHorizontalHeaderLabels(["Transaction ID", "Time", "Items", "Amount"])
        self.daily_sales_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.daily_sales_table)
        
        self.refresh_daily_sales()
        return page

    def load_daily_sales(self):
        self.sub_stack.setCurrentIndex(6)
        self.refresh_daily_sales()

    def refresh_daily_sales(self):
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get today's sales
        self.db.cursor.execute(
            "SELECT id, date, items, total FROM bills WHERE date LIKE ? ORDER BY date DESC",
            (f'{today}%',)
        )
        rows = self.db.cursor.fetchall()
        
        # Calculate statistics
        total_sales = sum(row[3] for row in rows)
        transaction_count = len(rows)
        avg_transaction = total_sales / transaction_count if transaction_count > 0 else 0
        
        # Update summary labels
        self.total_sales_lbl.setText(f"💰 Total Sales Today: ${total_sales:.2f}")
        self.transaction_count_lbl.setText(f"🛍️ Total Transactions: {transaction_count}")
        self.avg_transaction_lbl.setText(f"📈 Avg per Transaction: ${avg_transaction:.2f}")
        
        # Populate table
        self.daily_sales_table.setRowCount(0)
        for r in rows:
            pos = self.daily_sales_table.rowCount()
            self.daily_sales_table.insertRow(pos)
            
            # Bill ID
            self.daily_sales_table.setItem(pos, 0, QTableWidgetItem(str(r[0])))
            
            # Time (extract from datetime)
            time_str = r[1].split(" ")[1] if " " in r[1] else r[1]
            self.daily_sales_table.setItem(pos, 1, QTableWidgetItem(time_str))
            
            # Items
            self.daily_sales_table.setItem(pos, 2, QTableWidgetItem(r[2]))
            
            # Amount
            amount_item = QTableWidgetItem(f"Rs.{r[3]:.2f}")
            amount_item.setBackground(QColor("#d5f4e6"))
            self.daily_sales_table.setItem(pos, 3, amount_item)

    def load_restock_data(self):
        self.sub_stack.setCurrentIndex(2)
        # Load Low Stock
        self.db.cursor.execute("SELECT name, stock FROM medicines WHERE stock < 10")
        rows = self.db.cursor.fetchall()
        self.restock_table.setRowCount(0)
        for r in rows:
            pos = self.restock_table.rowCount()
            self.restock_table.insertRow(pos)
            self.restock_table.setItem(pos, 0, QTableWidgetItem(r[0]))
            self.restock_table.setItem(pos, 1, QTableWidgetItem(str(r[1])))
            self.restock_table.setItem(pos, 2, QTableWidgetItem("CRITICAL"))

        # Load Demand
        self.db.cursor.execute("SELECT med_name, request_count, date FROM demand")
        rows = self.db.cursor.fetchall()
        self.demand_table.setRowCount(0)
        for r in rows:
            pos = self.demand_table.rowCount()
            self.demand_table.insertRow(pos)
            for i, val in enumerate(r):
                self.demand_table.setItem(pos, i, QTableWidgetItem(str(val)))

    def record_demand(self):
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "New Demand", "Medicine Name requested by customer:")
        if ok and name:
            self.db.cursor.execute("SELECT id FROM demand WHERE med_name = ?", (name,))
            res = self.db.cursor.fetchone()
            if res:
                self.db.cursor.execute("UPDATE demand SET request_count = request_count + 1 WHERE med_name = ?", (name,))
            else:
                self.db.cursor.execute("INSERT INTO demand (med_name, request_count, date) VALUES (?, 1, ?)", 
                                       (name, datetime.now().strftime("%Y-%m-%d")))
            self.db.conn.commit()
            QMessageBox.information(self, "Recorded", f"Demand for {name} has been added to the Restock List.")

    # (Logic for finalize_sale and print_receipt would be same as previous refined version)
    # ... rest of the code logic ...

    def add_new_med(self):
        # Deprecated - using dialog instead
        pass

    def delete_med(self, med_id, med_name):
        reply = QMessageBox.question(
            self, "Confirm Deletion", 
            f"Are you sure you want to delete '{med_name}'?\n\nThis action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.cursor.execute("DELETE FROM medicines WHERE id = ?", (med_id,))
                self.db.conn.commit()
                QMessageBox.information(self, "Success", f"Medicine '{med_name}' has been deleted successfully!")
                self.refresh_inv_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete medicine: {str(e)}")

    def refresh_pos_list(self):
        # Implementation of Search
        search = self.pos_search.text()
        self.db.cursor.execute("SELECT * FROM medicines WHERE name LIKE ?", (f'%{search}%',))
        rows = self.db.cursor.fetchall()
        self.pos_table.setRowCount(0)
        for r in rows:
            pos = self.pos_table.rowCount()
            self.pos_table.insertRow(pos)
            
            # ID (read-only)
            id_item = QTableWidgetItem(str(r[0]))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.pos_table.setItem(pos, 0, id_item)
            
            # Medicine Name (read-only)
            name_item = QTableWidgetItem(r[1])
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.pos_table.setItem(pos, 1, name_item)
            
            # Stock with color coding (read-only)
            stock_item = QTableWidgetItem(str(r[3]))
            stock_item.setFlags(stock_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if r[3] < 5:
                stock_item.setBackground(QColor("#fadbd8"))  # Red
            elif r[3] < 15:
                stock_item.setBackground(QColor("#ffeaa7"))  # Yellow
            else:
                stock_item.setBackground(QColor("#d5f4e6"))  # Green
            self.pos_table.setItem(pos, 2, stock_item)
            
            # Price (read-only)
            price_item = QTableWidgetItem(f"Rs.{r[2]:.2f}")
            price_item.setFlags(price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.pos_table.setItem(pos, 3, price_item)

    def add_to_cart(self):
        row = self.pos_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a medicine first!")
            return
        
        name = self.pos_table.item(row, 1).text()
        price_text = self.pos_table.item(row, 3).text().replace("Rs.", "").strip()
        
        try:
            price = float(price_text)
            # Check if item already in cart
            for item in self.cart:
                if item["name"] == name:
                    item["qty"] += 1
                    self.update_cart_ui()
                    return
            # New item
            self.cart.append({"name": name, "price": price, "qty": 1})
            self.update_cart_ui()
            QMessageBox.information(self, "Added", f"✓ {name} added to bill!")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid price format!")

    def update_cart_ui(self):
        self.cart_table.setRowCount(0)
        self.cart_table.verticalHeader().setDefaultSectionSize(50)  # Increase row height
        total = 0
        for idx, item in enumerate(self.cart):
            pos = self.cart_table.rowCount()
            self.cart_table.insertRow(pos)
            
            # Item name (read-only)
            name_item = QTableWidgetItem(item['name'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            name_item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            self.cart_table.setItem(pos, 0, name_item)
            
            # Quantity (editable) with +/- buttons - LARGER SIZE
            qty_widget = QWidget()
            qty_layout = QHBoxLayout(qty_widget)
            qty_layout.setContentsMargins(2, 5, 2, 5)
            qty_layout.setSpacing(8)
            
            minus_btn = QPushButton("-")
            minus_btn.setMinimumSize(45, 40)
            minus_btn.setMaximumSize(45, 40)
            minus_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            minus_btn.setStyleSheet("background: #e74c3c; color: white; font-weight: bold; border-radius: 5px; border: none;")
            minus_btn.clicked.connect(lambda checked, i=idx: self.decrease_qty(i))
            
            qty_input = QLineEdit(str(item['qty']))
            qty_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qty_input.setMinimumSize(60, 40)
            qty_input.setMaximumSize(60, 40)
            qty_input.setFont(QFont("Arial", 13, QFont.Weight.Bold))
            qty_input.setStyleSheet("border: 2px solid #3498db; border-radius: 5px; padding: 5px;")
            qty_input.editingFinished.connect(lambda i=idx, w=qty_input: self.update_qty(i, w))
            
            plus_btn = QPushButton("+")
            plus_btn.setMinimumSize(45, 40)
            plus_btn.setMaximumSize(45, 40)
            plus_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            plus_btn.setStyleSheet("background: #27ae60; color: white; font-weight: bold; border-radius: 5px; border: none;")
            plus_btn.clicked.connect(lambda checked, i=idx: self.increase_qty(i))
            
            qty_layout.addWidget(minus_btn)
            qty_layout.addWidget(qty_input)
            qty_layout.addWidget(plus_btn)
            qty_layout.addStretch()
            self.cart_table.setCellWidget(pos, 1, qty_widget)
            
            # Subtotal (read-only)
            subtotal = item['price'] * item['qty']
            total += subtotal
            subtotal_item = QTableWidgetItem(f"Rs.{subtotal:.2f}")
            subtotal_item.setFlags(subtotal_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            subtotal_item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            subtotal_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            subtotal_item.setBackground(QColor("#e8f8f5"))
            self.cart_table.setItem(pos, 2, subtotal_item)
        
        self.total_lbl.setText(f"Total: Rs.{total:.2f}")
    
    def increase_qty(self, idx):
        if idx < len(self.cart):
            self.cart[idx]['qty'] += 1
            self.update_cart_ui()
    
    def decrease_qty(self, idx):
        if idx < len(self.cart):
            if self.cart[idx]['qty'] > 1:
                self.cart[idx]['qty'] -= 1
            else:
                self.cart.pop(idx)
            self.update_cart_ui()
    
    def update_qty(self, idx, widget):
        try:
            new_qty = int(widget.text())
            if new_qty > 0:
                if idx < len(self.cart):
                    self.cart[idx]['qty'] = new_qty
                    self.update_cart_ui()
            else:
                widget.setText(str(self.cart[idx]['qty']))
        except ValueError:
            if idx < len(self.cart):
                widget.setText(str(self.cart[idx]['qty']))

    def print_bill(self, receipt_text):
        """Print the receipt with logo using QPrinter"""
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setPageSize(QPrinter.PageSize.A4)
            
            # Create HTML document with logo and receipt
            html_content = """
            <html>
            <head>
                <style>
                    body { font-family: Courier, monospace; text-align: center; margin: 20px; }
                    .logo { text-align: center; margin-bottom: 10px; }
                    .logo img { max-width: 150px; height: auto; }
                    .header { font-weight: bold; font-size: 14px; margin-bottom: 10px; }
                    .receipt { white-space: pre-wrap; font-family: Courier; font-size: 10px; text-align: left; margin: 20px; }
                    .divider { border-top: 2px solid #000; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="logo">
                    <img src="logo.jpg" alt="Logo">
                </div>
                <div class="header">
                    FATIMA TU ZAHRA MEDICAL CENTRE<br>
                    PHARMACY RECEIPT
                </div>
                <div class="divider"></div>
                <div class="receipt">
            """ + receipt_text.replace("<", "&lt;").replace(">", "&gt;") + """
                </div>
                <div class="divider"></div>
                <p style="font-size: 9px; margin-top: 20px;">
                    Thank you for your purchase!<br>
                    This receipt is generated by FATIMA TU ZAHRA MEDICAL CENTRE
                </p>
            </body>
            </html>
            """
            
            # Create text document for printing
            doc = QTextDocument()
            doc.setHtml(html_content)
            
            # Show print dialog
            print_dialog = QPrintDialog(printer, self)
            if print_dialog.exec() == print_dialog.DialogCode.Accepted:
                doc.print(printer)
        except Exception as e:
            QMessageBox.warning(self, "Print Error", f"⚠️ Could not print receipt: {str(e)}")

    def finalize_sale(self):
        if not self.cart:
            QMessageBox.warning(self, "Empty Cart", "❌ Please add items to cart first!")
            return
        
        total = sum(i['price'] * i['qty'] for i in self.cart)
        items_str = ", ".join([f"{i['name']} x{i['qty']} (Rs.{i['price'] * i['qty']:.2f})" for i in self.cart])
        
        # Confirmation dialog
        reply = QMessageBox.question(
            self, "Confirm Sale",
            f"Sale Summary:\n\n{items_str}\n\n📊 Total: Rs.{total:.2f}\n\nComplete this sale?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Save to bills history
        self.db.cursor.execute(
            "INSERT INTO bills (date, items, total) VALUES (?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), items_str, total)
        )
        self.db.conn.commit()
        
        # Success message with receipt
        receipt = f"""
ITEMS SOLD:
{'-' * 40}
"""
        for item in self.cart:
            subtotal = item['price'] * item['qty']
            receipt += f"{item['name']} (x{item['qty']}) .... Rs.{subtotal:.2f}\n"
        
        receipt += f"""
{'-' * 40}
TOTAL AMOUNT: Rs.{total:.2f}
Date & Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'-' * 40}
"""
        
        QMessageBox.information(self, "✓ Sale Complete", receipt)
        
        # Print bill
        self.print_bill(receipt)
        
        # Clear cart
        self.cart = []
        self.update_cart_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernPharmacyPOS()
    window.show()
    sys.exit(app.exec())
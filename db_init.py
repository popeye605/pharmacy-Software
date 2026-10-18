"""
Database Initialization Script for Pharmacy POS System
Fatima Tu Zahra Medical Centre
"""

import sqlite3
from datetime import datetime

def initialize_database():
    """Initialize SQLite database with all required tables and default data"""
    
    conn = sqlite3.connect("pharmacy_pos.db")
    cursor = conn.cursor()
    
    # Drop existing tables to start fresh (optional - comment out for production)
    # cursor.execute("DROP TABLE IF EXISTS users")
    # cursor.execute("DROP TABLE IF EXISTS products")
    # cursor.execute("DROP TABLE IF EXISTS categories")
    # cursor.execute("DROP TABLE IF EXISTS vendors")
    # cursor.execute("DROP TABLE IF EXISTS customers")
    # cursor.execute("DROP TABLE IF EXISTS bills")
    # cursor.execute("DROP TABLE IF EXISTS bill_items")
    # cursor.execute("DROP TABLE IF EXISTS activity_logs")
    # cursor.execute("DROP TABLE IF EXISTS held_bills")
    # cursor.execute("DROP TABLE IF EXISTS held_bill_items")
    
    # 1. Users Table (Role-Based Access Control)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            role TEXT DEFAULT 'staff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    """)
    
    # 2. Categories Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 3. Vendors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 4. Customers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            balance REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 5. Products Table (Medicine/Inventory)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category_id INTEGER,
            vendor_id INTEGER,
            purchase_price REAL NOT NULL,
            sale_price REAL NOT NULL,
            quantity_stock INTEGER DEFAULT 0,
            minimum_stock INTEGER DEFAULT 10,
            expiry_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (vendor_id) REFERENCES vendors(id)
        )
    """)
    
    # Create index on serial_no for fast searches
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_serial_no ON products(serial_no)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_name ON products(name)")
    
    # 6. Bills Table (Transaction Header)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id TEXT UNIQUE NOT NULL,
            bill_number INTEGER UNIQUE NOT NULL,
            user_id INTEGER,
            customer_id INTEGER,
            bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL,
            discount_percent REAL DEFAULT 0,
            discount_amount REAL DEFAULT 0,
            payable_amount REAL,
            received_amount REAL,
            balance_amount REAL,
            payment_method TEXT,
            notes TEXT,
            is_voided INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    
    # Create index on bill_id for fast searches
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_bill_id ON bills(bill_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_bill_number ON bills(bill_number)")
    
    # 7. Bill Items Table (Transaction Details)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity REAL,
            unit_price REAL,
            discount_percent REAL DEFAULT 0,
            discount_amount REAL DEFAULT 0,
            line_total REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bill_id) REFERENCES bills(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # 8. Held Bills Table (For Hold/Resume Functionality)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS held_bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bill_data TEXT,
            held_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # 8b. Demand Notes Table (For Low Stock Management)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS demand_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            required_quantity INTEGER,
            notes TEXT,
            created_by INTEGER,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """)
    
    # Create index on demand notes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_demand_product ON demand_notes(product_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_demand_status ON demand_notes(status)")
    
    # 9. Activity Logs Table (Security & Accountability)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            action TEXT NOT NULL,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Create index on timestamp for efficient log searches
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activity_timestamp ON activity_logs(timestamp)")
    
    # 10. Income/Expense Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            category TEXT,
            amount REAL,
            description TEXT,
            user_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # 11. Stock Demand Book (For Out of Stock Items)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_demand (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_name TEXT,
            quantity_requested INTEGER,
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fulfilled_at TIMESTAMP,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # ===== DEFAULT DATA =====
    
    # Insert default categories
    default_categories = [
        ("Antibiotics", "Antibiotic medicines"),
        ("Pain Relief", "Painkillers and analgesics"),
        ("Vitamins", "Vitamin supplements"),
        ("Cold & Flu", "Cold and flu medications"),
        ("Digestive", "Digestive system medicines"),
        ("Skincare", "Topical applications"),
    ]
    
    for cat_name, cat_desc in default_categories:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
            (cat_name, cat_desc)
        )
    
    # Insert default vendors
    default_vendors = [
        ("Abbott", "John Smith", "0321-1234567", "abbott@pharma.com", "123 Pharma Street"),
        ("Novartis", "Ahmed Khan", "0321-2345678", "novartis@pharma.com", "456 Medical Avenue"),
        ("Glaxo", "Sarah Ahmed", "0321-3456789", "glaxo@pharma.com", "789 Health Road"),
    ]
    
    for vendor_name, contact, phone, email, address in default_vendors:
        cursor.execute(
            """INSERT OR IGNORE INTO vendors (name, contact_person, phone, email, address) 
               VALUES (?, ?, ?, ?, ?)""",
            (vendor_name, contact, phone, email, address)
        )
    
    # Insert default users (Admin and Staff)
    default_users = [
        ("admin", "admin@123", "Administrator", "admin@pharmacy.com", "admin"),
        ("pharmacist1", "pass123", "Ali Ahmed", "ali@pharmacy.com", "staff"),
        ("staff2", "pass123", "Fatima Khan", "fatima@pharmacy.com", "staff"),
    ]
    
    for username, password, full_name, email, role in default_users:
        cursor.execute(
            """INSERT OR IGNORE INTO users (username, password, full_name, email, role) 
               VALUES (?, ?, ?, ?, ?)""",
            (username, password, full_name, email, role)
        )
    
    # Insert sample products
    sample_products = [
        ("SN001", "Paracetamol 500mg", 1, 1, 5.00, 10.00, 50, 10, "2026-12-31"),
        ("SN002", "Amoxicillin 250mg", 1, 2, 8.00, 15.00, 35, 10, "2026-11-30"),
        ("SN003", "Ibuprofen 200mg", 2, 1, 6.00, 12.00, 40, 10, "2026-10-31"),
        ("SN004", "Vitamin C 1000mg", 3, 3, 4.00, 8.00, 100, 20, "2027-06-30"),
        ("SN005", "Cetirizine 10mg", 4, 2, 3.50, 7.00, 60, 15, "2026-09-30"),
        ("SN006", "Metformin 500mg", 5, 1, 2.50, 5.50, 80, 20, "2026-08-31"),
        ("SN007", "Omeprazole 20mg", 5, 3, 4.00, 8.50, 45, 10, "2026-07-31"),
        ("SN008", "Salicylic Acid Cream", 6, 2, 3.00, 6.50, 30, 10, "2026-05-31"),
    ]
    
    for serial_no, name, cat_id, vendor_id, purchase_price, sale_price, stock, min_stock, expiry in sample_products:
        cursor.execute(
            """INSERT OR IGNORE INTO products 
               (serial_no, name, category_id, vendor_id, purchase_price, sale_price, quantity_stock, minimum_stock, expiry_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (serial_no, name, cat_id, vendor_id, purchase_price, sale_price, stock, min_stock, expiry)
        )
    
    conn.commit()
    conn.close()
    
    print("✓ Database initialized successfully: pharmacy_pos.db")
    print("✓ Default users created (admin/admin@123, pharmacist1/pass123)")
    print("✓ Sample products, categories, and vendors loaded")

if __name__ == "__main__":
    initialize_database()

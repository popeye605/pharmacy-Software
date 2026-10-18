#!/usr/bin/env python3
"""Quick Start Guide for Pharmacy POS System"""

print("""
╔════════════════════════════════════════════════════════════════════════╗
║                  PHARMACY POS SYSTEM - QUICK START                     ║
║           Fatima Tu Zahra Medical Centre - Complete Package            ║
╚════════════════════════════════════════════════════════════════════════╝

SETUP COMPLETE ✓
═══════════════════════════════════════════════════════════════════════

✓ Database: pharmacy_pos.db (initialized with 12 tables)
✓ Sample Data: 3 users, 6 categories, 3 vendors, 8 medicines
✓ Application: pharmacy_app.py (complete PyQt6 implementation)
✓ Theme: Professional blue/grey color palette with hospital branding

DEFAULT CREDENTIALS
═══════════════════════════════════════════════════════════════════════

1. ADMIN ACCOUNT
   Username: admin
   Password: admin@123
   Access: Dashboard, Sales, Inventory, Bill History, Logs, Users

2. STAFF ACCOUNT
   Username: pharmacist1
   Password: pass123
   Access: Sales (POS) screen only

3. STAFF ACCOUNT 2
   Username: staff2
   Password: pass123
   Access: Sales (POS) screen only

TO RUN THE APPLICATION
═══════════════════════════════════════════════════════════════════════

   python pharmacy_app.py

The application will start with a login screen. Use any of the above
credentials to log in.

KEY FEATURES
═══════════════════════════════════════════════════════════════════════

📊 DASHBOARD
   • 8 KPI cards showing key metrics
   • Recent transactions overview
   • Real-time data updates
   • Welcome message with role identification

🛒 POINT OF SALE (POS)
   • Product search by name or serial number
   • Shopping cart with dynamic quantity adjustment
   • Live price editing per line item
   • Percentage-based bill discount
   • Automatic balance/change calculation
   • Hold & Resume bill functionality
   • Receipt printing to thermal printer
   • Stock validation with color coding
   • Unique Bill ID generation (BILL-YYYYMMDD-XXXX)

📦 INVENTORY MANAGEMENT (Admin Only)
   • Add new products with serial numbers
   • Edit product details and pricing
   • Delete/deactivate products
   • Color-coded stock status:
     - Red: Low stock (≤ minimum)
     - Yellow: Warning level (< 20 units)
     - Green: Good stock level
   • Search by product name or serial number
   • Quick access to cost vs selling price

📋 BILL HISTORY
   • Search bills by Bill ID
   • Date range filtering (default: last 30 days)
   • View complete bill details with line items
   • Reprint receipts to thermal printer
   • Searchable transaction history

📝 ACTIVITY LOGS (Admin Only)
   • Complete audit trail of all operations
   • Filter by user and action type
   • Export to CSV for reporting
   • Track LOGIN, LOGOUT, SALE, DELETE_PRODUCT, HOLD_BILL events
   • Timestamp tracking for all activities

👥 USER MANAGEMENT (Admin Only)
   • Add new users with roles (admin/staff)
   • Edit user details
   • Enable/disable user accounts
   • View user login history
   • Manage staff permissions

👤 PROFILE
   • View and update personal information
   • Change password with current password verification
   • Email management
   • Display current role and access level

SYSTEM CAPABILITIES
═══════════════════════════════════════════════════════════════════════

✓ Role-Based Access Control (RBAC)
  - Admin: Full system access
  - Staff: Sales screen only, cannot access inventory or logs

✓ Offline Functionality
  - 100% offline operation
  - SQLite local database
  - No internet required

✓ Receipt Printing
  - Thermal printer support
  - Professional formatting
  - Hospital branding integration
  - Unique Bill IDs on receipts

✓ Advanced Billing
  - Percentage-based discounts
  - Hold/Resume functionality
  - Live price and discount editing
  - Automatic balance calculation

✓ Security
  - User authentication
  - Password management
  - Activity logging
  - User role restrictions

✓ Inventory Intelligence
  - Stock level tracking
  - Minimum stock alerts
  - Color-coded stock status
  - Purchase price (admin only)
  - Serial number indexing for fast searches

DATABASE SCHEMA
═══════════════════════════════════════════════════════════════════════

Tables Created:
1. users - User accounts with roles
2. products - Medicines/pharmaceuticals with pricing
3. categories - Product categories
4. vendors - Supplier information
5. customers - Customer records
6. bills - Sales transaction headers
7. bill_items - Line items per transaction
8. held_bills - Bills on hold for later completion
9. activity_logs - Audit trail of all operations
10. transactions - Income/expense tracking
11. stock_demand - Customer demand tracking
12. sqlite_sequence - Auto-increment sequences

KEYBOARD SHORTCUTS
═══════════════════════════════════════════════════════════════════════

F1  - Open POS Screen (Sales)
F2  - Hold Current Bill
F3  - Resume Held Bill (from bill list)
Esc - Logout

FILE STRUCTURE
═══════════════════════════════════════════════════════════════════════

d:\\pharmacy Software\\
├── pharmacy_app.py          (Main application - ~3000 lines)
├── pharmacy_pos.db          (SQLite database)
├── db_init.py               (Database initialization script)
├── verify_db.py             (Database verification utility)
├── README.md                (Full documentation)
└── activity_logs_*.csv      (Exported activity logs)

TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════

Issue: "Database locked" error
  → Close other instances of the application

Issue: "No module named 'PyQt6'"
  → Install: pip install PyQt6

Issue: "Cannot print receipts"
  → Ensure a printer is installed on Windows
  → Test Windows Print Dialog functionality

Issue: "Forgot admin password"
  → Run: python db_init.py (reinitialize database with defaults)

ADVANCED FEATURES
═══════════════════════════════════════════════════════════════════════

Hold & Resume Bills:
  1. Add items to cart
  2. Click "Hold Bill" button
  3. Cart clears, bill is saved
  4. Later, access "Sale" screen
  5. Can resume from held bills (future enhancement)

Discount Types:
  • Item-level discount: Adjust per line in cart
  • Bill-level discount: Set percentage on entire transaction
  • Automatic calculation: Payable amount updates automatically

Stock Validation:
  • Red highlighting: Quantity exceeds available stock
  • Yellow highlighting: Low stock warning
  • Green highlighting: Adequate stock level
  • Prevents overselling

Activity Logging:
  • All user actions tracked with timestamp
  • Username recorded for accountability
  • Supports CSV export for reports
  • Helps audit trail and compliance

NEXT STEPS
═══════════════════════════════════════════════════════════════════════

1. Run the application: python pharmacy_app.py
2. Login with admin/admin@123
3. Explore the Dashboard to see KPI cards
4. Click "Sale" to access the POS screen
5. Add some products and create a test bill
6. Check "Bill History" to see saved transactions
7. View "Activity Logs" to see audit trail
8. Try adding a new staff user in "Users"
9. Logout and login with staff account to see restricted view

SUPPORT & CUSTOMIZATION
═══════════════════════════════════════════════════════════════════════

The system is designed for:
✓ Offline operation
✓ Small to medium pharmacies
✓ Quick learning curve
✓ Easy data backup (copy pharmacy_pos.db)
✓ SQLite database portability

For customizations:
• Modify THEME_STYLESHEET in pharmacy_app.py for colors
• Adjust KPI calculations in DashboardWidget.load_data()
• Add new product fields in ProductDialog
• Extend user roles by modifying role checks

═══════════════════════════════════════════════════════════════════════

System Ready for Deployment! 🎉

Questions? Check the detailed README.md file for complete documentation.

═══════════════════════════════════════════════════════════════════════
""")

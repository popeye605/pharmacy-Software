# Pharmacy POS System - Fatima Tu Zahra Medical Centre

Complete professional pharmacy management and point-of-sale (POS) system with role-based access control, advanced billing, inventory management, and comprehensive activity logging.

## Features

### 1. **Authentication & Security**
- Login system with role-based access control (RBAC)
- User roles: `admin` (full access) and `staff` (restricted to POS only)
- Activity logging for all user actions
- Secure password management with update capability
- User management interface for admins

### 2. **Dashboard**
- 8 KPI cards showing key metrics:
  - Visited Customers
  - Purchase volumes
  - Sales figures
  - Sale returns
  - Customer balance tracking
  - Low stock items alert
  - Total products count
  - Revenue tracking (Today)
- Recent transactions overview
- Real-time data updates

### 3. **Advanced POS System (F1 - Sale)**
- **Product Search & Selection**
  - Search by product name or serial number
  - Real-time product catalog
  - Stock availability display
  - Purchase price visibility (Admin only)
  
- **Shopping Cart**
  - Add/remove products
  - Quantity management (+/- buttons)
  - Unit price editing
  - Line item discount per product
  - Live calculation of subtotals
  
- **Billing & Payment**
  - Total amount calculation
  - Percentage-based discount (on entire bill)
  - Automatic discount amount calculation
  - Payable amount
  - Received amount tracking
  - Change/Balance calculation
  - Hold & Resume functionality for bills in progress
  
- **Receipt Printing**
  - Professional thermal printer support
  - Hospital branding (FATIMA TU ZAHRA MEDICAL CENTRE)
  - Unique Bill ID generation
  - Item details, amounts, discounts
  - Change amount display

### 4. **Inventory Management (Admin Only)**
- **Product Management**
  - Add new products with:
    - Unique Serial Number
    - Product name
    - Category selection
    - Vendor assignment
    - Purchase price (for margin calculation)
    - Sale price (for billing)
    - Stock quantity
    - Minimum stock threshold
    - Expiry date tracking
  
- **Inventory Controls**
  - Edit product details
  - Delete/deactivate products
  - Color-coded stock status:
    - Red: Low stock (≤ minimum)
    - Yellow: Warning level
    - Green: Good stock
  
- **Search & Filtering**
  - Search by product name or serial number
  - Indexed search for fast retrieval
  - Real-time filter updates

### 5. **Bill History & Archival**
- **Search & Retrieval**
  - Search by Bill ID
  - Search by date range
  - View complete bill details
  - List all transactions
  
- **Bill Management**
  - Detailed bill information view
  - Individual line item display
  - Re-print functionality for thermal printers
  - Date-range filtering (default: last 30 days)
  - Export capability

### 6. **Activity Logs (Admin Only)**
- **Comprehensive Logging**
  - Records all user actions:
    - LOGIN/LOGOUT
    - SALE transactions
    - PRODUCT deletions
    - BILL holds
  - Includes username, action type, details, and timestamp
  
- **Log Management**
  - Filter by user
  - Filter by action type
  - Export to CSV
  - Clear old logs
  - Search functionality

### 7. **User Management (Admin Only)**
- **User CRUD Operations**
  - Add new users (staff or admin)
  - Edit existing users
  - Disable/enable user accounts
  - View user login history
  - Role assignment
  
- **User Profile**
  - Full name
  - Email address
  - Role designation
  - Last login tracking
  - Status (Active/Inactive)

### 8. **Personal Profile & Settings**
- **Profile Management**
  - View and update personal information
  - Change password with current password verification
  - Email updates
  - Display current role
  
- **Security**
  - Password confirmation
  - Minimum password length requirement (6 characters)
  - Current password validation

## Database Schema

### Tables

1. **users** - User accounts and authentication
   - id, username, password, full_name, email, role, created_at, last_login, is_active

2. **products** - Medicine/pharmaceutical inventory
   - id, serial_no, name, category_id, vendor_id, purchase_price, sale_price, quantity_stock, minimum_stock, expiry_date, created_at, updated_at, is_active

3. **categories** - Product categories
   - id, name, description, created_at

4. **vendors** - Supplier information
   - id, name, contact_person, phone, email, address, created_at

5. **customers** - Customer records
   - id, name, phone, email, address, balance, created_at

6. **bills** - Transaction headers
   - id, bill_id, bill_number, user_id, customer_id, bill_date, total_amount, discount_percent, discount_amount, payable_amount, received_amount, balance_amount, payment_method, notes, is_voided, created_at, updated_at

7. **bill_items** - Transaction line items
   - id, bill_id, product_id, quantity, unit_price, discount_percent, discount_amount, line_total, created_at

8. **held_bills** - Bills on hold for later retrieval
   - id, user_id, bill_data (JSON), held_at

9. **activity_logs** - User action audit trail
   - id, user_id, username, action, details, timestamp, ip_address

10. **transactions** - Income/Expense tracking
    - id, type, category, amount, description, user_id, timestamp

11. **stock_demand** - Customer demand for out-of-stock items
    - id, product_id, customer_name, quantity_requested, requested_at, fulfilled_at, status

## Default Users

| Username      | Password    | Role   | Full Name        |
|---------------|-------------|--------|------------------|
| admin         | admin@123   | admin  | Administrator    |
| pharmacist1   | pass123     | staff  | Ali Ahmed        |
| staff2        | pass123     | staff  | Fatima Khan      |

## Installation & Setup

### Prerequisites
- Python 3.8+
- PyQt6
- SQLite3 (included with Python)

### Steps

1. **Install Dependencies**
   ```bash
   pip install PyQt6
   ```

2. **Initialize Database**
   ```bash
   python db_init.py
   ```
   This creates `pharmacy_pos.db` with:
   - All required tables
   - Default users (admin, pharmacist1, staff2)
   - Sample products (8 medicines)
   - Sample categories and vendors

3. **Run Application**
   ```bash
   python pharmacy_app.py
   ```

## Usage

### Admin Workflow
1. Login with admin credentials
2. Dashboard shows overview of all operations
3. Manage inventory (add/edit/delete products)
4. View activity logs
5. Manage system users
6. Monitor sales and transactions

### Staff/Pharmacist Workflow
1. Login with staff credentials
2. Access POS screen (Sale F1) immediately
3. Search and add products to cart
4. Apply discounts
5. Hold bill if needed, resume later
6. Complete sale with payment
7. Print receipt

### Admin - Inventory Management
```
Click "Inventory" → Search products → Add/Edit/Delete
- Serial Number (auto-indexed for fast search)
- Name, Category, Vendor
- Purchase Price (for margin calculation)
- Sale Price (for billing)
- Stock Quantity with minimum threshold
- Expiry date tracking
- Color-coded stock status
```

### Admin - Activity Audit
```
Click "Activity Logs" → Filter by User/Action → Export CSV
- Complete audit trail of all operations
- User identification
- Action details
- Timestamps
- CSV export capability
```

### Billing & Receipt
```
POS Screen → Add Products → Set Discount % → Enter Received Amount → Pay & Save
- Automatic receipt printing to default printer
- Professional format with hospital branding
- Unique Bill ID
- Thermal printer compatible
- Change amount display
```

## Professional Features

### Theme & Branding
- Professional blue/grey color palette
- Hospital name "FATIMA TU ZAHRA MEDICAL CENTRE" throughout
- Consistent UI design with PyQt6
- Responsive layout
- Accessibility-friendly fonts

### Security
- Role-based access control (RBAC)
- Admin-only features hidden from staff
- Purchase price visibility restricted (admin only)
- Audit trail of all actions
- Password security with confirmation

### Offline Functionality
- 100% offline operation
- SQLite local database
- No internet required
- All features available without connectivity

### Offline Printing
- Thermal printer support via Windows print dialog
- Professional receipt formatting
- Hospital branding on receipts
- Unique Bill ID and timestamps

## File Structure

```
pharmacy Software/
├── pharmacy_app.py          # Main application entry point
├── db_init.py              # Database initialization script
├── pharmacy_pos.db         # SQLite database (auto-created)
└── README.md              # This file
```

## Keyboard Shortcuts

| Shortcut | Action        |
|----------|---------------|
| F1       | Open POS      |
| F2       | Hold Bill     |
| F3       | Resume Bill   |
| F4       | Pay & Save    |
| Enter    | Login / Confirm|

## Database Indexing

For fast searches with large catalogs:
- `idx_serial_no` on products.serial_no
- `idx_product_name` on products.name
- `idx_bill_id` on bills.bill_id
- `idx_bill_number` on bills.bill_number
- `idx_activity_timestamp` on activity_logs.timestamp

## Troubleshooting

### Database Issues
- **"Database locked"**: Close other instances of the application
- **"No table"**: Run `python db_init.py` to initialize

### UI Issues
- **Display too small**: Adjust Windows DPI settings
- **Printing not working**: Ensure printer is installed in Windows

### Login Issues
- **Forgot password**: Reset via admin panel or database query

## Future Enhancements

- [ ] Multi-location support
- [ ] Email receipt delivery
- [ ] SMS notifications
- [ ] Customer loyalty program
- [ ] Advanced reports & analytics
- [ ] Barcode scanning
- [ ] Cloud backup
- [ ] Mobile app companion

## Support

For issues or feature requests, ensure:
1. Database is properly initialized
2. All dependencies are installed
3. You're using Python 3.8+
4. PyQt6 is correctly installed

## License

This system is proprietary software for Fatima Tu Zahra Medical Centre.

# Troubleshooting & Usage Guide

## Bill Saving Issues

### If bill still shows error when saving:

1. **Check error message** - It will now show the exact problem
2. **Common issues:**
   - Empty cart - Add items before saving
   - Database locked - Close other instances of the app
   - Payment method missing - Now defaults to 'CASH'

3. **Solution steps:**
   - Make sure at least one item is in cart
   - Check all prices are valid numbers
   - Try again after closing and reopening app

---

## Vendor Management

### To Add a Vendor:
1. Click "🏢 Vendors" in sidebar
2. Click "➕ Add Vendor" button
3. Enter:
   - **Vendor Name** (required)
   - **Phone** (optional)
   - **Email** (optional)
4. Click "Save"

### To Edit a Vendor:
1. Click "🏢 Vendors"
2. Click "Edit" button next to vendor
3. Update information
4. Click "Save"

### To Delete a Vendor:
1. Click "🏢 Vendors"
2. Click "Delete" button
3. Confirm deletion

---

## Category Management

### To Add a Category:
1. Click "📂 Categories" in sidebar
2. Click "➕ Add Category" button
3. Enter:
   - **Category Name** (required)
   - **Description** (optional)
4. Click "Save"

### To Edit a Category:
1. Click "📂 Categories"
2. Click "Edit" button
3. Update name/description
4. Click "Save"

### To Delete a Category:
1. Click "📂 Categories"
2. Click "Delete" button
3. Confirm deletion

**Note:** Only admin users can manage categories and vendors

---

## Low Stock Management

### Automatic Alert System:
- Medicines automatically show in "⚠️ Low Stock" tab when:
  - Current stock ≤ Minimum stock level
- Color coding:
  - **CRITICAL** (Red) = Stock is 0
  - **LOW** (Orange) = Stock below minimum

### To Create a Demand Note:
1. Click "⚠️ Low Stock" in sidebar
2. See all low stock medicines
3. Click "➕ Create Demand" for a medicine
4. Enter:
   - **Required Quantity** (default = 2x minimum stock)
   - **Notes** (optional - e.g., "Urgent needed for ward A")
5. Click "Create Demand"
6. System logs this action

### To View Demand Notes:
1. Click "⚠️ Low Stock"
2. Click "📝 Notes" for any medicine
3. View all demands for that medicine:
   - Date created
   - Required quantity
   - Current status (PENDING/FULFILLED)
   - Notes entered

### To Mark Demand as Fulfilled:
1. After stock is replenished
2. Click "📝 Notes" on that medicine
3. Click "✓ Fulfill" button
4. Status changes to FULFILLED
5. Closes the demand request

---

## Activity Tracking

All actions are automatically logged:
- **Bill Sales** - Amount and bill ID
- **Adding Vendors** - Vendor name
- **Editing Vendors** - What was updated
- **Deleting Vendors** - Vendor name
- **Adding Categories** - Category name
- **Creating Demands** - Product and quantity
- **Fulfilling Demands** - Which demand was fulfilled

View logs in "📝 Activity Logs" section (Admin only)

---

## Common Issues & Solutions

### Issue: "Failed to save bill"
**Solution:** Check error message in dialog
- Ensure all items have valid prices
- Ensure quantity is a valid number
- Make sure cart is not empty

### Issue: Cannot see Low Stock tab
**Solution:** 
- Log in as admin user
- Low Stock tab only appears for admin accounts

### Issue: Vendor/Category not appearing
**Solution:**
- Refresh the page
- Click "🔄 Refresh" button
- Check if it was actually created (check error message)

### Issue: Demand note not saving
**Solution:**
- Check that quantity is a valid number
- Ensure you selected a valid product
- Check database connection

---

## Quick Reference

| Feature | Access | Who Can Use | Keyboard |
|---------|--------|-------------|----------|
| Sale/POS | 🛒 Sale | Everyone | F1 |
| Inventory | 📦 Inventory | Admin only | - |
| Low Stock | ⚠️ Low Stock | Admin only | - |
| Categories | 📂 Categories | Admin only | - |
| Vendors | 🏢 Vendors | Admin only | - |
| Bill History | 📋 Bill History | Admin only | - |
| Activity Logs | 📝 Activity Logs | Admin only | - |
| Users | 👥 Users | Admin only | - |
| Profile | 👤 Profile | Everyone | - |

---

## Important Notes

⚠️ **Only Admin users can:**
- Manage vendors
- Manage categories
- View low stock
- Create demand notes
- View bill history
- View activity logs
- Manage users

✅ **All users can:**
- Make sales (POS)
- View their profile
- View dashboard

---

## Getting Help

If you encounter issues:

1. **Check the error message** - It now shows exact details
2. **Check Activity Logs** - See what was logged
3. **Close and reopen** - Fixes most connection issues
4. **Restart the app** - For database lock issues


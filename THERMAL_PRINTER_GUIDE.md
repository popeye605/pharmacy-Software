# Pharmacy POS - Thermal Printer Setup & Usage Guide

## Overview
The updated Pharmacy POS system now has full support for thermal printer receipt printing. When you complete a sale, a print dialog appears automatically allowing you to select your thermal printer.

---

## 1. Thermal Printer Setup

### Installing Thermal Printer Driver:
1. **Windows**:
   - Download driver from printer manufacturer
   - Install driver software
   - Connect printer via USB or Network
   - Test print from Windows Settings > Devices > Printers

2. **Common Thermal Printers**:
   - Zebra printers
   - Star Micronics
   - Epson TM series
   - Brother TD series
   - Citizen printers

### Configuring in Windows:
1. Go to Settings > Devices > Printers
2. Click "Add a printer"
3. Select your thermal printer
4. Click "Set as default" (optional)

---

## 2. Making a Sale with Thermal Printing

### Step-by-Step Workflow:

```
1. OPEN APPLICATION
   └─ python pharmacy_app.py
   └─ Login with credentials

2. SELECT SALE SCREEN
   └─ Click "Sale" button in sidebar
   └─ Product list displays on left

3. ADD PRODUCTS TO CART
   └─ Search for product: "Paracetamol"
   └─ Click "Add" button
   └─ Product added to shopping cart (right side)
   └─ Cart shows: Serial #, Name, Qty, Unit Price, Discount %, Subtotal

4. ADJUST QUANTITIES & PRICES
   └─ Double-click Qty column to change quantity
   └─ Double-click Unit Price to adjust price
   └─ Double-click Discount % to apply percentage discount
   └─ Subtotal auto-calculates: Qty × Price × (1 - Discount%)

5. APPLY OVERALL DISCOUNT (Optional)
   └─ Enter value in "Discount %:" field (e.g., 5)
   └─ Discount Amount auto-calculates
   └─ Payable Amount updated automatically

6. ENTER RECEIVED AMOUNT
   └─ Enter cash received in "Received Amount:" field
   └─ Balance/Change calculates automatically

7. SAVE BILL & PRINT
   └─ Click "Pay & Save" button
   └─ Print Dialog appears with:
      ├─ Printer selection dropdown
      ├─ Properties button (if needed)
      └─ Print / Cancel buttons

8. SELECT THERMAL PRINTER
   └─ Click dropdown list
   └─ Select your thermal printer (e.g., "Zebra ZD410")
   └─ Adjust print settings if needed (Properties)

9. PRINT RECEIPT
   └─ Click "Print" button
   └─ Receipt prints on thermal printer
   └─ Bill saves to database
   └─ Activity log created
   └─ Cart clears automatically

10. SUCCESS MESSAGE
    └─ "Bill saved successfully!"
    └─ Bill ID displayed (e.g., "BILL-20240123-0001")
```

---

## 3. Receipt Format & Content

### What Prints on Receipt:

```
╔═══════════════════════════════════════╗
║   FATIMA TU ZAHRA MEDICAL CENTRE     ║
║   PHARMACY BILLING RECEIPT             ║
╠═══════════════════════════════════════╣
║ Bill ID: BILL-20240123-0001           ║
║ Date & Time: 2024-01-23 14:35:22     ║
║ Cashier: pharmacist1                   ║
╠═══════════════════════════════════════╣
║ Item              Qty        Price    ║
║ Paracetamol       2        Rs. 100.00 ║
║ Aspirin           1        Rs. 50.00  ║
╠═══════════════════════════════════════╣
║ Subtotal:                  Rs. 250.00 ║
║ Discount (10%):           Rs. 25.00   ║
║                                        ║
║ PAYABLE: Rs. 225.00                   ║
║ Received: Rs. 500.00                   ║
║ CHANGE: Rs. 275.00                    ║
╠═══════════════════════════════════════╣
║       Thank you for Coming!           ║
║  Fatima Tu Zahra Medical Centre       ║
║         Naqvi Enterprises             
╚═══════════════════════════════════════╝
```

---

## 4. Thermal Printer Specifications

### Paper Size:
- **Standard**: 80mm width (thermal roll)
- **Length**: Continuous (auto-adjusts to content)

### Print Quality:
- **Resolution**: 203 DPI (typical thermal)
- **Font**: Arial 14px (professional)
- **Colors**: Black & white (monochrome)

### Recommended Settings:
- **Printer Type**: Thermal Receipt Printer
- **Connection**: USB (recommended) or Network
- **Paper**: 80mm × 40mm thermal roll
- **Default**: Set as default printer for quick access

---

## 5. Troubleshooting Thermal Printer Issues

### Problem: Print Dialog Doesn't Appear
**Solution:**
1. Check if printer is properly installed
2. Go to Settings > Devices > Printers
3. Verify thermal printer is listed
4. Try adding printer again if missing

### Problem: Printer Not in Dropdown List
**Solution:**
1. Open Settings > Devices > Printers & Scanners
2. Click "Add device"
3. Select "Local printer"
4. Choose your thermal printer
5. Complete installation
6. Restart application

### Problem: Receipt Prints with Strange Characters
**Solution:**
1. Check printer driver is latest version
2. Verify UTF-8 encoding in printer settings
3. Try different thermal printer driver
4. Test print from Notepad to verify printer works

### Problem: Receipt Prints but Text is Cut Off
**Solution:**
1. Adjust page size in printer properties:
   - Go to printer properties
   - Set paper size to "Custom 80mm × 40mm"
   - Adjust margins if needed
2. Reduce font size in code (search for "font-size: 14px")
3. Test with shorter product names first

### Problem: Printing Very Slowly
**Solution:**
1. Check USB connection (more reliable than network)
2. Reduce image quality in receipt
3. Use simpler HTML (fewer styles)
4. Verify printer buffer is clear

### Problem: Print Dialog Freezes Application
**Solution:**
1. Click Cancel in print dialog
2. Disconnect printer temporarily
3. Check printer is powered on
4. Verify driver installation
5. Restart application

---

## 6. Print Dialog Options

### When Print Dialog Appears:

```
┌─────────────────────────────────────┐
│ Print                               │
├─────────────────────────────────────┤
│ Name: [Zebra ZD410 v1            ▼] │
│                                     │
│ Status: [Ready                    ] │
│ Type:   [Thermal Printer USB     ] │
│ Where:  [Local Port (USB001)     ] │
│                                     │
│ ☐ Print to file                     │
│                                     │
│ [Properties] [OK] [Cancel]          │
└─────────────────────────────────────┘
```

### Buttons:
- **Properties**: Advanced printer settings
- **OK/Print**: Send receipt to printer
- **Cancel**: Don't print (bill still saves)

---

## 7. Advanced Thermal Printer Configuration

### For 80mm Thermal Printers:

```python
# In print_receipt() method:
printer = QPrinter()
printer.setPageSize(QPageSize(QSizeF(80, 40), QPageSize.Millimeter))
printer.setPageMargins(2, 2, 2, 2, QPrinter.Millimeter)
printer.setOutputFormat(QPrinter.NativeFormat)
printer.setColorMode(QPrinter.GrayScale)  # Thermal = B&W only
```

### Custom Paper Size:
1. Printer Properties > Advanced
2. Select "Custom"
3. Set Width: 80mm, Height: 40mm
4. Click OK

---

## 8. Bill Reprinting

### To Reprint an Old Bill:

```
1. Click "Bill History" in sidebar
2. Search for bill:
   └─ By Bill ID: "BILL-20240123-0001"
   └─ By Date Range: Select from/to dates
3. Select bill from list
4. Click "Reprint" button
5. Print dialog appears (same as before)
6. Select thermal printer
7. Click "Print"
8. Receipt reprints with original data
```

### What's Preserved in Reprints:
- ✓ Original bill ID
- ✓ Original date & time
- ✓ Original cashier name
- ✓ All items and prices
- ✓ Original discount applied
- ✓ Original amounts received & change

---

## 9. Activity Logging & Audit Trail

### Every Sale Creates a Log Entry:

```
User:       pharmacist1
Action:     SALE
Details:    Bill BILL-20240123-0001: Rs. 225.00
Timestamp:  2024-01-23 14:35:22
```

### View Logs:
1. Click "Activity Logs" (Admin only)
2. Filter by user or action
3. All sales listed with:
   - Bill ID
   - Amount
   - Date & Time
   - Cashier name
4. Export to CSV for records

---

## 10. Best Practices for Thermal Printing

### 1. Keep Receipt Rolls Fresh
- ✓ Store in cool, dry place
- ✓ Keep original packaging
- ✓ Use within 1 year of manufacture
- ✗ Avoid sunlight exposure

### 2. Regular Maintenance
- ✓ Clean print head weekly (gentle brush)
- ✓ Check for paper jams daily
- ✓ Update printer driver monthly
- ✓ Test print weekly

### 3. Print Settings
- ✓ Keep darkness/heat settings default
- ✓ Use recommended paper width (80mm)
- ✓ Don't force paper through printer
- ✓ Let printer warm up 30 seconds at startup

### 4. Troubleshooting
- ✓ Always have replacement ink/paper
- ✓ Keep printer driver updated
- ✓ Test with Windows print test page first
- ✓ Check USB cable connection regularly

---

## 11. Common Thermal Printers & Settings

| Model | Width | Connection | Driver Notes |
|-------|-------|-----------|--------------|
| Zebra ZD410 | 80mm | USB | Download from Zebra |
| Star Micronics | 80mm | USB/Net | Plugin available |
| Epson TM-T20 | 80mm | Serial/USB | Included in Windows |
| Brother TD-4550 | 80mm | USB | Download from Brother |
| Citizen CT-S4500 | 80mm | USB | Auto-detected |

---

## 12. Receipt Format Customization

### To Change Receipt Template:

**Location**: `print_receipt()` method in `pharmacy_app.py`

**Example Customizations**:

```python
# Change font size (in receipt HTML)
<body style="font-family: Arial; font-size: 16px;">

# Change header
<h2 style="margin: 5px;">YOUR HOSPITAL NAME</h2>

# Add custom footer
<p>Your custom message here</p>

# Add logo/image
<img src="path/to/logo.jpg" width="80px">
```

---

## 13. Batch Printing & Archiving

### Print Multiple Bills:
1. Go to "Bill History"
2. Select date range
3. For each bill:
   - Click bill
   - Click "Reprint"
   - Send to printer
4. All bills print sequentially

### Archive Receipts:
1. Activity Logs > Export to CSV
2. Save in: `d:\pharmacy Software\logs\`
3. Keep for 1+ years for audit
4. Organize by date

---

## 14. Support & Contact

### For Issues with:
- **Application**: Review console output in terminal
- **Printer Driver**: Contact printer manufacturer
- **Receipt Format**: Edit HTML in `print_receipt()` method
- **Database**: Check `pharmacy_pos.db` integrity

### Common Support Commands:
```bash
# Test database
python verify_db.py

# Check Python version
python --version

# Verify PyQt6
python -c "import PyQt6; print('PyQt6 OK')"

# Reset application
del pharmacy_pos.db
python db_init.py
```

---

## Quick Reference - Sales Process

```
START → Search Product → Add to Cart → Adjust Qty/Price
  ↓
Apply Discount → Enter Received Amount → Click "Pay & Save"
  ↓
Print Dialog Appears → Select Thermal Printer → Click Print
  ↓
Receipt Prints → Bill Saved → Log Created → Cart Cleared
  ↓
SUCCESS - Bill ID: BILL-YYYYMMDD-XXXX
```

---

**✅ Your thermal printer setup is complete!**

For detailed troubleshooting, consult the printer manufacturer's documentation or contact technical support.

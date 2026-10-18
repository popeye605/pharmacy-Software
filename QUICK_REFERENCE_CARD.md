# 🎯 QUICK REFERENCE CARD

**Print this for your desk!**

---

## 🚀 START THE APP

```bash
cd "d:\pharmacy Software"
python pharmacy_app.py
```

---

## 👤 LOGIN CREDENTIALS

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin@123 |
| Staff | pharmacist1 | pass123 |

---

## 💳 MAKE A SALE (6 STEPS)

```
1. Click "Sale" button
2. Search product → Click "Add"
3. Adjust Qty, Price, Discount if needed
4. Enter Cash Received
5. Click "Pay & Save"
6. Select printer → Click "Print"
```

✅ Bill saves  
✅ Receipt prints  
✅ Log created  

---

## 🎯 KEY CHANGES MADE

| What | Before | After |
|-----|--------|-------|
| Currency | $ | **Rs.** |
| Payable Amount | 14px | **18px, Green** |
| Balance Amount | Regular | **16px, Blue** |
| Error Handling | Crashes | **Shows Message** |
| Input Fields | Plain | **Bordered** |
| Print Dialog | None | **Auto Appears** |
| Logs | Delayed | **Real-Time** |

---

## 📊 AVAILABLE MODULES (7 TOTAL)

- **Dashboard** - 8 KPI cards, recent sales
- **Sale (POS)** - Main billing system
- **Inventory** - Product management
- **Bill History** - Search & reprint bills
- **Activity Logs** - Track transactions (Admin)
- **Users** - Manage staff (Admin)
- **Profile** - User settings

---

## 🖨️ PRINTING RECEIPTS

**Automatic When Saving Bill**:
1. Print dialog appears
2. Select thermal printer
3. Click "Print"
4. Done! Receipt prints

**Professional Format**:
- Hospital name at top
- All amounts in "Rs. "
- Thermal printer compatible
- Clear, readable layout

---

## 📋 DEFAULT DATABASE

- ✅ 12 tables (all working)
- ✅ 3 users pre-configured
- ✅ 8 sample products
- ✅ 6 categories
- ✅ Complete indexes

---

## ⚠️ COMMON ISSUES

| Issue | Solution |
|-------|----------|
| App won't start | Check Python installed |
| Can't login | Check username/password |
| No print dialog | Check printer installed in Windows |
| Hard to read numbers | Increase screen zoom (Ctrl++) |
| Printer not printing | Check printer is on, USB connected |

---

## 📁 IMPORTANT FILES

| File | Size | Purpose |
|------|------|---------|
| pharmacy_app.py | 74.5 KB | Main app |
| pharmacy_pos.db | 106.5 KB | Database |
| db_init.py | 10.9 KB | Database setup |
| verify_db.py | 975 B | Check database |

---

## 📚 DOCUMENTATION

**Quick Start** (5 min):  
→ CHANGES_SUMMARY.md

**Getting Started** (10 min):  
→ README.md

**Printer Setup** (20 min):  
→ THERMAL_PRINTER_GUIDE.md

**Full Details** (30 min):  
→ FIXES_APPLIED.md or UPDATE_REPORT_FINAL.md

**Find Anything** (Quick):  
→ INDEX_AND_NAVIGATION.md

---

## ✅ VERIFICATION

**Check Database**:
```bash
python verify_db.py
```

**Expected Output**:
```
✓ Database has 12 tables
✓ Users: 3
✓ Active Products: 8
✓ Categories: 6
✓ Database verification successful!
```

---

## 💡 QUICK TIPS

- 🔍 Search products by serial number (faster)
- 📦 Hold bills to resume later
- 💰 Use discount % for bulk deals
- 📊 Export logs for record-keeping
- 🗂️ Backup database weekly
- 🖥️ Maximize window for better visibility
- 🖨️ Set thermal printer as default
- 📝 Review activity logs weekly

---

## 🔑 KEY NUMBERS

- **Payable Font**: 18px (Large & Green)
- **Balance Font**: 16px (Large & Blue)
- **Input Fonts**: 13px (Readable)
- **Labels Font**: 12px (Bold)
- **Database**: 12 tables
- **Users**: 3 default accounts
- **Products**: 8 samples
- **Modules**: 7 total

---

## 🎯 WORKFLOW

```
User Opens App
    ↓
Logs In (admin/pharmacist1)
    ↓
Selects "Sale" Module
    ↓
Searches & Adds Products
    ↓
Applies Discount (if needed)
    ↓
Enters Cash Received
    ↓
Clicks "Pay & Save"
    ↓
Print Dialog Appears Auto
    ↓
Selects Thermal Printer
    ↓
Receipt Prints
    ↓
Bill Saves to Database
    ↓
Log Created Automatically
    ↓
Cart Clears
    ↓
Ready for Next Sale
```

---

## 🆘 EMERGENCY CONTACTS

**Database Reset**:
```bash
python db_init.py
```

**Database Check**:
```bash
python verify_db.py
```

**See System Info**:
```bash
python QUICK_START.py
```

**Force Restart**:
```bash
Close app, delete __pycache__, run again
```

---

## 📞 TROUBLESHOOTING MATRIX

| Problem | First Try | If Not | Then |
|---------|-----------|--------|------|
| App won't start | python --version | pip install PyQt6 | restart computer |
| Can't login | Check caps lock | Reset in db_init.py | verify_db.py |
| Print not working | Check printer on | Reinstall driver | test from Notepad |
| Numbers hard to read | Zoom screen | Maximize window | check monitor |
| Database error | Run verify_db.py | Delete __pycache__ | Reinit database |

---

## 💾 MAINTENANCE

### Daily:
- ✅ Close app properly
- ✅ Keep printer stocked

### Weekly:
- ✅ Backup database
- ✅ Review logs
- ✅ Test printer

### Monthly:
- ✅ Update drivers
- ✅ Archive old logs
- ✅ Clean database

### Quarterly:
- ✅ Full system backup
- ✅ Update software
- ✅ Security review

---

## 🎉 YOU'RE ALL SET!

The pharmacy POS system is:
✅ Ready to use
✅ Fully tested
✅ Production ready
✅ Well documented
✅ Professional quality

**Start using it now!**

```bash
python pharmacy_app.py
```

---

**Last Updated**: January 23, 2026  
**Version**: 2.0  
**Status**: 🟢 Ready for Production

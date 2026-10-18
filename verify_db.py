import sqlite3

conn = sqlite3.connect('pharmacy_pos.db')
c = conn.cursor()

# Check tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in c.fetchall()]
print(f"✓ Database has {len(tables)} tables: {tables}")

# Check users
c.execute("SELECT COUNT(*) FROM users")
user_count = c.fetchone()[0]
print(f"✓ Users: {user_count}")

# Check products
c.execute("SELECT COUNT(*) FROM products WHERE is_active = 1")
product_count = c.fetchone()[0]
print(f"✓ Active Products: {product_count}")

# Check categories
c.execute("SELECT COUNT(*) FROM categories")
cat_count = c.fetchone()[0]
print(f"✓ Categories: {cat_count}")

# Check default user
c.execute("SELECT username, role FROM users WHERE username = 'admin'")
admin = c.fetchone()
if admin:
    print(f"✓ Admin user exists: {admin[0]} ({admin[1]} role)")

conn.close()
print("\n✓ Database verification successful! Ready to run pharmacy_app.py")

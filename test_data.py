# # test_products.py
# from sqlalchemy import create_engine, text
# from database.database import engine

# def test_products():
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text("SELECT * FROM products"))
#             products = result.fetchall()
            
#             print(f"✅ Found {len(products)} products:")
#             for product in products:
#                 print(f"  • {product[1]} - ${product[3]} (ID: {product[0]})")
                
#     except Exception as e:
#         print(f"❌ Error: {e}")

# if __name__ == "__main__":
#     test_products()

# test_bcrypt.py
# try:
#     import bcrypt
#     print(f"bcrypt version: {bcrypt.__version__}")
#     print("✅ Bcrypt installed correctly!")
    
#     # Test hashing
#     password = b"password123"
#     hashed = bcrypt.hashpw(password, bcrypt.gensalt())
#     print("Hashing test: PASSED")
    
# except Exception as e:
#     print(f"❌ Error: {e}")

# test_hashing.py
from auth.auth import test_hashing

if __name__ == "__main__":
    print("Testing password hashing...")
    test_hashing()
